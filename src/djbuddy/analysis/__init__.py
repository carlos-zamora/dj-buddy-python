"""Audio analysis: embeddings and genre tags computed from local audio files.

What lives here (Phase 2 and 3):
    - PANNs audio embeddings and the genre model, both brought over from music-ml.
    - Batch analysis from the CLI first; an arq background worker later (P3-3).

Rules:
    - Audio files are read-only and are never committed to the repo.
    - Tests use precomputed fixture embeddings, so they need neither audio nor PyTorch weights.
"""
