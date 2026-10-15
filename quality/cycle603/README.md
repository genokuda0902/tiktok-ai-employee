# Cycle603 — focal hook (HUMAN_REVIEW)

Baseline: cycle602. Adds a short, palette-aware CPU focus cue in the first 1.75 seconds. This is not a TikTok publication approval.

- Video: 1080x1920, 30fps, 15.6s, H.264/AAC.
- Local QA: 12/12 technical checks passed, 5/5 local unit tests passed.
- Audio bitstream preserved; semantic Japanese subtitle alignment and voice naturalness NOT verified.
- Source baseline MP4 is not committed to GitHub; retrieve from the reproducible cycle603 ZIP in the conversation. Put it at `quality/cycle603/assets/cycle602_baseline.mp4`.
- Run `python -m pytest -q quality/cycle603/tests` (Pillow, pytest).
- Run `python quality/cycle603/build_cycle603.py` (FFmpeg required).
- SHA-256 of local output: `640f24705aa165cf7334c54d71a5f7f8d5af07b391a03be9f99d7fdcc87db716`.
- No automated posting, no paid service, no merging. Employee approval required before manual publication.
- Rights review of inherited images/audio remains outstanding.
