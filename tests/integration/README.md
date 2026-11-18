# Integration tests

Tests that touch a real database file, files on disk, or the HTTP API. Mark them with
`@pytest.mark.integration`.

- Database: a temporary SQLite file per test, upgraded with Alembic (from P1-1).
  From Phase 3, Postgres runs through testcontainers.
- API: FastAPI's `TestClient` (httpx) against the app factory (from P2-1).
- Ingest round trip: import, export, re-import loses nothing (P1-1, P1-5).

No test here may call a real LLM or need an API key.
