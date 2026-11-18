"""Pure domain core: the music theory and set-building logic, with no I/O.

What lives here (ported from the C# dj-buddy, with its tests as parity tests):
    - ``camelot``: Camelot wheel keys and harmonic relations between them (P1-2).
    - ``bpm``: BPM compatibility tiers, including half- and double-time matches (P1-2).
    - ``graph``: the track graph with harmonic and playlist co-occurrence edges (P1-3).
    - ``ordering``: set ordering for a target length, BPM ramp and energy curve (P1-4).
    - ``models``: plain dataclasses (``Track``, ``SetPlan``, ...) shared by the layers above.

Rules (enforced by ``tests/unit/test_architecture.py`` and ``mypy --strict``):
    - No I/O: no files, network, database, clock or randomness without an explicit seed.
    - No imports from other ``djbuddy`` packages. Other layers depend on core, never the reverse.
    - Functions take plain objects and return plain objects, so tests need no fixtures beyond data.
"""
