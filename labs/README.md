# CSC/EE 8001 Labs

Interactive labs for *Designing End-to-End ML Systems*. Each lab is a
[marimo](https://marimo.io) notebook exported to WebAssembly, so it runs entirely in
the student's browser. There is nothing to install, no kernel, and no server.

## Layout

```
labs/
  _src/<slug>/notebook.py   source you edit          (not published - "_" prefix)
  <slug>/index.html         generated bundle          (published, committed)
  runtime/                  shared marimo frontend    (published, committed)
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
2. Create `labs/_src/<slug>/notebook.py`.
3. Build it, then flip `status` to `available`.

The card and the course page pick it up automatically; no HTML to edit.

## Previewing

```bash
jekyll serve            # whole site, http://127.0.0.1:4000/courses/csc_ee_8001.html
```

A lab bundle needs to be served over HTTP. Opening `index.html` from the filesystem
will not work, because WebAssembly and module scripts are blocked on `file://`.
