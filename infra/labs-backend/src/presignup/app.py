"""Cognito pre sign-up check: only university addresses, owners, and added admins.

Admins can have addresses outside the university (a visiting TA, say), so the
admin list in the table is checked as well. Accounts made by an AWS operator
with admin-create-user skip the check, which is how test accounts are made.

The username has to be the address with university aliases folded together,
which the sign-in page does, so x@missouri.edu and x@umsystem.edu can never
become two accounts for one mailbox.
"""

from __future__ import annotations

import os

_table = None


def allowed_domains() -> set[str]:
    raw = os.environ.get("ALLOWED_DOMAINS", "")
    return {d.strip().lower() for d in raw.split(",") if d.strip()}


def alias_domains() -> list[str]:
    raw = os.environ.get("ALIAS_DOMAINS", "umsystem.edu,missouri.edu,mail.missouri.edu")
    return [d.strip().lower() for d in raw.split(",") if d.strip()]


def canonical(email: str) -> str:
    """Kept identical to canonical() in the API."""
    email = (email or "").strip().lower()
    local, at, domain = email.rpartition("@")
    domains = alias_domains()
    if at and local and domain in domains:
        return f"{local}@{domains[0]}"
    return email


def owners() -> set[str]:
    raw = os.environ.get("OWNER_EMAILS", "")
    return {canonical(e) for e in raw.split(",") if e.strip()}


def listed_admin(email: str) -> bool:
    global _table
    if _table is None:
        import boto3

        _table = boto3.resource("dynamodb").Table(os.environ["TABLE_NAME"])
    res = _table.get_item(Key={"PK": "CONFIG", "SK": f"ADMIN#{email}"},
                          ProjectionExpression="PK")
    return "Item" in res


def handler(event, context):
    if event.get("triggerSource") == "PreSignUp_AdminCreateUser":
        return event

    email = (event["request"]["userAttributes"].get("email") or "").strip().lower()
    uid = canonical(email)
    if (event.get("userName") or "").strip().lower() != uid:
        raise Exception("Please create your account from a lab page")

    domain = email.rpartition("@")[2]
    if domain in allowed_domains() or uid in owners() or listed_admin(uid):
        return event

    # Cognito shows this text to the person signing up, after its own prefix.
    raise Exception("Please sign up with your University of Missouri email address")
