"""Rekordbox import and export.

What lives here:
    - Import: parse tracks, playlists and history from rekordbox.xml with pyrekordbox and hand
      them to the store. A second import of the same file adds no rows (P1-1).
    - Export: write planned sets back as a ``DJ_BUDDY`` playlist folder in rekordbox.xml (P1-5).

Rules:
    - Rekordbox is the source of truth for BPM, key and cue points.
    - Never open or write Rekordbox's ``master.db``. Only rekordbox.xml is read or written.
    - Back up the target file before every export, and write atomically (temp file, then rename).
"""
