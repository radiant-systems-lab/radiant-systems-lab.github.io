# CSC/EE 8001 Labs

Interactive labs for *Designing End-to-End ML Systems*. Each lab is a
[marimo](https://marimo.io) notebook exported to WebAssembly, so it runs entirely in
the student's browser. There is nothing to install, no kernel, and no server.

## Layout

```
labs/
  _src/<slug>/notebook.py   source you edit          (not published - "_" prefix)
  _src/lab_template.py      starting point for a new lab, with saving wired in
  <slug>/index.html         generated bundle          (published, committed)
  runtime/                  shared marimo frontend    (published, committed)
  gate/                     sign-in screen and its config (published, committed)
  admin/                    instructor dashboard      (published, committed)
  build_labs.py             build script              (not published)
  .venv/                    build toolchain           (gitignored)
```

`labs/runtime/` holds the marimo frontend (~26 MB) **once**, shared by every lab.
marimo normally emits that payload next to each notebook; the build hoists it and
rewrites each lab's references to `../runtime/`. Sixteen labs therefore cost about
27 MB in total rather than about 420 MB.

Lab metadata (title, number, due date, status, summary, objectives) lives in
`_data/labs.yml`, not in the notebook. The course page renders it through
`_includes/lab_card.html`, and the build reads it to set each bundle's `<title>`
and `<meta name="description">`.

## One-time setup

```bash
python -m venv labs/.venv
labs/.venv/Scripts/python -m pip install marimo uv    # Windows
labs/.venv/bin/python     -m pip install marimo uv    # macOS / Linux
```

`uv` is required: marimo shells out to it to resolve a notebook's imports during a
WASM export, and looks it up on `PATH`.

## Authoring a lab

```bash
labs/.venv/Scripts/python -m marimo edit labs/_src/week_01/notebook.py
```

This opens marimo's editor in a browser with live reactive execution, which is the fastest
way to iterate. Keep to packages [Pyodide ships](https://pyodide.org/en/stable/usage/packages-in-pyodide.html);
anything else needs a `micropip` install at notebook start, which slows the first load
for students on slow connections. Week 1 deliberately uses only `numpy` and `math`.

## Building

```bash
labs/.venv/Scripts/python labs/build_labs.py                 # every lab
labs/.venv/Scripts/python labs/build_labs.py week_01    # just one
labs/.venv/Scripts/python labs/build_labs.py --check         # CI: bundles current?
```

Generated bundles are committed, because GitHub Pages cannot run this build. Always
rebuild **every** lab after upgrading marimo, so the shared runtime stays consistent. The
build stops with a `runtime conflict` error if two labs disagree.

## Adding a lab

1. Add a record to `_data/labs.yml` with `status: coming-soon`.
2. Copy `labs/_src/lab_template.py` to `labs/_src/<slug>/notebook.py` and write the lab.
   The comment at the top of the template explains how to make each answer save.
3. Build it, then flip `status` to `available`.

The card and the course page pick it up automatically; no HTML to edit.

## Sign-in and saving

Every lab asks students to sign in with their university email before it opens,
and saves their answers as they go. A returning student sees their answers again,
on any computer. Instructors see everything at `/labs/admin/`.

How the pieces fit:

- `gate/gate.js` covers the lab with a sign-in screen, talks to Amazon Cognito, and
  calls the progress API. The build adds it to any notebook that contains the
  `"radiant-lab-"` channel name, which is how the saving cell identifies itself.
- The notebook runs in a web worker, so it cannot see the page. The gate gives each
  tab a random `rl` query parameter before marimo starts, and the notebook uses it
  to open a private `BroadcastChannel` to the gate. Tokens never reach Python.
- `gate/config.js` holds the API address and Cognito client id. Both are public by
  design. `infra/labs-backend/deploy.sh` writes this file; do not edit it by hand.
- The backend (Cognito, API Gateway, Lambda, DynamoDB) lives in
  `infra/labs-backend/`. Its README covers deploying, costs, and tests.

Students can type `missouri.edu`, `mail.missouri.edu` or `umsystem.edu`; all three
reach the same account and the same saved answers. Students stay signed in for
30 days across every lab. Owners and admins can lock a
whole lab or one student's answers from the dashboard. A locked lab still opens,
with the saved answers visible and every control disabled.

Opened with `marimo edit`, a notebook has no gate and simply does not save.

### Previewing without AWS

To click through a lab locally without signing in, temporarily replace
`gate/config.js` with:

```js
window.RADIANT_LAB_CONFIG = {
  region: "us-east-1", apiUrl: "http://mock.invalid", clientId: "mock",
  mock: true, mockAdmin: true, mockEmail: "you@umsystem.edu",
};
```

The gate then skips sign-in and keeps a fake database in this browser's
localStorage. Put the real file back (`git checkout labs/gate/config.js`) and
rebuild before committing.

## Previewing

```bash
jekyll serve            # whole site, http://127.0.0.1:4000/courses/csc_ee_8001.html
```

A lab bundle needs to be served over HTTP. Opening `index.html` from the filesystem
will not work, because WebAssembly and module scripts are blocked on `file://`.
