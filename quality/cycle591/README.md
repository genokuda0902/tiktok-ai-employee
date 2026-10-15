# Cycle591 — Japanese keyword caption emphasis (0 JPY)

Baseline: cycle590 MP4. This cycle highlights important Japanese words in seven subtitle segments while keeping the 1080x1920, 30fps, 15.6s H.264 picture, original AAC Japanese-voice track and final checklist. Ten genres share a configurable palette. Final output is HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

Reproduce locally using `python build_cycle591.py` after placing cycle590 MP4 at `assets/cycle590.mp4`; then run `python qa_cycle591.py` and `python -m pytest -q tests/test_cycle591.py`. The complete baseline and scripts are distributed separately in the conversation ZIP. GitHub alone does not contain the MP4 asset.

QA: 13/13 technical checks and 4/4 unit tests locally. Human review still required for Japanese voice naturalness, exact spoken-text alignment, media rights and phone playback. No posting, payment, or merge performed.
