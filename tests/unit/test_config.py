"""Tests for djbuddy.config: defaults, overrides and safe display of secrets."""

from __future__ import annotations

from pathlib import Path

import pytest

from djbuddy.config import SECRET_MASK, Settings, get_settings

pytestmark = pytest.mark.unit


def test_defaults_need_no_library_database_server_or_api_key() -> None:
    settings = Settings()

    assert settings.database_url == "sqlite:///./djbuddy.db"
    assert settings.library_path is None
    assert settings.model_name == "test"
    assert settings.llm_api_key is None


def test_environment_variables_override_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DJBUDDY_DATABASE_URL", "sqlite:///./other.db")
    monkeypatch.setenv("DJBUDDY_LIBRARY_PATH", "music/rekordbox.xml")

    settings = Settings()

    assert settings.database_url == "sqlite:///./other.db"
    assert settings.library_path == Path("music/rekordbox.xml")


def test_dotenv_file_is_read(tmp_path: Path) -> None:
    # The clean_settings fixture has already moved into tmp_path.
    (tmp_path / ".env").write_text("DJBUDDY_MODEL_NAME=anthropic:claude-sonnet-5-5\n")

    assert Settings().model_name == "anthropic:claude-sonnet-5-5"


def test_display_items_masks_secrets_and_marks_unset_values(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DJBUDDY_LLM_API_KEY", "sk-very-secret")

    shown = dict(Settings().display_items())

    assert shown["llm_api_key"] == SECRET_MASK
    assert "sk-very-secret" not in shown.values()
    assert shown["library_path"] == "(not set)"


def test_get_settings_is_cached() -> None:
    assert get_settings() is get_settings()
