"""Shared pytest fixtures for the whole test suite."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import pytest

from djbuddy.config import get_settings


@pytest.fixture(autouse=True)
def clean_settings(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Iterator[None]:
    """Isolate every test from the developer's real configuration.

    Removes all ``DJBUDDY_*`` environment variables, moves into an empty temporary directory so
    no ``.env`` file is picked up, and clears the cached settings before and after the test.
    Tests that need a setting set it with ``monkeypatch.setenv``.

    Args:
        monkeypatch: pytest's fixture for temporary environment and working-directory changes.
        tmp_path: An empty per-test directory provided by pytest.

    Yields:
        Nothing; the fixture only sets up and tears down state.
    """
    import os

    for key in list(os.environ):
        if key.startswith("DJBUDDY_"):
            monkeypatch.delenv(key)
    monkeypatch.chdir(tmp_path)
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
