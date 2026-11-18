"""Architecture guard: djbuddy.core must stay pure.

The core holds the domain logic that most tests exercise. It stays fast and deterministic only
if it never reaches for a database, the network, files or another djbuddy layer. This test reads
the import statements of every module under ``src/djbuddy/core`` and fails on any forbidden one.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

CORE_DIR = Path(__file__).resolve().parents[2] / "src" / "djbuddy" / "core"

# Top-level modules the core may not import. Extend this list when a new I/O-bound
# dependency joins the project.
FORBIDDEN_TOP_LEVEL = frozenset(
    {
        # persistence
        "sqlalchemy",
        "alembic",
        "sqlite3",
        "psycopg",
        "pgvector",
        # web and network
        "fastapi",
        "starlette",
        "httpx",
        "requests",
        "urllib",
        "socket",
        # processes and jobs
        "subprocess",
        "arq",
        "redis",
        # Rekordbox files and audio
        "pyrekordbox",
        "lxml",
        "torch",
        # LLM providers and agent frameworks
        "pydantic_ai",
        "anthropic",
        "openai",
        # presentation
        "typer",
        "rich",
    }
)


def forbidden_imports(source: str) -> list[str]:
    """Find the imports in one core module's source that break the pure-core rule.

    A module breaks the rule if it imports a top-level module from ``FORBIDDEN_TOP_LEVEL``,
    imports any ``djbuddy`` package other than ``djbuddy.core``, or uses a relative import that
    climbs out of the core package (two or more leading dots).

    Args:
        source: The Python source code of a module inside ``djbuddy.core``.

    Returns:
        A description of each offending import, in source order; empty when the module is pure.
    """
    problems: list[str] = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level >= 2:
                dots = "." * node.level
                problems.append(f"relative import leaves core: {dots}{node.module or ''}")
                continue
            if node.level == 1:
                continue  # sibling module inside core
            names = [node.module or ""]
        else:
            continue
        for name in names:
            top = name.split(".")[0]
            in_core = name == "djbuddy.core" or name.startswith("djbuddy.core.")
            if top in FORBIDDEN_TOP_LEVEL:
                problems.append(f"I/O or framework import: {name}")
            elif top == "djbuddy" and not in_core:
                problems.append(f"import from another djbuddy layer: {name}")
    return problems


def core_modules() -> list[Path]:
    """List every Python file in the core package.

    Returns:
        Paths of the ``.py`` files under ``src/djbuddy/core``, sorted for stable test IDs.
    """
    return sorted(CORE_DIR.rglob("*.py"))


@pytest.mark.parametrize("module", core_modules(), ids=lambda p: p.relative_to(CORE_DIR).as_posix())
def test_core_module_is_pure(module: Path) -> None:
    assert forbidden_imports(module.read_text(encoding="utf-8")) == []


@pytest.mark.parametrize(
    "source",
    [
        "import sqlalchemy",
        "from fastapi import FastAPI",
        "import urllib.request",
        "from djbuddy.store import repo",
        "import djbuddy.api",
        "from ..store import repo",
    ],
)
def test_guard_rejects_impure_imports(source: str) -> None:
    assert forbidden_imports(source) != []


@pytest.mark.parametrize(
    "source",
    [
        "import math",
        "from dataclasses import dataclass",
        "from djbuddy.core.camelot import CamelotKey",
        "from .bpm import bpm_tier",
        "import networkx as nx",
    ],
)
def test_guard_allows_pure_imports(source: str) -> None:
    assert forbidden_imports(source) == []
