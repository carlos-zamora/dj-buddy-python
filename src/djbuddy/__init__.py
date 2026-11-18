"""dj-buddy-python: a DJ set planner for Rekordbox libraries.

The package is a modular monolith. Each subpackage owns one layer of the architecture
(see docs/architecture.md):

- ``core``: pure domain logic (Camelot keys, BPM matching, track graph, set ordering).
- ``ingest``: reading and writing rekordbox.xml.
- ``store``: persistence (SQLAlchemy models and repositories).
- ``analysis``: audio embeddings and genre tags.
- ``recommend``: the ``Recommender`` interface and its implementations.
- ``assistant``: the LLM agent and the tools it may call.
- ``api``: the FastAPI service.

``cli`` and ``config`` sit at the top level because every layer shares them.
"""

from importlib.metadata import PackageNotFoundError, version

try:
    # The installed distribution is "dj-buddy-python"; its version comes from pyproject.toml.
    __version__ = version("dj-buddy-python")
except PackageNotFoundError:  # pragma: no cover - only when running from an uninstalled checkout
    __version__ = "0.0.0+unknown"

__all__ = ["__version__"]
