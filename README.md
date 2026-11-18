# dj-buddy-python

A DJ set planner for Rekordbox libraries. It suggests harmonically compatible next tracks,
orders a crate into a set with a sensible BPM ramp and energy curve, and writes the result back
to Rekordbox as a playlist.

This is the Python successor to [dj-buddy](https://github.com/carlos-zamora/dj-buddy) (C#). It
ports dj-buddy's Camelot, BPM, track-graph and set-ordering logic, then adds a database, audio
embeddings from [music-ml](https://github.com/carlos-zamora/music-ml), swappable recommenders, an
LLM assistant, a web editor and an MCP server.

> **Status: Phase 0, Foundation.** The scaffold, tooling and CI are in place. The domain logic
> arrives in Phase 1. See [ROADMAP.md](ROADMAP.md).

## Principles

- **Rekordbox stays the source of truth.** BPM, key and cue points come from your Rekordbox XML
  export. The app never touches Rekordbox's `master.db`. It writes sets into a `DJ_BUDDY` folder in
  rekordbox.xml, after making a backup.
- **A pure core.** Music logic is plain Python with no I/O, so most tests run in seconds.
- **The assistant gets access, not intelligence.** Its tools return track IDs and facts.
  Deterministic code does the BPM maths and ordering.
- **Runs anywhere without your music or an API key.** A synthetic fixture library and an offline
  test model let every test run on a fresh Linux VM.

## Quickstart

You need [uv](https://docs.astral.sh/uv/). It installs the right Python (3.12) for you.

```bash
# Linux / macOS
curl -LsSf https://astral.sh/uv/install.sh | sh
uv sync          # create .venv and install locked dependencies
make check       # ruff + mypy + pytest
```

```powershell
# Windows (PowerShell)
winget install --id astral-sh.uv -e
uv sync
./scripts/check.ps1   # the same checks as `make check`
```

Then try the CLI:

```bash
uv run djbuddy --help
uv run djbuddy version
uv run djbuddy config    # show active settings (API keys masked)
```

## Configuration

Settings come from `DJBUDDY_*` environment variables or a `.env` file in the working directory.
Copy [.env.example](.env.example) to `.env` to start. Every setting has a default that works
offline.

| Variable               | Default                   | Purpose                                         |
| ---------------------- | ------------------------- | ----------------------------------------------- |
| `DJBUDDY_DATABASE_URL` | `sqlite:///./djbuddy.db`  | App database (SQLite now, Postgres in Phase 3) |
| `DJBUDDY_LIBRARY_PATH` | not set                   | Path to your rekordbox.xml export               |
| `DJBUDDY_MODEL_NAME`   | `test`                    | Assistant model; `test` is the offline model    |
| `DJBUDDY_LLM_API_KEY`  | not set                   | Model provider key, only for live runs          |

## Development

| Task                     | Linux / macOS     | Windows                     |
| ------------------------ | ----------------- | --------------------------- |
| Install dependencies     | `make install`    | `uv sync --locked`          |
| All checks (CI gate)     | `make check`      | `./scripts/check.ps1`       |
| Auto-fix lint and format | `make format`     | `./scripts/check.ps1 -Fix`  |
| Tests only               | `make test`       | `uv run pytest`             |
| Coverage report          | `make cov`        | `uv run pytest --cov`       |
| Add a dependency         | `uv add <pkg>`    | `uv add <pkg>`              |

Every change ends with the checks green and includes a test that failed before the change.
Docstrings are required on every module, class and function (ruff enforces Google style,
including an `Args:` entry for each parameter). [CLAUDE.md](CLAUDE.md) has the full contributor
rules, for humans and AI coding agents alike.

## Project layout

```text
dj-buddy-python/
├── src/djbuddy/
│   ├── core/        # pure: Camelot, BPM, track graph, set ordering, models
│   ├── ingest/      # rekordbox.xml import and export
│   ├── store/       # SQLAlchemy models and repositories
│   ├── analysis/    # audio embeddings and genre tags (from music-ml)
│   ├── recommend/   # Recommender interface, rules and embedding recommenders
│   ├── assistant/   # LLM agent, tools, prompts
│   ├── api/         # FastAPI app, routers, schemas
│   ├── config.py    # settings from env vars and .env
│   └── cli.py       # the `djbuddy` command
├── tests/{unit,integration,evals,fixtures}/
├── migrations/      # Alembic (from P1-1)
├── web/             # React editor (Phase 3)
├── docs/architecture.md
├── scripts/check.ps1
├── ROADMAP.md
└── CLAUDE.md
```

## Documentation

- [docs/architecture.md](docs/architecture.md): architecture, key decisions, package choices,
  testing plan.
- [ROADMAP.md](ROADMAP.md): phases, gates and the task tracker.
- [CLAUDE.md](CLAUDE.md): rules and conventions for contributors and AI coding agents.

## License

[MIT](LICENSE)
