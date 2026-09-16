# Class lab backend

Sign-in and progress storage for the CSC/EE 8001 class labs. The website stays on
GitHub Pages; only this backend runs on AWS.

```
browser (labs/gate/gate.js)
  |-- sign up, sign in, reset password --> Amazon Cognito user pool
  |                                          '-- pre sign-up Lambda: university emails only
  '-- save and load answers (ID token) --> API Gateway (HTTP API, JWT check)
                                             '-- Lambda (src/api/app.py) --> DynamoDB
```

Everything is in `template.yaml`. Nothing here is secret: the API address and the
Cognito client id end up in `labs/gate/config.js` for every browser to read.

## Who can do what

| Role | How someone gets it | Can |
| - | - | - |
| Student | Signs up with an address at an allowed domain | Save and submit their own answers |
| Admin | An owner adds their email on the dashboard | See everyone's answers, lock labs and students |
| Owner | Listed in `OWNERS` when deploying | Everything an admin can, plus add and remove admins |

Allowed domains default to `umsystem.edu`, `missouri.edu` and `mail.missouri.edu`.
An admin can sign up with any address once an owner has added it.

## One person, three spellings

`x@missouri.edu`, `x@mail.missouri.edu` and `x@umsystem.edu` reach the same inbox,
so they are treated as one person everywhere:

- The sign-in page turns any of them into `x@umsystem.edu` and uses that as the
  Cognito username. Whichever spelling a student types, they reach the same
  account and the same password.
- The account's email is left as typed, so verification and reset codes go to
  the spelling the student signed up with.
- Saved answers, owners and admins are all stored under the `umsystem.edu`
  spelling, so adding `ta@missouri.edu` as an admin also covers `ta@umsystem.edu`.
- The sign-up check refuses any account whose username is not the folded
  address, so a second account for the same inbox cannot be made by calling
  Cognito directly.

This assumes the part before the `@` means the same person on all three domains,
which is how university accounts work. The list is the `AliasDomains` parameter.

## Semesters

Answers, submissions and locks are kept per semester. The current semester
follows the date (January to May is spring, June and July summer, August to
December fall); an owner can pin a different one on the dashboard. A student who
takes the course again later starts fresh, and earlier work stays viewable by
picking that semester on the dashboard. Accounts are not per semester: the
dashboard shows when each person was last active, and an owner can delete
accounts not used since a chosen semester (their work is kept).

## Locking

A locked lab, or a lab locked for one student, is not shown to students at all:
the sign-in screen stays up with "This lab is locked", and saving is refused.
Owners and admins still open it. The lab pages themselves are public files on
GitHub Pages, so this stops everyone using the site normally; someone who loads
the raw page with browser tools could still read it, but could not save.

## Deploying

Needs the AWS CLI and a signed-in profile.

```bash
aws sso login --profile bhanu
infra/labs-backend/deploy.sh test     # the stack for trying things out
infra/labs-backend/deploy.sh prod     # the real one
```

The script packages the Lambda code, deploys the stack
`csc-ee-8001-labs-<stage>`, and rewrites `labs/gate/config.js` to point at it.
After a deploy, rebuild the labs so their pages pick up the new config:

```bash
labs/.venv/Scripts/python labs/build_labs.py
```

Defaults can be overridden:

```bash
OWNERS="a@missouri.edu,b@umsystem.edu" AWS_PROFILE=other infra/labs-backend/deploy.sh prod
```

`prod` keeps the user pool and the table if the stack is deleted, and turns on
deletion protection for both. `test` deletes them with the stack.

To remove the test stack entirely:

```bash
aws cloudformation delete-stack --stack-name csc-ee-8001-labs-test --profile bhanu
```

## Tests

```bash
cd infra/labs-backend
python -m unittest discover -s tests          # no AWS needed
python tests/smoke_test.py test               # against the deployed test stack
```

The smoke test makes two throwaway accounts at example.com, checks saving,
submitting, admin access and both kinds of lock through the real API, then
deletes everything it created.

## What it costs

For a class of about 100 students, expect well under $2 a month. Most of it sits
inside AWS's free allowances.

| Service | Used for | Expected cost |
| - | - | - |
| Cognito, Lite tier | accounts and sign-in | free under 10,000 monthly active users |
| API Gateway, HTTP API | saves and loads | about $1 per million requests |
| Lambda | the API | inside the always-free tier |
| DynamoDB, on demand | answers and settings | cents, since the data is kilobytes |
| CloudWatch Logs | 30 days of logs | inside the free 5 GB |
| S3 | build artifacts, deleted after 30 days | cents |

Throttling is set to 25 requests a second with bursts of 50, which caps what a
misbehaving script could cost.

## Things to know

- **No emails.** Cognito's built-in sender (`no-reply@verificationemail.com`) is
  held by university mail filters, so the sign-in page never asks for emailed
  codes. New accounts wait under "Student accounts" on the dashboard until an
  admin approves them. For a typo or a forgotten password, the admin deletes the
  account and the student creates it again, then the admin approves it. Saved
  work is stored by email address, not by account, so it is kept. Only an owner
  can approve or delete an owner's or admin's account. To bring emailed codes
  back once delivery works (for example through Amazon SES with your own domain),
  add `emailCodes: true` to `labs/gate/config.js`.
- **Data.** Student answers tied to names are education records under FERPA.
  Check that this AWS account is approved for them before using it with a class.
- **Viewing.** The labs are static files on GitHub Pages. The sign-in screen stops
  casual viewing, but a determined student could load a lab without it. They
  could not save anything, because the API checks every request.
- **Stored data.** Each student has one record per lab with their latest answers,
  plus a copy of every submission. Point-in-time recovery is on, so the table can
  be restored to any second in the last 35 days.
