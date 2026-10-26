# cycle873 — motion-safe editorial video (human review)

- **Change from cycle872:** gentle 30fps pan with 3.7% overscan, plus a timed outline around the locally computed 75% result.
- 10 genre presets and geometry validation; source assets and complete offline MP4 renderer are included in the user-facing review ZIP, **not committed here** because inherited portrait/audio rights remain unverified.
- Test: `python -m pip install pytest && python -m pytest -q experiments/cycle873/test_motion_core.py`
- Local technical QA: 24/24, 1080×1920 H.264 30fps, 691 frames, AAC 48kHz, full decode, 24 subtitle intervals.
- This CI only tests shared logic. It **does not** generate or certify the actual MP4.
- **PUBLICATION_NOT_APPROVED.** No auto-posting, paid API, merging, or user data.
