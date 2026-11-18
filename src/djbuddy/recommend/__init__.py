"""Track recommenders behind a single interface.

What lives here (from P2-2):
    - ``Recommender``: the interface every recommender implements.
    - A rules recommender built on the harmonic track graph from ``djbuddy.core``.
    - An embedding recommender that ranks tracks by audio-embedding similarity.
    - Experiment assignment for the A/B test of recommenders (P4-1).

Because both recommenders share one interface, choosing between them is configuration,
not a rewrite. This package is type-checked with ``mypy --strict`` and has a 90% coverage
target.
"""
