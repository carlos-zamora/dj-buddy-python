# AGENTS.md

The rules for AI coding agents in this repo are in [CLAUDE.md](CLAUDE.md). They apply to every
agent, not only Claude. Read that file in full before making changes.

The short version:

- Never write to Rekordbox's `master.db`. Never commit audio, a real library, `.env` files or API
  keys.
- One behaviour per change.
- Every change ends with `make check` green (`./scripts/check.ps1` on Windows) and a new test that
  failed before the change.
- Every module, class and function gets a Google-style docstring that documents each parameter.
