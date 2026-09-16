"""End-to-end check against a deployed stack, then clean up after itself.

    python infra/labs-backend/tests/smoke_test.py test          # uses AWS profile "bhanu"
    AWS_PROFILE=other python infra/labs-backend/tests/smoke_test.py test

Creates two throwaway accounts at example.com (Cognito sends no email for
operator-created accounts), makes one of them an admin by writing the admin
record directly, and exercises sign-in, saving, submitting, and both kinds of
lock through the real API. Owner-only routes are covered by the unit tests,
because the owners are real people whose accounts this should not touch.
"""

from __future__ import annotations

import json
import os
import secrets
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

STAGE = sys.argv[1] if len(sys.argv) > 1 else "test"
PROFILE = os.environ.get("AWS_PROFILE", "bhanu")
REGION = os.environ.get("AWS_REGION", "us-east-1")
STACK = f"csc-ee-8001-labs-{STAGE}"
LAB = "smoke_test"


def aws(*args: str) -> dict:
    out = subprocess.run(
        ["aws", "--profile", PROFILE, "--region", REGION, "--output", "json", *args],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out) if out.strip() else {}


def outputs() -> dict:
    stack = aws("cloudformation", "describe-stacks", "--stack-name", STACK)["Stacks"][0]
    return {o["OutputKey"]: o["OutputValue"] for o in stack["Outputs"]}


def http(method: str, url: str, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    if data is not None:
        req.add_header("Content-Type", req.headers.get("Content-type", "application/json"))
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return res.status, json.loads(res.read() or b"{}")
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read() or b"{}")


def main() -> int:
    out = outputs()
    api, pool, client = out["ApiUrl"], out["UserPoolId"], out["UserPoolClientId"]
    table = out["TableName"]
    tag = secrets.token_hex(3)
    people = {
        "student": f"smoke-student-{tag}@example.com",
        "admin": f"smoke-admin-{tag}@example.com",
    }
    # A university account stored the way the sign-in page makes it: the username
    # is the umsystem.edu spelling, the email attribute is what the person typed.
    # admin-create-user with SUPPRESS sends nothing, so no real inbox is touched.
    alias_user = f"smoke-alias-{tag}@umsystem.edu"
    alias_typed = f"smoke-alias-{tag}@missouri.edu"
    # Accounts left waiting for a code. example.com accepts no mail, so the codes
    # Cognito sends for these go nowhere. They are briefly listed as admins only so
    # the sign-up check lets a non-university address through.
    waiting = [f"smoke-wait-{tag}-{n}@example.com" for n in (1, 2)]
    password = "Smoke-" + secrets.token_urlsafe(12) + "1a"
    failures: list[str] = []

    def check(label, got, want):
        ok = got == want
        print(f"  {'ok  ' if ok else 'FAIL'} {label}: {got!r}" + ("" if ok else f" (wanted {want!r})"))
        if not ok:
            failures.append(label)

    def sign_in(email):
        status, data = http(
            "POST", f"https://cognito-idp.{REGION}.amazonaws.com/",
            {"AuthFlow": "USER_PASSWORD_AUTH", "ClientId": client,
             "AuthParameters": {"USERNAME": email, "PASSWORD": password}},
            {"Content-Type": "application/x-amz-json-1.1",
             "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"},
        )
        assert status == 200, data
        return data["AuthenticationResult"]["IdToken"]

    def call(who, method, path, body=None, token=None):
        return http(method, api + path, body, {"Authorization": token or tokens[who]})

    try:
        print(f"stack {STACK}: creating throwaway accounts")
        for role, email in people.items():
            aws("cognito-idp", "admin-create-user", "--user-pool-id", pool,
                "--username", email, "--message-action", "SUPPRESS",
                "--user-attributes", f"Name=email,Value={email}",
                "Name=email_verified,Value=true")
            aws("cognito-idp", "admin-set-user-password", "--user-pool-id", pool,
                "--username", email, "--password", password, "--permanent")
        aws("cognito-idp", "admin-create-user", "--user-pool-id", pool,
            "--username", alias_user, "--message-action", "SUPPRESS",
            "--user-attributes", f"Name=email,Value={alias_typed}",
            "Name=email_verified,Value=true")
        aws("cognito-idp", "admin-set-user-password", "--user-pool-id", pool,
            "--username", alias_user, "--password", password, "--permanent")
        aws("dynamodb", "put-item", "--table-name", table, "--item", json.dumps({
            "PK": {"S": "CONFIG"}, "SK": {"S": f"ADMIN#{people['admin']}"},
            "email": {"S": people["admin"]}, "addedBy": {"S": "smoke-test"},
        }))
        tokens = {role: sign_in(email) for role, email in people.items()}

        print("identity")
        check("no token", http("GET", api + "/me")[0], 401)
        check("student /me admin", call("student", "GET", "/me")[1].get("admin"), False)
        check("admin /me admin", call("admin", "GET", "/me")[1].get("admin"), True)
        check("admin /me owner", call("admin", "GET", "/me")[1].get("owner"), False)

        print("saving")
        check("empty progress", call("student", "GET", f"/labs/{LAB}/progress")[1].get("state"), {})
        check("save", call("student", "PUT", f"/labs/{LAB}/progress",
                           {"state": {"q1": "b", "size": 3.5}})[0], 200)
        check("restored", call("student", "GET", f"/labs/{LAB}/progress")[1].get("state"),
              {"q1": "b", "size": 3.5})
        status, body = call("student", "PUT", f"/labs/{LAB}/progress",
                            {"state": {"q1": "c"}, "submit": True})
        check("submit", (status, body.get("submitted")), (200, True))
        check("student blocked from admin", call("student", "GET", f"/admin/labs/{LAB}/progress")[0], 403)

        print("admin view")
        status, body = call("admin", "GET", f"/admin/labs/{LAB}/progress")
        rows = {r["email"]: r for r in body.get("students", [])}
        check("admin sees student", people["student"] in rows, True)
        check("student row submitted", rows.get(people["student"], {}).get("submitted"), True)
        check("admin cannot add admins", call("admin", "POST", "/admin/admins",
                                              {"email": "x@example.com"})[0], 403)

        print("locking")
        check("lock lab", call("admin", "PUT", f"/admin/labs/{LAB}/lock", {"locked": True})[0], 200)
        check("student save refused", call("student", "PUT", f"/labs/{LAB}/progress",
                                           {"state": {"q1": "d"}})[0], 423)
        check("student sees lock", call("student", "GET", f"/labs/{LAB}/progress")[1].get("locked"), True)
        check("admin still saves", call("admin", "PUT", f"/labs/{LAB}/progress",
                                        {"state": {"x": 1}})[0], 200)
        check("lab in list", any(l["lab"] == LAB and l["locked"] for l in
                                 call("admin", "GET", "/admin/labs")[1].get("labs", [])), True)
        check("unlock lab", call("admin", "PUT", f"/admin/labs/{LAB}/lock", {"locked": False})[0], 200)
        check("student saves again", call("student", "PUT", f"/labs/{LAB}/progress",
                                          {"state": {"q1": "d"}})[0], 200)
        student_path = urllib.parse.quote(people["student"])
        check("lock student", call("admin", "PUT",
                                   f"/admin/labs/{LAB}/students/{student_path}/lock",
                                   {"locked": True})[0], 200)
        check("locked student refused", call("student", "PUT", f"/labs/{LAB}/progress",
                                             {"state": {"q1": "e"}})[0], 423)
        check("unlock student", call("admin", "PUT",
                                     f"/admin/labs/{LAB}/students/{student_path}/lock",
                                     {"locked": False})[0], 200)
        check("final state", call("student", "GET", f"/labs/{LAB}/progress")[1].get("state"),
              {"q1": "d"})

        print("university aliases")
        alias_token = sign_in(alias_user)
        status, body = http("GET", api + "/me", headers={"Authorization": alias_token})
        check("alias id", body.get("email"), alias_user)
        check("alias address", body.get("address"), alias_typed)
        check("alias saves under one id", http(
            "PUT", api + f"/labs/{LAB}/progress", {"state": {"a": 1}},
            {"Authorization": alias_token})[0], 200)
        status, body = http(
            "POST", f"https://cognito-idp.{REGION}.amazonaws.com/",
            {"ClientId": client, "Username": "not-the-address", "Password": password,
             "UserAttributes": [{"Name": "email", "Value": f"nobody-{tag}@gmail.com"}]},
            {"Content-Type": "application/x-amz-json-1.1",
             "X-Amz-Target": "AWSCognitoIdentityProviderService.SignUp"},
        )
        check("sign-up must use the folded address",
              (status, "lab page" in body.get("message", "")), (400, True))

        print("accounts waiting for a code")
        for email in waiting:
            aws("dynamodb", "put-item", "--table-name", table, "--item", json.dumps({
                "PK": {"S": "CONFIG"}, "SK": {"S": f"ADMIN#{email}"}, "email": {"S": email}}))
            status, body = http(
                "POST", f"https://cognito-idp.{REGION}.amazonaws.com/",
                {"ClientId": client, "Username": email, "Password": password,
                 "UserAttributes": [{"Name": "email", "Value": email}]},
                {"Content-Type": "application/x-amz-json-1.1",
                 "X-Amz-Target": "AWSCognitoIdentityProviderService.SignUp"},
            )
            check(f"sign up {email.split('@')[0][-1]}", status, 200)
            aws("dynamodb", "delete-item", "--table-name", table, "--key", json.dumps({
                "PK": {"S": "CONFIG"}, "SK": {"S": f"ADMIN#{email}"}}))
        status, body = call("admin", "GET", "/admin/accounts/pending")
        listed = {a["username"] for a in body.get("accounts", [])}
        check("pending listed", set(waiting) <= listed, True)
        check("student cannot list", call("student", "GET", "/admin/accounts/pending")[0], 403)
        status, body = call("admin", "POST", "/admin/accounts/confirm", {"usernames": [waiting[0]]})
        check("confirm", body.get("results", [{}])[0].get("confirmed"), True)
        check("confirmed can sign in", bool(sign_in(waiting[0])), True)
        check("remove", call("admin", "DELETE",
                             "/admin/accounts/" + urllib.parse.quote(waiting[1]))[0], 200)
        check("removed is gone", call("admin", "DELETE",
                                      "/admin/accounts/" + urllib.parse.quote(waiting[1]))[0], 404)

        print("password reset by an admin")
        status, body = call("admin", "POST", "/admin/accounts/reset-password",
                            {"email": people["student"]})
        check("reset", status, 200)
        temp = body.get("temporaryPassword", "")
        status, data = http(
            "POST", f"https://cognito-idp.{REGION}.amazonaws.com/",
            {"AuthFlow": "USER_PASSWORD_AUTH", "ClientId": client,
             "AuthParameters": {"USERNAME": people["student"], "PASSWORD": temp}},
            {"Content-Type": "application/x-amz-json-1.1",
             "X-Amz-Target": "AWSCognitoIdentityProviderService.InitiateAuth"},
        )
        check("temporary password asks for a new one", data.get("ChallengeName"),
              "NEW_PASSWORD_REQUIRED")
        new_password = password + "x"
        status, data = http(
            "POST", f"https://cognito-idp.{REGION}.amazonaws.com/",
            {"ChallengeName": "NEW_PASSWORD_REQUIRED", "ClientId": client,
             "Session": data.get("Session"),
             "ChallengeResponses": {"USERNAME": people["student"], "NEW_PASSWORD": new_password}},
            {"Content-Type": "application/x-amz-json-1.1",
             "X-Amz-Target": "AWSCognitoIdentityProviderService.RespondToAuthChallenge"},
        )
        check("new password accepted", "AuthenticationResult" in data, True)

        print("CORS")
        req = urllib.request.Request(api + f"/labs/{LAB}/progress", method="OPTIONS", headers={
            "Origin": "https://radiant-systems-lab.github.io",
            "Access-Control-Request-Method": "PUT",
            "Access-Control-Request-Headers": "authorization,content-type",
        })
        with urllib.request.urlopen(req, timeout=20) as res:
            check("preflight origin", res.headers.get("access-control-allow-origin"),
                  "https://radiant-systems-lab.github.io")
    finally:
        print("cleaning up")
        for email in [*people.values(), alias_user, *waiting]:
            try:
                aws("cognito-idp", "admin-delete-user", "--user-pool-id", pool, "--username", email)
            except subprocess.CalledProcessError:
                pass
        keys = [("CONFIG", f"ADMIN#{people['admin']}"), (f"LAB#{LAB}", "SETTINGS"),
                *[("CONFIG", f"ADMIN#{w}") for w in waiting]]
        for email in [*people.values(), alias_user]:
            found = aws("dynamodb", "query", "--table-name", table,
                        "--key-condition-expression", "PK = :pk",
                        "--expression-attribute-values", json.dumps({":pk": {"S": f"USER#{email}"}}),
                        "--projection-expression", "PK, SK")
            keys += [(i["PK"]["S"], i["SK"]["S"]) for i in found.get("Items", [])]
        for pk, sk in keys:
            aws("dynamodb", "delete-item", "--table-name", table,
                "--key", json.dumps({"PK": {"S": pk}, "SK": {"S": sk}}))
        print(f"  removed the test accounts and {len(keys)} records")

    print("PASSED" if not failures else f"FAILED: {', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
