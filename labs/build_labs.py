#!/usr/bin/env python3
"""Compile every lab notebook under labs/_src/ into a committed WASM bundle.

Each labs/_src/<slug>/notebook.py is exported to labs/<slug>/, which Jekyll then
copies verbatim into the built site (the files carry no YAML front matter, so
Jekyll leaves them alone). Directories beginning with "_" are ignored by Jekyll,
so the sources themselves are never published.

Usage
-----
    python labs/build_labs.py              # build every lab
    python labs/build_labs.py lab_01_hello # build one lab
    python labs/build_labs.py --check      # verify bundles are up to date

Requires marimo. Install it into the repo-local venv:

    python -m venv labs/.venv
    labs/.venv/Scripts/python -m pip install marimo     # Windows
    labs/.venv/bin/python -m pip install marimo         # macOS / Linux
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

LABS_DIR = Path(__file__).resolve().parent
SRC_DIR = LABS_DIR / "_src"
REPO_ROOT = LABS_DIR.parent

# PWA manifests are rewritten post-hoist; excluded from the runtime-conflict check.
BRANDED = ("manifest.json", "site.webmanifest")


def discover(only: list[str]) -> list[Path]:
    if not SRC_DIR.is_dir():
        sys.exit(f"no lab sources found at {SRC_DIR}")
    found = sorted(p for p in SRC_DIR.iterdir() if p.is_dir() and (p / "notebook.py").is_file())
    if not only:
        return found
    by_name = {p.name: p for p in found}
    missing = [s for s in only if s not in by_name]
    if missing:
        sys.exit(f"unknown lab(s): {', '.join(missing)}\navailable: {', '.join(by_name)}")
    return [by_name[s] for s in only]


def build(src: Path) -> Path:
    out = LABS_DIR / src.name
    notebook = src / "notebook.py"

    # marimo's exporter does not reject a notebook that fails to parse, so a syntax
    # error would ship a broken bundle and only surface in a student's browser.
    try:
        ast.parse(notebook.read_text(encoding="utf-8"), filename=str(notebook))
    except SyntaxError as exc:
        sys.exit(f"{src.name}: notebook.py does not parse\n  line {exc.lineno}: {exc.msg}")

    # marimo refuses to overwrite without --force; clear the directory ourselves so
    # assets renamed between marimo versions do not accumulate as orphans.
    if out.exists():
        shutil.rmtree(out)

    cmd = [
        sys.executable, "-m", "marimo", "export", "html-wasm",
        str(notebook),
        "-o", str(out),
        "--mode", "run",
        "--no-show-code",
        "--force",
    ]
    # marimo shells out to `uv` to resolve the notebook's imports and looks it up on
    # PATH, not as an importable module. When this script runs from a venv, that
    # venv's Scripts/bin directory is not necessarily on PATH, so add it.
    env = dict(os.environ)
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")

    print(f"  building {src.name} ...", flush=True)
    result = subprocess.run(cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        sys.stderr.write(result.stdout + result.stderr)
        sys.exit(f"marimo export failed for {src.name}")

    index = out / "index.html"
    if not index.is_file():
        sys.exit(f"{src.name}: expected {index} but marimo did not produce it")

    hoist_runtime(out)
    patch_title(index, src.name)
    return out


def hoist_runtime(out: Path) -> None:
    """Move the shared marimo frontend out of the lab and rewrite the references.

    marimo emits its whole frontend (~26 MB: Plot, loro-wasm, cytoscape, vega, a SQL
    parser) next to every exported notebook. That payload depends only on the marimo
    version, not on the notebook, so sixteen labs would commit sixteen identical
    copies. Hoist it to labs/runtime/ once and point each lab's index.html at it.

    Filenames are content-hashed by marimo's bundler, so identical names are
    identical files; a name collision with differing bytes means two labs were built
    against different marimo versions, which is worth stopping on.
    """
    runtime = LABS_DIR / "runtime"
    runtime.mkdir(exist_ok=True)

    for item in sorted(out.rglob("*")):
        if not item.is_file() or item.name == "index.html":
            continue
        rel = item.relative_to(out)
        # The export drops a couple of files that are not web content: an editor
        # prompt file at the top level, and a .nojekyll that only has meaning at a
        # site root (and this site *is* Jekyll-built, so it must not be honoured).
        if (rel.parent == Path(".") and rel.suffix == ".md") or rel.name == ".nojekyll":
            item.unlink()
            continue
        dest = runtime / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            # The manifests are rewritten by brand_manifest() after hoisting, so the
            # copy already in runtime/ legitimately differs from a fresh export.
            if rel.name in BRANDED:
                item.unlink()
                continue
            if dest.stat().st_size != item.stat().st_size:
                sys.exit(
                    f"runtime conflict: {rel} differs from the copy already in "
                    f"labs/runtime/. Rebuild every lab with one marimo version:\n"
                    f"    python labs/build_labs.py"
                )
            item.unlink()
        else:
            shutil.move(str(item), str(dest))

    # Drop the now-empty directories the export left behind.
    for d in sorted((p for p in out.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()

    index = out / "index.html"
    html = index.read_text(encoding="utf-8")
    html = html.replace('="./', '="../runtime/')
    index.write_text(html, encoding="utf-8")

    brand_manifest(runtime)


def brand_manifest(runtime: Path) -> None:
    """Replace marimo's default PWA name so installed labs are identifiable."""
    for name in BRANDED:
        path = runtime / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace('"A Marimo App"', '"CSC/EE 8001 Labs"')
        text = text.replace('"Marimo"', '"8001 Labs"')
        path.write_text(text, encoding="utf-8")


def patch_title(index: Path, slug: str) -> None:
    """Replace marimo's generated <title> and placeholder description.

    marimo derives the title from the filename ("notebook") and hardcodes
    <meta name="description" content="a marimo app">. Both leak into browser
    tabs, bookmarks and link previews, so rewrite them from lab metadata.
    """
    meta = read_lab_meta(slug)
    if meta is None:
        return

    html = index.read_text(encoding="utf-8")
    if meta.get("week"):
        title = f"Week {meta['week']}: {meta['title']} - CSC/EE 8001"
    else:
        title = f"Lab {meta['number']}: {meta['title']} - CSC/EE 8001"
    summary = " ".join(meta.get("summary", "").split())


    html = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", html, count=1, flags=re.S)
    if summary:
        html = re.sub(
            r'<meta name="description" content="[^"]*"\s*/?>',
            f'<meta name="description" content="{summary}" />',
            html,
            count=1,
        )
    index.write_text(html, encoding="utf-8")


def read_lab_meta(slug: str) -> dict | None:
    """Pull number/title/summary for `slug` out of _data/labs.yml.

    Hand-parsed so the build has no PyYAML dependency; the file is a flat list
    of scalar fields plus a folded `summary`, which is all this needs.
    """
    data = REPO_ROOT / "_data" / "labs.yml"
    if not data.is_file():
        return None

    record: dict = {}
    current: dict = {}
    in_summary = False
    summary: list[str] = []

    for raw in data.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("- id:"):
            if current.get("slug") == slug:
                current["summary"] = " ".join(summary)
                record = current
                break
            current, summary, in_summary = {}, [], False
            continue
        stripped = line.strip()
        if in_summary:
            if line.startswith("    ") and stripped and not stripped.endswith(":"):
                summary.append(stripped)
                continue
            in_summary = False
        if stripped == "summary: >":
            in_summary = True
            continue
        for key in ("number", "week", "part", "slug", "title"):
            prefix = f"{key}:"
            if stripped.startswith(prefix):
                value = stripped[len(prefix):].strip().strip("'\"")
                current[key] = int(value) if key in ("number", "week") else value

    if not record and current.get("slug") == slug:
        current["summary"] = " ".join(summary)
        record = current

    return record or None


def check_published() -> int:
    """Fail if Jekyll would silently drop any file in labs/runtime/.

    Jekyll skips every entry whose basename starts with "_", ".", "#" or "~" unless
    it is named in the `include:` list. marimo's bundler emits several such modules
    (vite externals, lodash internals), and a dropped module is a 404 at runtime that
    breaks every lab. A marimo upgrade can introduce new ones, so this check exists to
    catch that at build time rather than in a student's browser.
    """
    import fnmatch

    runtime = LABS_DIR / "runtime"
    if not runtime.is_dir():
        print("labs/runtime/ does not exist; nothing to check")
        return 0

    config = (REPO_ROOT / "_config.yml").read_text(encoding="utf-8")
    match = re.search(r"^include:\s*\[(.*?)\]", config, re.S | re.M)
    patterns = re.findall(r'"([^"]+)"', match.group(1)) if match else []

    at_risk = [
        f for f in runtime.rglob("*")
        if f.is_file() and f.name[:1] in ("_", ".", "#", "~")
    ]
    unlisted = [
        f for f in at_risk
        if not any(fnmatch.fnmatch(f.name, p) for p in patterns)
    ]

    if unlisted:
        print("These files would be dropped by Jekyll and 404 at runtime:")
        for f in sorted(unlisted):
            print(f"  labs/{f.relative_to(LABS_DIR)}")
        print("\nAdd their basename patterns to `include:` in _config.yml.")
        return 1

    print(f"ok: {len(at_risk)} at-risk file(s) in labs/runtime/ are all covered by include:")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("labs", nargs="*", help="slug(s) to build; default is all")
    parser.add_argument(
        "--check", action="store_true",
        help="fail if any bundle is older than its source",
    )
    parser.add_argument(
        "--check-published", action="store_true",
        help="fail if any runtime file would be dropped by Jekyll",
    )
    args = parser.parse_args()

    if args.check_published:
        sys.exit(check_published())

    sources = discover(args.labs)
    if not sources:
        sys.exit(f"no notebook.py found under {SRC_DIR}")

    if args.check:
        stale = []
        for src in sources:
            out = LABS_DIR / src.name / "index.html"
            if not out.is_file():
                stale.append(f"{src.name}: never built")
            elif (src / "notebook.py").stat().st_mtime > out.stat().st_mtime:
                stale.append(f"{src.name}: source is newer than bundle")
        if stale:
            print("stale bundles:\n  " + "\n  ".join(stale))
            sys.exit(1)
        print(f"all {len(sources)} bundle(s) up to date")
        return

    print(f"building {len(sources)} lab(s) from {SRC_DIR}")
    for src in sources:
        out = build(src)
        size = sum(f.stat().st_size for f in out.rglob("*") if f.is_file())
        count = sum(1 for f in out.rglob("*") if f.is_file())
        print(f"  -> labs/{out.name}/  ({count} files, {size / 1_048_576:.1f} MB)")
    print("done")


if __name__ == "__main__":
    main()
