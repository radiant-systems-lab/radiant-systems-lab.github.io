"""Unit tests for the lab progress API.

Run from infra/labs-backend with:  python -m unittest discover -s tests
No AWS access or boto3 install is needed; the table is faked.
"""

import json
import os
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src" / "api"))

import app  # noqa: E402  (the API; the sign-up trigger is loaded by path below)

OWNER = "owner@missouri.edu"
OWNER_ID = "owner@umsystem.edu"       # the same mailbox, as stored
STUDENT_SUB = "11111111-1111-1111-1111-111111111111"
OTHER_SUB = "22222222-2222-2222-2222-222222222222"


class ConditionFailed(Exception):
    pass


def split_top_level(text):
    """Split a SET list on commas that are not inside parentheses."""
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            parts.append(text[start:i])
            start = i + 1
    parts.append(text[start:])
    return [p.strip() for p in parts]


class FakeTable:
    """Just enough of a DynamoDB Table for Store, with a real lock condition."""

    class meta:
        class client:
            class exceptions:
                ConditionalCheckFailedException = ConditionFailed

    def __init__(self):
        self.items = {}
        self.calls = []

    def _key(self, key):
        return (key["PK"], key["SK"])

    def get_item(self, Key, **kwargs):
        item = self.items.get(self._key(Key))
        return {"Item": dict(item)} if item else {}

    def put_item(self, Item):
        self.items[(Item["PK"], Item["SK"])] = dict(Item)

    def delete_item(self, Key):
        self.items.pop(self._key(Key), None)

    def update_item(self, Key, UpdateExpression, ExpressionAttributeValues,
                    ReturnValues, ExpressionAttributeNames=None,
                    ConditionExpression=None):
        self.calls.append({
            "names": ExpressionAttributeNames or {},
            "values": ExpressionAttributeValues,
            "condition": ConditionExpression,
            "update": UpdateExpression,
        })
        names = ExpressionAttributeNames or {}
        values = ExpressionAttributeValues
        # Every name and value has to be used, or DynamoDB rejects the call.
        text = UpdateExpression + " " + (ConditionExpression or "")
        for placeholder in list(names) + list(values):
            assert placeholder in text, f"unused placeholder {placeholder}"

        key = self._key(Key)
        current = self.items.get(key)
        if ConditionExpression == "attribute_exists(PK)" and current is None:
            raise ConditionFailed()
        if ConditionExpression and "#locked" in ConditionExpression:
            if current and current.get("locked"):
                raise ConditionFailed()

        item = dict(current or {"PK": Key["PK"], "SK": Key["SK"]})
        for clause in split_top_level(UpdateExpression[len("SET "):]):
            field, expr = [p.strip() for p in clause.split(" = ", 1)]
            field = names.get(field, field)
            if expr.startswith("if_not_exists("):
                inner, _, rest = expr[len("if_not_exists("):].partition(")")
                _, default = [p.strip() for p in inner.split(",")]
                value = item.get(field, values[default])
                if rest.strip().startswith("+"):
                    value = value + values[rest.strip()[1:].strip()]
                item[field] = value
            else:
                item[field] = values[expr]
        self.items[key] = item
        return {"Attributes": dict(item)}

    def query(self, KeyConditionExpression, ExpressionAttributeValues,
              IndexName=None, ExclusiveStartKey=None):
        pk = ExpressionAttributeValues[":pk"]
        field = "GSI1PK" if IndexName == "GSI1" else "PK"
        prefix = ExpressionAttributeValues.get(":prefix", "")
        found = [dict(i) for i in self.items.values()
                 if i.get(field) == pk and i["SK"].startswith(prefix)]
        return {"Items": found}


class UserNotFound(Exception):
    pass


class FakeCognito:
    """Just enough of the Cognito client for Accounts."""

    class exceptions:
        UserNotFoundException = UserNotFound

    def __init__(self):
        import datetime
        self.users = {}
        self.now = datetime.datetime(2026, 9, 16, 22, 0, tzinfo=datetime.timezone.utc)

    def add(self, username, email, status="UNCONFIRMED"):
        self.users[username] = {"status": status, "email": email, "verified": "false"}

    def list_users(self, UserPoolId, Limit, Filter, PaginationToken=None):
        wanted = Filter.split('"')[1]
        users = [{"Username": u, "UserCreateDate": self.now,
                  "Attributes": [{"Name": "email", "Value": v["email"]}]}
                 for u, v in self.users.items() if v["status"] == wanted]
        # Serve two pages so the paging loop is exercised.
        if PaginationToken is None and len(users) > 1:
            return {"Users": users[:1], "PaginationToken": "next"}
        return {"Users": users[1:] if PaginationToken else users}

    def admin_get_user(self, UserPoolId, Username):
        if Username not in self.users:
            raise UserNotFound()
        return {"UserStatus": self.users[Username]["status"]}

    def admin_confirm_sign_up(self, UserPoolId, Username):
        self.users[Username]["status"] = "CONFIRMED"

    def admin_update_user_attributes(self, UserPoolId, Username, UserAttributes):
        assert UserAttributes == [{"Name": "email_verified", "Value": "true"}]
        self.users[Username]["verified"] = "true"

    def admin_delete_user(self, UserPoolId, Username):
        del self.users[Username]

    def admin_set_user_password(self, UserPoolId, Username, Password, Permanent):
        assert Permanent is False
        self.users[Username]["status"] = "FORCE_CHANGE_PASSWORD"
        self.users[Username]["password"] = Password

    def admin_user_global_sign_out(self, UserPoolId, Username):
        self.users[Username]["signed_out"] = True


def event(route, sub=STUDENT_SUB, email="student@umsystem.edu", body=None,
          params=None, verified="true", token_use="id"):
    return {
        "routeKey": route,
        "pathParameters": params or {},
        "body": json.dumps(body) if body is not None else None,
        "requestContext": {"authorizer": {"jwt": {"claims": {
            "sub": sub, "email": email, "email_verified": verified,
            "token_use": token_use,
        }}}},
    }


class ApiTest(unittest.TestCase):
    def setUp(self):
        os.environ["OWNER_EMAILS"] = f"{OWNER}, Second.Owner@missouri.edu"
        self.table = FakeTable()
        self.cognito = FakeCognito()
        self.store = app.Store(self.table, app.Accounts(self.cognito, "pool"))

    def call(self, *args, **kwargs):
        res = app.handler(event(*args, **kwargs), None, store=self.store)
        return res["statusCode"], json.loads(res["body"])

    def save(self, state, submit=False, sub=STUDENT_SUB, email="student@umsystem.edu"):
        return self.call("PUT /labs/{lab}/progress", sub=sub, email=email,
                         params={"lab": "week_01"},
                         body={"state": state, "submit": submit})

    # identity ---------------------------------------------------------------

    def test_unverified_email_is_refused(self):
        status, _ = self.call("GET /me", verified="false")
        self.assertEqual(status, 403)

    def test_access_token_is_refused(self):
        status, _ = self.call("GET /me", token_use="access")
        self.assertEqual(status, 401)

    def test_unknown_route(self):
        status, _ = self.call("GET /nope")
        self.assertEqual(status, 404)

    def test_owner_detection_ignores_case(self):
        status, body = self.call("GET /me", email="SECOND.owner@Missouri.edu")
        self.assertEqual(status, 200)
        self.assertTrue(body["owner"])
        self.assertTrue(body["admin"])

    # saving -----------------------------------------------------------------

    def test_save_then_load_round_trip(self):
        status, body = self.save({"q1": "b", "size": 3.5})
        self.assertEqual(status, 200)
        self.assertEqual(body["saves"], 1)
        self.assertFalse(body["submitted"])

        self.save({"q1": "c", "size": 25.0})
        status, body = self.call("GET /labs/{lab}/progress", params={"lab": "week_01"})
        self.assertEqual(status, 200)
        self.assertEqual(body["state"], {"q1": "c", "size": 25.0})
        self.assertFalse(body["locked"])

    def test_submit_marks_submitted_and_keeps_history(self):
        self.save({"q1": "b"})
        status, body = self.save({"q1": "b", "done": True}, submit=True)
        self.assertEqual(status, 200)
        self.assertTrue(body["submitted"])
        history = [k for k in self.table.items if k[1].startswith("SUBMIT#week_01#")]
        self.assertEqual(len(history), 1)

    def test_students_cannot_read_each_other(self):
        self.save({"secret": 1})
        status, body = self.call("GET /labs/{lab}/progress", sub=OTHER_SUB,
                                 email="other@umsystem.edu", params={"lab": "week_01"})
        self.assertEqual(status, 200)
        self.assertEqual(body["state"], {})

    def test_bad_lab_id(self):
        status, _ = self.call("GET /labs/{lab}/progress", params={"lab": "../x"})
        self.assertEqual(status, 400)

    def test_state_must_be_object(self):
        status, _ = self.call("PUT /labs/{lab}/progress", params={"lab": "week_01"},
                              body={"state": [1, 2]})
        self.assertEqual(status, 400)

    def test_oversized_state(self):
        status, _ = self.save({"essay": "x" * 70_000})
        self.assertEqual(status, 413)

    def test_invalid_json(self):
        ev = event("PUT /labs/{lab}/progress", params={"lab": "week_01"})
        ev["body"] = "{not json"
        res = app.handler(ev, None, store=self.store)
        self.assertEqual(res["statusCode"], 400)

    # locking ----------------------------------------------------------------

    def test_lab_lock_blocks_students_but_not_admins(self):
        self.save({"q1": "a"})
        status, _ = self.call("PUT /admin/labs/{lab}/lock", email=OWNER,
                              sub=OTHER_SUB, params={"lab": "week_01"},
                              body={"locked": True})
        self.assertEqual(status, 200)

        status, _ = self.save({"q1": "b"})
        self.assertEqual(status, 423)
        status, body = self.call("GET /labs/{lab}/progress", params={"lab": "week_01"})
        self.assertTrue(body["locked"])
        self.assertEqual(body["state"], {"q1": "a"})

        status, _ = self.save({"q1": "b"}, sub=OTHER_SUB, email=OWNER)
        self.assertEqual(status, 200)

    def test_student_lock_is_individual(self):
        self.save({"q1": "a"})
        self.save({"q1": "a"}, sub=OTHER_SUB, email="other@umsystem.edu")
        status, row = self.call(
            "PUT /admin/labs/{lab}/students/{student}/lock", email=OWNER, sub=OTHER_SUB,
            params={"lab": "week_01", "student": "student%40umsystem.edu"}, body={"locked": True})
        self.assertEqual(status, 200)
        self.assertTrue(row["locked"])

        self.assertEqual(self.save({"q1": "z"})[0], 423)
        self.assertEqual(self.save({"q1": "z"}, sub=OTHER_SUB,
                                   email="other@umsystem.edu")[0], 200)

        self.call("PUT /admin/labs/{lab}/students/{student}/lock", email=OWNER,
                  sub=OTHER_SUB, params={"lab": "week_01", "student": "student@umsystem.edu"},
                  body={"locked": False})
        self.assertEqual(self.save({"q1": "z"})[0], 200)

    def test_locking_a_student_who_never_opened_the_lab(self):
        status, _ = self.call(
            "PUT /admin/labs/{lab}/students/{student}/lock", email=OWNER,
            params={"lab": "week_01", "student": "other@umsystem.edu"}, body={"locked": True})
        self.assertEqual(status, 404)

    def test_lock_needs_a_boolean(self):
        status, _ = self.call("PUT /admin/labs/{lab}/lock", email=OWNER,
                              params={"lab": "week_01"}, body={"locked": "yes"})
        self.assertEqual(status, 400)

    def test_save_expression_uses_every_placeholder(self):
        # FakeTable asserts this; run both the locked and forced paths.
        self.save({"a": 1}, submit=True)
        self.save({"a": 1}, sub=OTHER_SUB, email=OWNER, submit=True)
        self.assertIsNone(self.table.calls[-1]["condition"])
        self.assertIn("#locked", self.table.calls[0]["condition"])

    # admin access -----------------------------------------------------------

    def test_students_cannot_use_admin_routes(self):
        for route, params, body in [
            ("GET /admin/labs", {}, None),
            ("GET /admin/labs/{lab}/progress", {"lab": "week_01"}, None),
            ("PUT /admin/labs/{lab}/lock", {"lab": "week_01"}, {"locked": True}),
            ("GET /admin/admins", {}, None),
            ("POST /admin/admins", {}, {"email": "me@umsystem.edu"}),
            ("GET /admin/accounts/pending", {}, None),
        ]:
            status, _ = self.call(route, params=params, body=body)
            self.assertEqual(status, 403, route)

    def test_owner_adds_admin_who_can_then_lock_but_not_add(self):
        status, _ = self.call("POST /admin/admins", email=OWNER, sub=OTHER_SUB,
                              body={"email": " TA@Example.com "})
        self.assertEqual(status, 200)

        status, body = self.call("GET /me", email="ta@example.com")
        self.assertTrue(body["admin"])
        self.assertFalse(body["owner"])

        status, _ = self.call("PUT /admin/labs/{lab}/lock", email="ta@example.com",
                              params={"lab": "week_02"}, body={"locked": True})
        self.assertEqual(status, 200)

        status, _ = self.call("POST /admin/admins", email="ta@example.com",
                              body={"email": "friend@example.com"})
        self.assertEqual(status, 403)

        status, body = self.call("GET /admin/admins", email="ta@example.com")
        emails = [a["email"] for a in body["admins"]]
        self.assertEqual(emails[:2], [OWNER_ID, "second.owner@umsystem.edu"])
        self.assertIn("ta@example.com", emails)

        status, _ = self.call("DELETE /admin/admins/{email}", email=OWNER,
                              params={"email": "ta@example.com"})
        self.assertEqual(status, 200)
        status, body = self.call("GET /me", email="ta@example.com")
        self.assertFalse(body["admin"])

    def test_owners_cannot_be_removed_or_re_added(self):
        status, _ = self.call("DELETE /admin/admins/{email}", email=OWNER,
                              params={"email": "second.owner@missouri.edu"})
        self.assertEqual(status, 400)
        status, _ = self.call("POST /admin/admins", email=OWNER,
                              body={"email": OWNER})
        self.assertEqual(status, 400)

    def test_add_admin_rejects_bad_email(self):
        for bad in ["", "no-at-sign", "a@b", None, 5]:
            status, _ = self.call("POST /admin/admins", email=OWNER, body={"email": bad})
            self.assertEqual(status, 400, bad)

    def test_admin_sees_every_student_in_a_lab(self):
        self.save({"q1": "a"}, submit=True)
        self.save({"q1": "b"}, sub=OTHER_SUB, email="other@umsystem.edu")
        status, body = self.call("GET /admin/labs/{lab}/progress", email=OWNER,
                                 sub="33333333-3333-3333-3333-333333333333",
                                 params={"lab": "week_01"})
        self.assertEqual(status, 200)
        by_email = {r["email"]: r for r in body["students"]}
        self.assertEqual(set(by_email), {"student@umsystem.edu", "other@umsystem.edu"})
        self.assertTrue(by_email["student@umsystem.edu"]["submitted"])
        self.assertEqual(by_email["other@umsystem.edu"]["id"], "other@umsystem.edu")
        self.assertEqual(by_email["other@umsystem.edu"]["state"], {"q1": "b"})

    # accounts whose code never arrived --------------------------------------

    def test_admin_lists_and_confirms_pending_accounts(self):
        self.cognito.add("a@umsystem.edu", "a@missouri.edu")
        self.cognito.add("b@umsystem.edu", "b@umsystem.edu")
        self.cognito.add("c@umsystem.edu", "c@umsystem.edu", status="CONFIRMED")
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta@umsystem.edu"})

        status, body = self.call("GET /admin/accounts/pending", email="ta@umsystem.edu")
        self.assertEqual(status, 200)
        self.assertEqual({a["username"] for a in body["accounts"]},
                         {"a@umsystem.edu", "b@umsystem.edu"})
        self.assertEqual(body["accounts"][0]["createdAt"], "2026-09-16T22:00:00+00:00")

        status, body = self.call("POST /admin/accounts/confirm", email="ta@umsystem.edu",
                                 body={"usernames": ["a@umsystem.edu", "c@umsystem.edu",
                                                     "nobody@umsystem.edu"]})
        self.assertEqual(status, 200)
        by_name = {r["username"]: r for r in body["results"]}
        self.assertTrue(by_name["a@umsystem.edu"]["confirmed"])
        self.assertFalse(by_name["c@umsystem.edu"]["confirmed"])
        self.assertFalse(by_name["nobody@umsystem.edu"]["confirmed"])
        self.assertEqual(self.cognito.users["a@umsystem.edu"],
                         {"status": "CONFIRMED", "email": "a@missouri.edu", "verified": "true"})

    def test_students_cannot_touch_accounts(self):
        self.cognito.add("a@umsystem.edu", "a@umsystem.edu")
        self.assertEqual(self.call("GET /admin/accounts/pending")[0], 403)
        self.assertEqual(self.call("POST /admin/accounts/confirm",
                                   body={"usernames": ["a@umsystem.edu"]})[0], 403)
        self.assertEqual(self.call("DELETE /admin/accounts/{username}",
                                   params={"username": "a@umsystem.edu"})[0], 403)
        self.assertEqual(self.cognito.users["a@umsystem.edu"]["status"], "UNCONFIRMED")

    def test_only_owners_confirm_staff_accounts(self):
        # A student signs up with an owner's address and with an admin's address.
        self.cognito.add("second.owner@umsystem.edu", "second.owner@missouri.edu")
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta@umsystem.edu"})
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta2@umsystem.edu"})
        self.cognito.add("ta2@umsystem.edu", "ta2@umsystem.edu")

        status, body = self.call("GET /admin/accounts/pending", email="ta@umsystem.edu")
        self.assertTrue(all(a["staff"] for a in body["accounts"]))

        status, body = self.call("POST /admin/accounts/confirm", email="ta@umsystem.edu",
                                 body={"usernames": ["second.owner@umsystem.edu",
                                                     "ta2@umsystem.edu"]})
        self.assertFalse(any(r["confirmed"] for r in body["results"]))
        self.assertEqual(self.call("DELETE /admin/accounts/{username}", email="ta@umsystem.edu",
                                   params={"username": "ta2%40umsystem.edu"})[0], 403)

        status, body = self.call("POST /admin/accounts/confirm", email=OWNER,
                                 body={"usernames": ["ta2@umsystem.edu"]})
        self.assertTrue(body["results"][0]["confirmed"])

    def test_remove_pending_account(self):
        self.cognito.add("a@umsystem.edu", "a@umsystem.edu")
        self.cognito.add("c@umsystem.edu", "c@umsystem.edu", status="CONFIRMED")
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta@umsystem.edu"})
        status, _ = self.call("DELETE /admin/accounts/{username}", email="ta@umsystem.edu",
                              params={"username": "a%40umsystem.edu"})
        self.assertEqual(status, 200)
        self.assertNotIn("a@umsystem.edu", self.cognito.users)
        status, _ = self.call("DELETE /admin/accounts/{username}", email=OWNER,
                              params={"username": "c@umsystem.edu"})
        self.assertEqual(status, 409)
        self.assertIn("c@umsystem.edu", self.cognito.users)

    def test_confirm_rejects_bad_input(self):
        for bad in [None, [], "a@umsystem.edu", [5], ["x"] * 101]:
            status, _ = self.call("POST /admin/accounts/confirm", email=OWNER,
                                  body={"usernames": bad})
            self.assertEqual(status, 400, bad)
        # Usernames are always the folded spelling; anything else is refused.
        self.cognito.add("a@missouri.edu", "a@missouri.edu")
        status, body = self.call("POST /admin/accounts/confirm", email=OWNER,
                                 body={"usernames": ["a@missouri.edu"]})
        self.assertFalse(body["results"][0]["confirmed"])

    def test_admin_resets_a_student_password(self):
        import re
        self.cognito.add("a@umsystem.edu", "a@missouri.edu", status="CONFIRMED")
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta@umsystem.edu"})
        status, body = self.call("POST /admin/accounts/reset-password",
                                 email="ta@umsystem.edu", body={"email": "A@Mail.Missouri.edu"})
        self.assertEqual(status, 200)
        self.assertEqual(body["username"], "a@umsystem.edu")
        self.assertRegex(body["temporaryPassword"], r"^[a-z]{4}-[2-9]{4}-[a-z]{4}$")
        user = self.cognito.users["a@umsystem.edu"]
        self.assertEqual(user["status"], "FORCE_CHANGE_PASSWORD")
        self.assertEqual(user["password"], body["temporaryPassword"])
        self.assertTrue(user["signed_out"])
        # Every reset gives a different password.
        _, again = self.call("POST /admin/accounts/reset-password", email=OWNER,
                             body={"email": "a@umsystem.edu"})
        self.assertNotEqual(again["temporaryPassword"], body["temporaryPassword"])

    def test_reset_password_rules(self):
        self.cognito.add("waiting@umsystem.edu", "waiting@umsystem.edu")
        self.cognito.add("second.owner@umsystem.edu", "second.owner@umsystem.edu", status="CONFIRMED")
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta@umsystem.edu"})
        cases = [
            ("student@umsystem.edu", {"email": "x@umsystem.edu"}, 403),     # students cannot
            ("ta@umsystem.edu", {"email": "nobody@umsystem.edu"}, 404),
            ("ta@umsystem.edu", {"email": "waiting@umsystem.edu"}, 409),   # approve instead
            ("ta@umsystem.edu", {"email": "second.owner@missouri.edu"}, 403),
            ("ta@umsystem.edu", {"email": 7}, 400),
        ]
        for who, body, want in cases:
            status, _ = self.call("POST /admin/accounts/reset-password", email=who, body=body)
            self.assertEqual(status, want, (who, body))
        status, _ = self.call("POST /admin/accounts/reset-password", email=OWNER,
                              body={"email": "second.owner@umsystem.edu"})
        self.assertEqual(status, 200)

    # one mailbox, three spellings ---------------------------------------------

    def test_aliases_share_one_record(self):
        self.save({"q1": "a"}, email="Pawprint@Missouri.edu")
        status, body = self.call("GET /labs/{lab}/progress", sub=OTHER_SUB,
                                 email="pawprint@mail.missouri.edu",
                                 params={"lab": "week_01"})
        self.assertEqual(body["state"], {"q1": "a"})
        status, body = self.call("GET /me", email="pawprint@missouri.edu")
        self.assertEqual(body["email"], "pawprint@umsystem.edu")
        self.assertEqual(body["address"], "pawprint@missouri.edu")

    def test_owner_by_any_spelling(self):
        for spelling in ["owner@missouri.edu", "owner@umsystem.edu", "owner@mail.missouri.edu"]:
            status, body = self.call("GET /me", email=spelling)
            self.assertTrue(body["owner"], spelling)

    def test_admin_by_any_spelling(self):
        self.call("POST /admin/admins", email=OWNER, body={"email": "ta@mail.missouri.edu"})
        status, body = self.call("GET /me", email="TA@umsystem.edu")
        self.assertTrue(body["admin"])
        self.call("DELETE /admin/admins/{email}", email=OWNER,
                  params={"email": "ta%40missouri.edu"})
        status, body = self.call("GET /me", email="ta@umsystem.edu")
        self.assertFalse(body["admin"])

    def test_other_domains_are_not_folded(self):
        self.save({"q1": "a"}, email="pawprint@gmail.com")
        status, body = self.call("GET /labs/{lab}/progress", email="pawprint@umsystem.edu",
                                 params={"lab": "week_01"})
        self.assertEqual(body["state"], {})
        self.assertEqual(app.canonical("a@evil-missouri.edu"), "a@evil-missouri.edu")
        self.assertEqual(app.canonical("a@missouri.edu.evil.com"), "a@missouri.edu.evil.com")

    def test_decimals_serialise(self):
        res = app.respond(200, {"n": app.Decimal("3"), "f": app.Decimal("2.5")})
        self.assertEqual(json.loads(res["body"]), {"n": 3, "f": 2.5})


class PreSignUpTest(unittest.TestCase):
    def setUp(self):
        import importlib.util

        os.environ["ALLOWED_DOMAINS"] = "umsystem.edu, missouri.edu,mail.missouri.edu"
        os.environ["OWNER_EMAILS"] = OWNER
        path = HERE.parent / "src" / "presignup" / "app.py"
        spec = importlib.util.spec_from_file_location("presignup_app", path)
        self.pre = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.pre)
        self.table = FakeTable()
        self.pre._table = self.table

    def run_trigger(self, email, source="PreSignUp_SignUp", username=None):
        return self.pre.handler(
            {"triggerSource": source,
             "userName": self.pre.canonical(email) if username is None else username,
             "request": {"userAttributes": {"email": email}}},
            None,
        )

    def test_university_domains_allowed(self):
        for email in ["a@umsystem.edu", "B@Missouri.edu", "c@mail.missouri.edu"]:
            self.run_trigger(email)

    def test_other_domains_refused(self):
        for email in ["a@gmail.com", "a@evil-missouri.edu", "a@umsystem.edu.evil.com"]:
            with self.assertRaises(Exception, msg=email):
                self.run_trigger(email)

    def test_owner_and_listed_admin_allowed_anywhere(self):
        self.run_trigger(OWNER)
        self.table.put_item({"PK": "CONFIG", "SK": "ADMIN#ta@gmail.com"})
        self.run_trigger("TA@gmail.com")

    def test_username_must_be_the_folded_address(self):
        self.run_trigger("x@missouri.edu", username="x@umsystem.edu")
        for wrong in ["x@missouri.edu", "someone-else@umsystem.edu", ""]:
            with self.assertRaises(Exception, msg=wrong):
                self.run_trigger("x@missouri.edu", username=wrong)

    def test_owner_alias_allowed(self):
        self.run_trigger("owner@umsystem.edu")

    def test_operator_created_accounts_skip_the_check(self):
        self.run_trigger("tester@example.com", source="PreSignUp_AdminCreateUser")


if __name__ == "__main__":
    unittest.main()
