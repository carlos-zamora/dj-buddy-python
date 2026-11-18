"""Tests for the djbuddy command-line interface."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from djbuddy import __version__
from djbuddy.cli import app

pytestmark = pytest.mark.unit

runner = CliRunner()


def test_version_prints_installed_version() -> None:
    result = runner.invoke(app, ["version"])

    assert result.exit_code == 0
    assert __version__ in result.output


def test_config_lists_settings_and_masks_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DJBUDDY_LLM_API_KEY", "sk-very-secret")

    result = runner.invoke(app, ["config"])

    assert result.exit_code == 0
    assert "database_url" in result.output
    assert "DJBUDDY_DATABASE_URL" in result.output
    assert "sk-very-secret" not in result.output


def test_no_arguments_shows_help() -> None:
    result = runner.invoke(app, [])

    # Typer exits with code 2 ("usage") when it prints help because no command was given.
    assert result.exit_code in (0, 2)
    assert "version" in result.output
    assert "config" in result.output
