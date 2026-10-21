# cycle750 / three-stage end card
Zero-cost quality experiment. Cycle749 changed scene 2; cycle750 changes scene 8 (save → run → result).
The attached MP4 was locally rendered at 1080×1920, 30 fps, 14.3 seconds; inherited Japanese AAC stream is copied.
The code in this branch is a portable, compact reproduction of the end-card approach; the full exact-generation source, 3 PNG stages, MP4 and QA are delivered separately in the cycle750 ZIP.
To regenerate: install Pillow and ffmpeg, place a rights-cleared previous.mp4 in input/, then run:
python experiments/cycle750/endcard.py
python experiments/cycle750/render.py
Local QA: 16/16 technical checks, 8/8 tests. Audio naturalness, reference equivalence, rights and physical smartphone playback unverified.
PUBLICATION_NOT_APPROVED. Human approval and manual upload only. No paid services, merges or automated posting.
