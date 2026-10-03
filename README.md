# Radiant Systems Lab Website

This repository contains the Jekyll source for the Radiant Systems Lab website.

## Local development

Install the Ruby dependencies once:

```powershell
bundle install
```

Build and serve the site locally:

```powershell
bundle exec jekyll serve --livereload
```

Open `http://127.0.0.1:4000/` in a browser. For a production-style validation build, run:

```powershell
bundle exec jekyll build --trace
```

## Contributor documentation

- `CHANGE_GUIDE.md` explains which file owns each kind of website content.
- `AGENTS.md` records important data, rendering, ordering, and validation conventions.
- `TUTORIAL_SECTION_IMPLEMENTATION.md` documents the tutorial-section architecture and initial implementation.

Primary structured content lives under `_data/`. Page templates are Markdown files in the repository root, reusable markup lives under `_includes/`, and the shared site styling is in `assets/themes/twitter/css/style.css`.
