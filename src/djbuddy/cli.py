"""Command-line interface, the ``djbuddy`` command.

The CLI is a thin layer: it parses arguments, calls into the service and domain modules, and
prints results with Rich. It holds no business logic of its own, so everything it does can
also be reached from the API and the assistant.

Commands added by later roadmap tasks:
    - ``demo``: load the seeded fixture library (P0-2).
    - ``import``, ``suggest``, ``order``, ``export`` and a ``--json`` flag (P1-6).
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

from djbuddy import __version__
from djbuddy.config import get_settings

app = typer.Typer(
    name="djbuddy",
    help="Plan DJ sets from your Rekordbox library.",
    no_args_is_help=True,
    add_completion=False,
)

# One shared console so all output goes through Rich (colours, tables, wrapping).
console = Console()


@app.command()
def version() -> None:
    """Print the installed dj-buddy-python version."""
    console.print(f"djbuddy {__version__}")


@app.command()
def config() -> None:
    """Show the active settings and where they can be changed.

    Secret values (API keys) are masked. Settings come from DJBUDDY_* environment variables
    and the .env file in the current directory.
    """
    table = Table(title="djbuddy settings", show_header=True, header_style="bold")
    table.add_column("Setting")
    table.add_column("Value")
    table.add_column("Environment variable", style="dim")
    for name, shown in get_settings().display_items():
        table.add_row(name, shown, f"DJBUDDY_{name.upper()}")
    console.print(table)


if __name__ == "__main__":  # pragma: no cover - use `python -m djbuddy` or the console script
    app()
