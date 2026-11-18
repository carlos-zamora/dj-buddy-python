# Test fixtures

Synthetic data only. Never put a real Rekordbox library, real audio, or a real master.db here.

Planned contents:

- A seeded 300-track `rekordbox.xml` with playlists and history sets (P0-2). The same seed must
  produce a byte-identical file.
- `minimal.xml` and `round_trip.xml`, ported from dj-buddy's `Rekordbox.Tests` (P1-1).
- Precomputed embedding vectors for the fixture tracks (P0-2), so recommender tests need no audio
  and no model weights.
