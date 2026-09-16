"""Progress API for the CSC/EE 8001 class labs.

API Gateway verifies the Cognito ID token before this function runs, so the
claims in the request context can be trusted. A student's identity always comes
from those claims and never from the request body, which is what stops one
student from writing into another student's record.

Work is kept per semester ("term"), so a student who takes the course again in a
later year starts fresh, and last year's answers and locks stay where they were.
The current term follows the calendar (January to May is spring, June and July
summer, August to December fall) unless an owner sets it on the dashboard.

Table layout (one table, string keys):

    PK                  SK                            what it holds
    USER#<id>           LAB#<term>#<lab>              latest answers for one lab
    USER#<id>           SUBMIT#<term>#<lab>#<time>    every submission, as history
    USER#<id>           PROFILE                       last term the person was active
    LAB#<term>#<lab>    SETTINGS                      whether the whole lab is locked
    CONFIG              ADMIN#<id>                    admins added by an owner
    CONFIG              TERM#<term>                   a term that has saved work
    CONFIG              CURRENT_TERM                  an owner's choice of term

GSI1 lists one lab's students in a term (GSI1PK = LAB#<term>#<lab>), the lab
settings of a term (GSI1PK = LABS#<term>), and everyone's profile
(GSI1PK = PROFILES).

A person's <id> is their verified email with university aliases folded
together: x@missouri.edu, x@mail.missouri.edu and x@umsystem.edu are one
mailbox, so all three become x@umsystem.edu (see canonical()). The sign-in page
uses the same id as the Cognito username, so there is one account per person.

Owners come from the OWNER_EMAILS environment variable, so they cannot be
removed from the dashboard. Only owners can add or remove admins, choose the
term, or clear out old accounts. Owners and admins can lock labs and students.

New accounts wait for an admin to approve them, since Cognito's emails do not
reach university inboxes. A student who forgot their password asks an admin to
delete the account and creates it again; saved work is keyed by email, not by
account, so nothing is lost. An account that would be an owner or an admin can
only be approved or deleted by an owner, so a student cannot claim a staff
address and have it approved by a TA.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import re
from datetime import date, datetime, timezone
from decimal import Decimal
from urllib.parse import unquote

log = logging.getLogger()
log.setLevel(logging.INFO)

LAB_ID = re.compile(r"^[a-z0-9_]{1,40}$")
EMAIL = re.compile(r"^[^@\s]{1,64}@[A-Za-z0-9.-]{1,190}\.[A-Za-z]{2,}$")
TERM_ID = re.compile(r"^(\d{4})-(spring|summer|fall)$")
SEASONS = ["spring", "summer", "fall"]
SEASON_START = {"spring": 1, "summer": 6, "fall": 8}     # month each term begins

MAX_BODY_BYTES = 100_000
MAX_STATE_BYTES = 64_000


class HttpError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status
        self.message = message


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def today() -> date:
    """Separate so the tests can pick the date."""
    return datetime.now(timezone.utc).date()


# -- terms -------------------------------------------------------------------

def term_for(day: date) -> str:
    season = "spring" if day.month <= 5 else "summer" if day.month <= 7 else "fall"
    return f"{day.year}-{season}"


def term_order(term: str) -> tuple[int, int]:
    m = TERM_ID.match(term)
    return (int(m.group(1)), SEASONS.index(m.group(2))) if m else (0, -1)


def term_label(term: str) -> str:
    m = TERM_ID.match(term)
    return f"{m.group(2).title()} {m.group(1)}" if m else term


def term_start(term: str) -> str:
    m = TERM_ID.match(term)
    return date(int(m.group(1)), SEASON_START[m.group(2)], 1).isoformat()


def next_term(term: str) -> str:
    year, i = term_order(term)
    return f"{year + (i == 2)}-{SEASONS[(i + 1) % 3]}"


def check_term(value) -> str:
    if not isinstance(value, str) or not TERM_ID.match(value):
        raise HttpError(400, "A semester looks like 2026-fall, 2027-spring or 2027-summer.")
    return value


# -- identity ----------------------------------------------------------------

def alias_domains() -> list[str]:
    """University domains that share one mailbox; the first is the canonical one."""
    raw = os.environ.get("ALIAS_DOMAINS", "umsystem.edu,missouri.edu,mail.missouri.edu")
    return [d.strip().lower() for d in raw.split(",") if d.strip()]


def canonical(email: str) -> str:
    """The id for an address: lower case, with university aliases folded together."""
    email = (email or "").strip().lower()
    local, at, domain = email.rpartition("@")
    domains = alias_domains()
    if at and local and domain in domains:
        return f"{local}@{domains[0]}"
    return email


def owners() -> set[str]:
    raw = os.environ.get("OWNER_EMAILS", "")
    return {canonical(e) for e in raw.split(",") if e.strip()}


class Accounts:
    """The Cognito calls the dashboard makes, so the tests can swap in a fake."""

    def __init__(self, client, pool_id: str):
        self.c = client
        self.pool = pool_id

    def everyone(self) -> list[dict]:
        """Every account, approved or waiting."""
        found: list[dict] = []
        kwargs = {"UserPoolId": self.pool, "Limit": 60}
        while True:
            page = self.c.list_users(**kwargs)
            for u in page.get("Users", []):
                attrs = {a["Name"]: a["Value"] for a in u.get("Attributes", [])}
                created = u.get("UserCreateDate")
                found.append({
                    "username": u["Username"],
                    "email": attrs.get("email", ""),
                    "status": u.get("UserStatus"),
                    "createdAt": created.isoformat(timespec="seconds") if created else None,
                })
            if not page.get("PaginationToken"):
                return found
            kwargs["PaginationToken"] = page["PaginationToken"]

    def status(self, username: str) -> str | None:
        try:
            return self.c.admin_get_user(UserPoolId=self.pool, Username=username)["UserStatus"]
        except self.c.exceptions.UserNotFoundException:
            return None

    def confirm(self, username: str) -> None:
        self.c.admin_confirm_sign_up(UserPoolId=self.pool, Username=username)
        self.c.admin_update_user_attributes(
            UserPoolId=self.pool, Username=username,
            UserAttributes=[{"Name": "email_verified", "Value": "true"}],
        )

    def remove(self, username: str) -> None:
        self.c.admin_delete_user(UserPoolId=self.pool, Username=username)


class Store:
    """Every DynamoDB call the API makes, so the tests can swap in a fake."""

    def __init__(self, table, accounts: Accounts | None = None):
        self.t = table
        self.accounts = accounts

    # -- admins ------------------------------------------------------------

    def is_listed_admin(self, email: str) -> bool:
        res = self.t.get_item(
            Key={"PK": "CONFIG", "SK": f"ADMIN#{email}"}, ProjectionExpression="PK"
        )
        return "Item" in res

    def list_admins(self) -> list[dict]:
        return self._query(
            "PK = :pk AND begins_with(SK, :prefix)",
            {":pk": "CONFIG", ":prefix": "ADMIN#"},
        )

    def add_admin(self, email: str, by: str) -> None:
        self.t.put_item(Item={
            "PK": "CONFIG", "SK": f"ADMIN#{email}",
            "email": email, "addedBy": by, "addedAt": now(),
        })

    def remove_admin(self, email: str) -> None:
        self.t.delete_item(Key={"PK": "CONFIG", "SK": f"ADMIN#{email}"})

    # -- terms -------------------------------------------------------------

    def term_choice(self) -> str | None:
        item = self.t.get_item(Key={"PK": "CONFIG", "SK": "CURRENT_TERM"}).get("Item")
        return item.get("term") if item else None

    def set_term_choice(self, term: str | None, by: str) -> None:
        if term is None:
            self.t.delete_item(Key={"PK": "CONFIG", "SK": "CURRENT_TERM"})
        else:
            self.t.put_item(Item={"PK": "CONFIG", "SK": "CURRENT_TERM",
                                  "term": term, "setBy": by, "setAt": now()})

    def terms_with_work(self) -> list[str]:
        items = self._query("PK = :pk AND begins_with(SK, :prefix)",
                            {":pk": "CONFIG", ":prefix": "TERM#"})
        return [i["SK"].split("#", 1)[1] for i in items]

    def note_activity(self, uid: str, email: str, term: str) -> None:
        """Remember that this term has work, and when this person was last active."""
        self.t.put_item(Item={"PK": "CONFIG", "SK": f"TERM#{term}", "term": term})
        profile = self.t.get_item(Key={"PK": f"USER#{uid}", "SK": "PROFILE"}).get("Item") or {}
        latest = profile.get("lastTerm")
        if latest and term_order(latest) > term_order(term):
            term = latest
        self.t.put_item(Item={
            "PK": f"USER#{uid}", "SK": "PROFILE", "GSI1PK": "PROFILES", "GSI1SK": uid,
            "email": email, "lastTerm": term, "lastSeen": now(),
        })

    def profiles(self) -> dict[str, dict]:
        items = self._query("GSI1PK = :pk", {":pk": "PROFILES"}, index="GSI1")
        return {i["GSI1SK"]: i for i in items}

    # -- lab settings ------------------------------------------------------

    def lab_settings(self, term: str, lab: str) -> dict:
        res = self.t.get_item(Key={"PK": f"LAB#{term}#{lab}", "SK": "SETTINGS"})
        return res.get("Item") or {}

    def all_lab_settings(self, term: str) -> list[dict]:
        return self._query("GSI1PK = :pk", {":pk": f"LABS#{term}"}, index="GSI1")

    def set_lab_lock(self, term: str, lab: str, locked: bool, by: str) -> dict:
        item = {
            "PK": f"LAB#{term}#{lab}", "SK": "SETTINGS",
            "GSI1PK": f"LABS#{term}", "GSI1SK": lab,
            "term": term, "lab": lab, "locked": locked, "lockedBy": by, "lockedAt": now(),
        }
        self.t.put_item(Item=item)
        return item

    # -- student progress --------------------------------------------------

    def progress(self, uid: str, term: str, lab: str) -> dict | None:
        res = self.t.get_item(Key={"PK": f"USER#{uid}", "SK": f"LAB#{term}#{lab}"})
        return res.get("Item")

    def lab_progress(self, term: str, lab: str) -> list[dict]:
        return self._query("GSI1PK = :pk", {":pk": f"LAB#{term}#{lab}"}, index="GSI1")

    def save_progress(self, uid: str, email: str, term: str, lab: str, state_json: str,
                      submit: bool, force: bool) -> dict:
        ts = now()
        names = {"#state": "state", "#locked": "locked", "#term": "term"}
        values = {
            ":state": state_json, ":ts": ts, ":email": email, ":lab": lab, ":term": term,
            ":gpk": f"LAB#{term}#{lab}", ":zero": 0, ":one": 1,
        }
        sets = [
            "#state = :state", "updatedAt = :ts", "email = :email", "lab = :lab",
            "#term = :term", "GSI1PK = :gpk", "GSI1SK = :email",
            "saves = if_not_exists(saves, :zero) + :one",
            "createdAt = if_not_exists(createdAt, :ts)",
        ]
        if submit:
            sets += [
                "submitted = :true", "submittedAt = :ts",
                "submissions = if_not_exists(submissions, :zero) + :one",
            ]
            values[":true"] = True

        kwargs = {
            "Key": {"PK": f"USER#{uid}", "SK": f"LAB#{term}#{lab}"},
            "UpdateExpression": "SET " + ", ".join(sets),
            "ExpressionAttributeValues": values,
            "ReturnValues": "ALL_NEW",
        }
        if force:
            # #locked only appears in the condition; DynamoDB rejects unused names.
            del names["#locked"]
        else:
            # Checked in the same write, so a lock placed a moment earlier still wins.
            kwargs["ConditionExpression"] = "attribute_not_exists(#locked) OR #locked = :false"
            values[":false"] = False
        kwargs["ExpressionAttributeNames"] = names

        try:
            item = self.t.update_item(**kwargs)["Attributes"]
        except self.t.meta.client.exceptions.ConditionalCheckFailedException:
            raise HttpError(423, "An instructor has locked your answers for this lab.")

        if item.get("saves") == 1:
            self.note_activity(uid, email, term)
        if submit:
            self.t.put_item(Item={
                "PK": f"USER#{uid}", "SK": f"SUBMIT#{term}#{lab}#{ts}",
                "email": email, "term": term, "lab": lab, "state": state_json,
                "submittedAt": ts,
            })
        return item

    def set_student_lock(self, uid: str, term: str, lab: str, locked: bool, by: str) -> dict:
        try:
            res = self.t.update_item(
                Key={"PK": f"USER#{uid}", "SK": f"LAB#{term}#{lab}"},
                UpdateExpression="SET #locked = :locked, lockedBy = :by, lockedAt = :ts",
                ConditionExpression="attribute_exists(PK)",
                ExpressionAttributeNames={"#locked": "locked"},
                ExpressionAttributeValues={":locked": locked, ":by": by, ":ts": now()},
                ReturnValues="ALL_NEW",
            )
        except self.t.meta.client.exceptions.ConditionalCheckFailedException:
            raise HttpError(404, "That student has not opened this lab this semester.")
        return res["Attributes"]

    # -- helpers -----------------------------------------------------------

    def _query(self, condition: str, values: dict, index: str | None = None) -> list[dict]:
        kwargs = {"KeyConditionExpression": condition, "ExpressionAttributeValues": values}
        if index:
            kwargs["IndexName"] = index
        items: list[dict] = []
        while True:
            page = self.t.query(**kwargs)
            items.extend(page.get("Items", []))
            if "LastEvaluatedKey" not in page:
                return items
            kwargs["ExclusiveStartKey"] = page["LastEvaluatedKey"]


_store: Store | None = None


def default_store() -> Store:
    global _store
    if _store is None:
        import boto3  # imported here so the unit tests run without it

        _store = Store(
            boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"]),
            Accounts(boto3.client("cognito-idp"), os.environ["USER_POOL_ID"]),
        )
    return _store


# -- request handling --------------------------------------------------------

def caller(event: dict, store: Store) -> dict:
    claims = (
        event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
    )
    address = (claims.get("email") or "").strip().lower()
    verified = str(claims.get("email_verified", "")).lower() == "true"
    # The authorizer accepts access tokens too, and those carry no email.
    if not claims.get("sub") or not address or claims.get("token_use") != "id":
        raise HttpError(401, "Please sign in again.")
    if not verified:
        raise HttpError(403, "Please verify your email address first.")
    uid = canonical(address)
    is_owner = uid in owners()
    return {
        "id": uid,
        "email": uid,
        "address": address,
        "owner": is_owner,
        "admin": is_owner or store.is_listed_admin(uid),
    }


def parse_body(event: dict) -> dict:
    raw = event.get("body")
    if not raw:
        return {}
    if len(raw) > MAX_BODY_BYTES:
        raise HttpError(413, "That is more than a lab can save.")
    if event.get("isBase64Encoded"):
        raw = base64.b64decode(raw).decode("utf-8")
    try:
        body = json.loads(raw)
    except ValueError:
        raise HttpError(400, "The request was not valid JSON.")
    if not isinstance(body, dict):
        raise HttpError(400, "The request must be a JSON object.")
    return body


def current_term(store: Store) -> str:
    return store.term_choice() or term_for(today())


def term_param(store: Store, params: dict) -> str:
    """The term an admin asked for with ?term=, or the current one."""
    wanted = (params.get("query") or {}).get("term")
    return check_term(wanted) if wanted else current_term(store)


def lab_param(params: dict) -> str:
    lab = params.get("lab", "")
    if not LAB_ID.match(lab):
        raise HttpError(400, "Unknown lab.")
    return lab


def flag(body: dict, name: str) -> bool:
    value = body.get(name)
    if not isinstance(value, bool):
        raise HttpError(400, f"'{name}' must be true or false.")
    return value


def require_admin(user: dict) -> None:
    if not user["admin"]:
        raise HttpError(403, "This needs instructor access.")


def require_owner(user: dict, what: str = "change who the admins are") -> None:
    if not user["owner"]:
        raise HttpError(403, f"Only a course owner can {what}.")


def load_state(item: dict | None) -> dict:
    if not item or not item.get("state"):
        return {}
    try:
        return json.loads(item["state"])
    except ValueError:
        return {}


def student_row(item: dict) -> dict:
    return {
        "id": item["PK"].split("#", 1)[1],
        "email": item.get("email"),
        "state": load_state(item),
        "submitted": bool(item.get("submitted")),
        "submittedAt": item.get("submittedAt"),
        "submissions": item.get("submissions", 0),
        "updatedAt": item.get("updatedAt"),
        "createdAt": item.get("createdAt"),
        "saves": item.get("saves", 0),
        "locked": bool(item.get("locked")),
        "lockedBy": item.get("lockedBy"),
    }


# -- routes: students ----------------------------------------------------------

def get_me(store, user, params, body):
    term = current_term(store)
    return {"email": user["email"], "address": user["address"],
            "admin": user["admin"], "owner": user["owner"],
            "term": term, "termLabel": term_label(term)}


def get_progress(store, user, params, body):
    lab = lab_param(params)
    term = current_term(store)
    item = store.progress(user["id"], term, lab)
    lab_locked = bool(store.lab_settings(term, lab).get("locked"))
    student_locked = bool(item and item.get("locked"))
    return {
        "lab": lab,
        "term": term,
        "termLabel": term_label(term),
        "state": load_state(item),
        "submitted": bool(item and item.get("submitted")),
        "submittedAt": item.get("submittedAt") if item else None,
        "updatedAt": item.get("updatedAt") if item else None,
        # Admins are never locked out, but they are told when students are.
        "locked": (lab_locked or student_locked) and not user["admin"],
        "labLocked": lab_locked,
        "studentLocked": student_locked,
        "admin": user["admin"],
    }


def put_progress(store, user, params, body):
    lab = lab_param(params)
    term = current_term(store)
    state = body.get("state")
    if not isinstance(state, dict):
        raise HttpError(400, "'state' must be an object.")
    submit = body.get("submit", False)
    if not isinstance(submit, bool):
        raise HttpError(400, "'submit' must be true or false.")
    state_json = json.dumps(state, separators=(",", ":"), sort_keys=True)
    if len(state_json.encode("utf-8")) > MAX_STATE_BYTES:
        raise HttpError(413, "That is more than a lab can save.")

    if not user["admin"] and store.lab_settings(term, lab).get("locked"):
        raise HttpError(423, "An instructor has locked this lab.")

    item = store.save_progress(
        user["id"], user["email"], term, lab, state_json, submit, force=user["admin"]
    )
    return {
        "lab": lab,
        "term": term,
        "updatedAt": item.get("updatedAt"),
        "submitted": bool(item.get("submitted")),
        "submittedAt": item.get("submittedAt"),
        "saves": item.get("saves", 0),
    }


# -- routes: labs and terms ----------------------------------------------------

def admin_terms(store, user, params, body):
    require_admin(user)
    chosen = store.term_choice()
    automatic = term_for(today())
    current = chosen or automatic
    ids = set(store.terms_with_work()) | {current, automatic, next_term(automatic)}
    ids = sorted(ids, key=term_order, reverse=True)
    return {
        "current": current,
        "automatic": automatic,
        "chosen": chosen,
        "terms": [{"id": t, "label": term_label(t)} for t in ids],
    }


def admin_set_term(store, user, params, body):
    require_owner(user, "choose the semester")
    term = body.get("term")
    if term is not None:
        check_term(term)
    store.set_term_choice(term, user["email"])
    log.info("%s set the semester to %s", user["email"], term or "automatic")
    return admin_terms(store, user, params, body)


def admin_labs(store, user, params, body):
    require_admin(user)
    term = term_param(store, params)
    return {"term": term, "labs": [
        {"lab": s.get("lab"), "locked": bool(s.get("locked")),
         "lockedBy": s.get("lockedBy"), "lockedAt": s.get("lockedAt")}
        for s in store.all_lab_settings(term)
    ]}


def admin_lab_progress(store, user, params, body):
    require_admin(user)
    lab = lab_param(params)
    term = term_param(store, params)
    settings = store.lab_settings(term, lab)
    rows = sorted((student_row(i) for i in store.lab_progress(term, lab)),
                  key=lambda r: r["email"] or "")
    return {"lab": lab, "term": term, "locked": bool(settings.get("locked")),
            "students": rows}


def admin_lock_lab(store, user, params, body):
    require_admin(user)
    lab = lab_param(params)
    term = term_param(store, params)
    item = store.set_lab_lock(term, lab, flag(body, "locked"), user["email"])
    return {"lab": lab, "term": term, "locked": item["locked"],
            "lockedBy": item["lockedBy"], "lockedAt": item["lockedAt"]}


def admin_lock_student(store, user, params, body):
    require_admin(user)
    lab = lab_param(params)
    term = term_param(store, params)
    uid = canonical(unquote(params.get("student") or ""))
    if not EMAIL.match(uid):
        raise HttpError(400, "Unknown student.")
    item = store.set_student_lock(uid, term, lab, flag(body, "locked"), user["email"])
    return student_row(item)


# -- routes: admins -------------------------------------------------------------

def admin_list_admins(store, user, params, body):
    require_admin(user)
    listed = [{"email": a["email"], "owner": False, "addedBy": a.get("addedBy"),
               "addedAt": a.get("addedAt")} for a in store.list_admins()]
    fixed = [{"email": e, "owner": True, "addedBy": None, "addedAt": None}
             for e in sorted(owners())]
    return {"admins": fixed + sorted(listed, key=lambda a: a["email"])}


def admin_add_admin(store, user, params, body):
    require_owner(user)
    email = canonical(body["email"]) if isinstance(body.get("email"), str) else ""
    if not EMAIL.match(email):
        raise HttpError(400, "That does not look like an email address.")
    if email in owners():
        raise HttpError(400, "That person is already an owner.")
    store.add_admin(email, user["email"])
    return {"email": email, "owner": False, "addedBy": user["email"]}


def admin_remove_admin(store, user, params, body):
    require_owner(user)
    email = canonical(unquote(params.get("email") or ""))
    if email in owners():
        raise HttpError(400, "Owners are set when the backend is deployed, not here.")
    if not EMAIL.match(email):
        raise HttpError(400, "That does not look like an email address.")
    store.remove_admin(email)
    return {"email": email, "removed": True}


# -- routes: accounts -----------------------------------------------------------

def is_staff(store, uid: str) -> bool:
    return uid in owners() or store.is_listed_admin(uid)


def pending_account(store, user, username: str) -> str:
    """Check an account can be approved by this admin; return its id."""
    uid = canonical(username)
    if not EMAIL.match(uid) or uid != (username or "").strip().lower():
        raise HttpError(400, "Unknown account.")
    status = store.accounts.status(uid)
    if status is None:
        raise HttpError(404, "There is no such account.")
    if status != "UNCONFIRMED":
        raise HttpError(409, "That account is already confirmed.")
    if is_staff(store, uid) and not user["owner"]:
        raise HttpError(403, "Only a course owner can confirm or remove an owner or admin account.")
    return uid


def admin_accounts(store, user, params, body):
    require_admin(user)
    profiles = store.profiles()
    rows = []
    for a in store.accounts.everyone():
        uid = canonical(a["username"])
        last = profiles.get(uid, {}).get("lastTerm")
        rows.append({
            **a,
            "approved": a["status"] != "UNCONFIRMED",
            "staff": is_staff(store, uid),
            "you": uid == user["id"],
            "lastTerm": last,
            "lastTermLabel": term_label(last) if last else None,
        })
    # Waiting first, then newest first.
    rows.sort(key=lambda a: a["createdAt"] or "", reverse=True)
    rows.sort(key=lambda a: a["approved"])
    return {"accounts": rows}


def admin_confirm_accounts(store, user, params, body):
    require_admin(user)
    names = body.get("usernames")
    if (not isinstance(names, list) or not 1 <= len(names) <= 100
            or not all(isinstance(n, str) for n in names)):
        raise HttpError(400, "'usernames' must be a list of 1 to 100 accounts.")
    results = []
    for name in dict.fromkeys(names):
        try:
            uid = pending_account(store, user, name)
            store.accounts.confirm(uid)
            results.append({"username": name, "confirmed": True})
        except HttpError as err:
            results.append({"username": name, "confirmed": False, "error": err.message})
    log.info("%s confirmed %s", user["email"],
             [r["username"] for r in results if r["confirmed"]])
    return {"results": results}


def account_param(params: dict) -> str:
    raw = unquote(params.get("username") or "")
    uid = canonical(raw)
    if not EMAIL.match(uid):
        raise HttpError(400, "That does not look like an email address.")
    return uid


def admin_remove_account(store, user, params, body):
    require_admin(user)
    uid = account_param(params)
    if uid == user["id"]:
        raise HttpError(400, "You cannot remove your own account.")
    if store.accounts.status(uid) is None:
        raise HttpError(404, "There is no such account.")
    if is_staff(store, uid) and not user["owner"]:
        raise HttpError(403, "Only a course owner can remove an owner or admin account.")
    store.accounts.remove(uid)
    log.info("%s deleted the account %s", user["email"], uid)   # saved work is kept
    return {"username": uid, "removed": True}


def admin_clear_old_accounts(store, user, params, body):
    """Delete student accounts with no work since `before`. Their work is kept."""
    require_owner(user, "clear out old accounts")
    before = check_term(body.get("before"))
    dry_run = body.get("dryRun", True)
    if not isinstance(dry_run, bool):
        raise HttpError(400, "'dryRun' must be true or false.")
    profiles = store.profiles()
    starts = term_start(before)
    chosen = []
    for a in store.accounts.everyone():
        uid = canonical(a["username"])
        if uid == user["id"] or is_staff(store, uid):
            continue
        last = profiles.get(uid, {}).get("lastTerm")
        if last:
            old = term_order(last) < term_order(before)
        else:
            # Never saved anything: go by when the account was made.
            old = (a["createdAt"] or "")[:10] < starts
        if old:
            chosen.append(uid)
    if not dry_run:
        for uid in chosen:
            store.accounts.remove(uid)
        log.info("%s cleared %d accounts inactive before %s", user["email"], len(chosen), before)
    return {"before": before, "dryRun": dry_run, "accounts": chosen}


ROUTES = {
    "GET /me": get_me,
    "GET /labs/{lab}/progress": get_progress,
    "PUT /labs/{lab}/progress": put_progress,
    "GET /admin/terms": admin_terms,
    "PUT /admin/terms/current": admin_set_term,
    "GET /admin/labs": admin_labs,
    "GET /admin/labs/{lab}/progress": admin_lab_progress,
    "PUT /admin/labs/{lab}/lock": admin_lock_lab,
    "PUT /admin/labs/{lab}/students/{student}/lock": admin_lock_student,
    "GET /admin/admins": admin_list_admins,
    "POST /admin/admins": admin_add_admin,
    "DELETE /admin/admins/{email}": admin_remove_admin,
    "GET /admin/accounts": admin_accounts,
    "POST /admin/accounts/confirm": admin_confirm_accounts,
    "POST /admin/accounts/clear-old": admin_clear_old_accounts,
    "DELETE /admin/accounts/{username}": admin_remove_account,
}


def _json_default(value):
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    raise TypeError(f"cannot serialise {type(value).__name__}")


def respond(status: int, payload: dict) -> dict:
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json", "Cache-Control": "no-store"},
        "body": json.dumps(payload, default=_json_default),
    }


def handler(event, context, store: Store | None = None):
    try:
        store = store or default_store()
        route = ROUTES.get(event.get("routeKey", ""))
        if route is None:
            raise HttpError(404, "Not found.")
        user = caller(event, store)
        params = dict(event.get("pathParameters") or {})
        params["query"] = event.get("queryStringParameters") or {}
        return respond(200, route(store, user, params, parse_body(event)))
    except HttpError as err:
        return respond(err.status, {"error": err.message})
    except Exception:
        log.exception("unhandled error on %s", event.get("routeKey"))
        return respond(500, {"error": "Something went wrong on our side. Please try again."})
