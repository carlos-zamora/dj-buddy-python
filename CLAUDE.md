# CLAUDE.md

Rules and conventions for AI coding agents (and humans) working in this repo. `AGENTS.md` points
here. Read this whole file before making a change.

## What this project is

dj-buddy-python is a DJ set planner for Rekordbox libraries, written in Python 3.12. It ports
the C# [dj-buddy](https://github.com/carlos-zamora/dj-buddy) core (Camelot keys, BPM matching,
track graph, set ordering) and builds a service, recommenders, an LLM assistant and a web editor
on top. Architecture: [docs/architecture.md](docs/architecture.md). Task tracker and current
phase: [ROADMAP.md](ROADMAP.md).

## Hard rules

These are not negotiable. A change that breaks one is wrong even if the tests pass.

1. **Never write to Rekordbox's `master.db`.** Do not open it either. Read and write only
   rekordbox.xml. Back up the target before every export and write atomically.
2. **Never commit audio, a real music library, `.env` files or API keys.** Test data is synthetic
   and lives in `tests/fixtures/`.
3. **One behaviour per change.** Do not bundle refactors, renames or unrelated fixes with a
   feature.
4. **Every task ends with `make check` green** (`./scripts/check.ps1` on Windows) **and a new test
   that failed before the change.** Run the checks yourself before saying a task is done, and
   report failures as they are.
5. **No test calls a real LLM or the network.** Use Pydantic AI's test model. Live evals run only
   on a schedule (`tests/evals`).

## Commands

```bash
uv sync                  # install locked dependencies into .venv
make check               # ruff lint + format check + mypy + pytest (the CI gate)
make format              # auto-fix lint and formatting
uv run pytest tests/unit/test_config.py -k dotenv   # run one test
uv run djbuddy --help    # the CLI
uv add <pkg>             # add a runtime dependency (updates pyproject.toml and uv.lock)
uv add --dev <pkg>       # add a dev dependency
```

On Windows without make: `./scripts/check.ps1` (add `-Fix` to auto-fix first).

## Layout and dependency direction

```text
cli / api / assistant / (MCP server)    entry points; thin
            │
        recommend                       Recommender interface + implementations
            │
  ingest · store · analysis             I/O: files, database, audio
            │
          core                          pure: no I/O, imports nothing else from djbuddy
```

- `djbuddy.core` is pure. It must not import any other `djbuddy` package or any I/O library
  (database, HTTP, Rekordbox parsing, LLM). `tests/unit/test_architecture.py` enforces this. If
  you add an I/O-bound dependency, add it to `FORBIDDEN_TOP_LEVEL` there.
- Higher layers pass plain objects (dataclasses from `djbuddy.core.models`) into core functions and
  get plain objects back.
- Other layers reach the database only through repositories in `djbuddy.store`.
- Each package's `__init__.py` docstring says what belongs in it. Read it before adding a module.

## Code style

- **Docstrings on every module, class and function**, Google style. Describe what the function
  does, then document every parameter under `Args:`, the result under `Returns:` (or `Yields:`),
  and anything raised under `Raises:`. Ruff's `D` rules enforce this, including D417, which fails
  when a parameter is missing from `Args:`. Tests are exempt, but helpers in tests should still
  have one.
- **Comments explain why, not what.** Add one wherever the reason for the code is not obvious:
  a music-theory rule, a dj-buddy parity quirk, a Rekordbox format detail.
- **Types everywhere.** `mypy --strict` applies to `djbuddy.core` and `djbuddy.recommend`. Other
  packages still need full annotations on every function.
- Use `from __future__ import annotations`, `pathlib.Path` for paths, and dataclasses or Pydantic
  models instead of loose dicts.
- Line length 100. Ruff formats; do not hand-format.

Example of the expected docstring style:

```python
def bpm_tier(a: float, b: float, tolerance: float = 0.06) -> BpmTier:
    """Classify how well two tempos mix, allowing half- and double-time matches.

    Args:
        a: Tempo of the outgoing track, in beats per minute.
        b: Tempo of the incoming track, in beats per minute.
        tolerance: Largest relative tempo difference still counted as a match.

    Returns:
        The best tier that applies: exact, close, half/double time, or none.

    Raises:
        ValueError: If either tempo is not positive.
    """
```

## Testing

- Put tests in `tests/unit` (pure code, marked `unit`), `tests/integration` (database, files,
  API; marked `integration`) or `tests/evals` (assistant; marked `evals`). Markers are strict.
- Core logic gets property tests with hypothesis (e.g. "ordering returns a permutation", "same
  seed, same order") as well as example tests.
- Parity tests port dj-buddy's `Rekordbox.Tests` cases and must give the same answers.
- The autouse `clean_settings` fixture isolates tests from your real `.env` and `DJBUDDY_*`
  variables. Set what a test needs with `monkeypatch.setenv`.
- Coverage target: 90% of lines in `core/` and `recommend/` (the gate arrives with P1-2).

## Configuration

`djbuddy.config.Settings` reads `DJBUDDY_*` environment variables and `.env`. Add new settings
there with a safe offline default, document them in the class docstring and `.env.example`, and
mark secrets as `SecretStr` so `djbuddy config` masks them.

## Working on a roadmap task

1. Find the task in [ROADMAP.md](ROADMAP.md). Work tasks in ID order; each has rounds (R1, R2, R3)
   and a "done when" check.
2. Write the failing test first, then the code.
3. Add any new dependency with `uv add` in the same change that uses it.
4. Run `make check`. When the task's "done when" check holds, tick it in ROADMAP.md.
