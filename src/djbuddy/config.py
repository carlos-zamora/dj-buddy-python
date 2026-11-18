"""Application settings, loaded from environment variables and an optional ``.env`` file.

Every setting can be overridden with an environment variable that has the ``DJBUDDY_`` prefix,
for example ``DJBUDDY_DATABASE_URL=sqlite:///./other.db``. See ``.env.example`` for the full list.

The defaults let the app and the whole test suite run on a fresh machine with no music library,
no database server and no API key.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

#: Characters shown in place of a secret value when settings are displayed.
SECRET_MASK = "********"


class Settings(BaseSettings):
    """Typed configuration for dj-buddy-python.

    Values come from, in order of priority: keyword arguments, ``DJBUDDY_*`` environment
    variables, the ``.env`` file in the working directory, and finally the defaults below.

    Attributes:
        database_url: SQLAlchemy URL of the app database. SQLite until Phase 3, then Postgres.
        library_path: Path to the user's rekordbox.xml export. ``None`` until the user sets it;
            commands that need a library will ask for it.
        model_name: Model the assistant uses, as a Pydantic AI model string. The default
            ``"test"`` is Pydantic AI's offline test model, so nothing calls a paid API by accident.
        llm_api_key: API key for the model provider. Never logged or displayed in full.
    """

    model_config = SettingsConfigDict(
        env_prefix="DJBUDDY_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(default="sqlite:///./djbuddy.db")
    library_path: Path | None = Field(default=None)
    model_name: str = Field(default="test")
    llm_api_key: SecretStr | None = Field(default=None)

    def display_items(self) -> list[tuple[str, str]]:
        """List every setting as a (name, value) pair that is safe to print.

        Secret values are replaced by ``SECRET_MASK``. Unset optional values show as
        ``"(not set)"`` so the output says plainly what is missing.

        Returns:
            Pairs of setting name and display string, in field declaration order.
        """
        items: list[tuple[str, str]] = []
        for name in type(self).model_fields:
            value = getattr(self, name)
            if value is None:
                shown = "(not set)"
            elif isinstance(value, SecretStr):
                shown = SECRET_MASK
            else:
                shown = str(value)
            items.append((name, shown))
        return items


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings, loading them on first call.

    The result is cached so every caller sees the same object. Tests that change environment
    variables must call ``get_settings.cache_clear()`` afterwards (the ``clean_settings``
    fixture in ``tests/conftest.py`` does this).

    Returns:
        The loaded ``Settings`` instance.
    """
    return Settings()
