# Roadmap

The live tracker for dj-buddy-python. Five phases, each closed by a gate you can check. Work tasks
in ID order. Each task has three rounds (R1 happy path, R2 and R3 edge cases, tests and refactors)
and a "done when" check. Tick a box only when its check passes.

The reasoning behind each phase is in [docs/architecture.md](docs/architecture.md).

| Phase | Theme | Gate | Status |
| --- | --- | --- | --- |
| P0 | Foundation | A fresh VM runs `make check` green with one command | In progress |
| P1 | Core port from dj-buddy | dj-buddy parity tests pass and the repo passes 1,000 lines | Not started |
| P2 | Service and assistant | Deterministic evals pass offline and against a live model | Not started |
| P3 | Web and cloud | `docker compose up` serves the app and one request traces end to end | Not started |
| P4 | Experiments and reach | A/B report runs on logged data and every page passes an axe scan | Not started |

## P0 · Foundation

Scaffold, CI on Ubuntu, and a seeded fixture library, so every later task starts from a green
build on a fresh Linux VM.

- [ ] **P0-1 Scaffold and CI.** Done when: on a fresh VM, `uv sync && make check` is green.
  - [x] R1 uv project, ruff, mypy, pytest
  - [x] R2 GitHub Actions on Ubuntu, Makefile (plus `scripts/check.ps1` for Windows)
  - [x] R3 CLAUDE.md rules, README quickstart
  - [ ] First CI run green on `ubuntu-latest` (all checks already pass locally on Windows)
- [ ] **P0-2 Fixture library generator.** Done when: the same seed gives an identical file, and
  `djbuddy demo` loads it.
  - [ ] R1 seeded generator for a 300-track rekordbox.xml
  - [ ] R2 playlists and history sets with realistic key and BPM mixes
  - [ ] R3 fixture embeddings, `djbuddy demo`

## P1 · Core port from dj-buddy

Rekordbox import and export, Camelot and BPM, the track graph, set ordering, and the CLI.

- [ ] **P1-1 Rekordbox import.** Done when: two imports in a row add no rows; fixtures pass.
  - [ ] R1 parse tracks and playlists with pyrekordbox
  - [ ] R2 persist with SQLAlchemy and Alembic, idempotent
  - [ ] R3 port dj-buddy fixtures and edge cases (missing key, unicode paths)
- [ ] **P1-2 Camelot and BPM core.** Done when: parity cases pass; properties hold over 1,000
  examples. Also turns on the 90% coverage gate for `core/` and `recommend/`.
  - [ ] R1 port CamelotWheel and HarmonicRelation
  - [ ] R2 BPM tiers with half and double time
  - [ ] R3 hypothesis properties and dj-buddy parity cases
- [ ] **P1-3 Track graph.** Done when: answers match dj-buddy on fixtures, under 200 ms per query.
  - [ ] R1 harmonic edges in networkx
  - [ ] R2 playlist co-occurrence edges and weights
  - [ ] R3 suggest-next and find-similar, timed on 10,000 fixture tracks
- [ ] **P1-4 Set ordering.** Done when: output is a permutation, and the transition score is never
  below the greedy order.
  - [ ] R1 port TrackSetOrdering
  - [ ] R2 target length, BPM ramp, energy curve
  - [ ] R3 a 2-opt improvement pass
- [ ] **P1-5 Rekordbox export.** Done when: the round trip loses nothing and Rekordbox opens the
  file.
  - [ ] R1 write the `DJ_BUDDY` folder
  - [ ] R2 backup and atomic write
  - [ ] R3 round-trip test, then a manual import in Rekordbox
- [ ] **P1-6 CLI.** Done when: every command has a test.
  - [ ] R1 `import`, `suggest`, `order`, `export` commands
  - [ ] R2 Rich tables and a `--json` flag
  - [ ] R3 CliRunner snapshot tests

## P2 · Service and assistant

FastAPI, the recommender interface, the Pydantic AI agent, and the eval suite.

- [ ] **P2-1 FastAPI service.** Done when: the OpenAPI snapshot is stable and tests are green.
  - [ ] R1 library and track endpoints
  - [ ] R2 sets and recommendations
  - [ ] R3 error model, OpenAPI snapshot, integration tests
- [ ] **P2-2 Recommender interface.** Done when: the replay report is committed and both
  recommenders beat a random baseline.
  - [ ] R1 interface plus the rules recommender
  - [ ] R2 embedding recommender on fixture vectors
  - [ ] R3 replay eval comparing both
- [ ] **P2-3 Assistant agent.** Done when: tests pass with no API key.
  - [ ] R1 agent with dj-buddy's library and workspace tools
  - [ ] R2 `SetPlan` structured output, validation, retries
  - [ ] R3 streaming endpoint, offline tests
- [ ] **P2-4 Assistant eval suite.** Done when: a baseline is stored and CI fails on a regression.
  - [ ] R1 30-case dataset and deterministic evaluators
  - [ ] R2 LLM judge and HTML report
  - [ ] R3 CI job that gates on the deterministic score

## P3 · Web and cloud

The React editor, Postgres with pgvector, the analysis worker, Docker, and OpenTelemetry.

- [ ] **P3-1 React set editor.** Done when: a keyboard-only user can build and save a set.
  - [ ] R1 Vite + TypeScript, generated client, library table
  - [ ] R2 set timeline with keyboard reorder and harmonic colours
  - [ ] R3 Playwright E2E and axe scan
- [ ] **P3-2 Postgres, pgvector, Docker.** Done when: `docker compose up` serves the app and tests
  are green.
  - [ ] R1 Compose with Postgres, Alembic on Postgres
  - [ ] R2 pgvector similarity replaces numpy
  - [ ] R3 testcontainers tests and a speed comparison
- [ ] **P3-3 Analysis worker.** Done when: killing the worker mid-job loses no work.
  - [ ] R1 arq job computes embeddings
  - [ ] R2 idempotency keys, retries with backoff, dead-letter list
  - [ ] R3 progress endpoint and tests
- [ ] **P3-4 OpenTelemetry.** Done when: one request shows end to end in Grafana.
  - [ ] R1 traces for FastAPI and SQLAlchemy
  - [ ] R2 spans for recommender and LLM calls (tokens, latency)
  - [ ] R3 Grafana dashboard committed as JSON

## P4 · Experiments and reach

An A/B test of recommenders, an MCP server for the library, and auth.

- [ ] **P4-1 A/B test of recommenders.** Done when: the report runs on logged fixture data.
  - [ ] R1 deterministic assignment by session hash
  - [ ] R2 log shown and accepted suggestions
  - [ ] R3 report with confidence intervals
- [ ] **P4-2 MCP server for the library.** Done when: it works from VS Code and Claude Desktop.
  - [ ] R1 read-only library tools
  - [ ] R2 set tools that return proposed sets instead of writing
  - [ ] R3 in-memory client tests
- [ ] **P4-3 Auth.** Done when: one user cannot read another's sets.
  - [ ] R1 OAuth login with Authlib
  - [ ] R2 per-user libraries
  - [ ] R3 permission tests
