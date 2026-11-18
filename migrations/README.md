# Database migrations

Alembic migration scripts live here. Task **P1-1** (Rekordbox import) runs `alembic init`,
points it at `djbuddy.store` models and `Settings.database_url`, and adds the first revision.

Every schema change gets a migration, and tests check both `upgrade` and `downgrade`.
