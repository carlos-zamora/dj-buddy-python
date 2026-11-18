"""Persistence: SQLAlchemy 2 models and repositories.

What lives here (from P1-1):
    - ORM models for tracks, playlists, sets and embeddings.
    - Repositories that load and save core models. The rest of the app talks to repositories,
      never to SQLAlchemy sessions directly.
    - Schema changes go through Alembic migrations in the top-level ``migrations/`` folder.

The database is SQLite until Phase 3, then Postgres with pgvector (P3-2). The URL comes
from ``djbuddy.config.Settings.database_url``.
"""
