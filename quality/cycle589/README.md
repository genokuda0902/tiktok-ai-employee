# cycle589 — spreadsheet proof UI (REVIEW ONLY)

- Date: 2026-10-15 JST; additional spend ¥0.
- User-visible predecessor: cycle587 20-second synthetic AI/Excel demo. Latest open PR #49 is a **different Raspberry Pi / silence-aware checklist branch**, not the predecessor of this Excel-video iteration.
- Replace seconds 9–12 with a new original spreadsheet-like screen, animated selection of B2:B5, SUM formula entry, and computed total 720. Synthetic data only: 120+150+200+250=720.
- 10 configurable genre accent themes and a fail-closed numeric check. Only AI/productivity video was rendered.
- This repository contains a standalone compact renderer and regression tests. A separate local delivery ZIP contains the full renderer used for the shared MP4, which has additional cursor/window polish; the two renderers are **not byte-identical**. Both use the same verified data and timing. Do not claim a byte-reproducible GitHub video.
- Local reproduction: `python -m unittest -v test_scene_proof.py`; `python scene_proof.py --baseline /path/to/cycle587_collision_free_REVIEW_ONLY.mp4 --out cycle589_REVIEW_ONLY.mp4`. Requires Pillow, FFmpeg/libx264 and Noto Sans CJK font.
- GitHub source video and inherited AAC are not uploaded because inherited media rights are unverified. No Japanese TTS; existing BGM/SFX only; no speech-to-caption alignment. No production/employee release.
- v33 reference and user 16-panel storyboard show a real tool UI. This synthetic scene is an improvement over prior flat proof cards but not equivalent to v33.
- CI workflow write was rejected by the connector safety check; CI is NOT RUN. Tests ran locally on the full local renderer.
- Quality state: HUMAN_REVIEW; PUBLICATION_NOT_APPROVED. No merge, auto-post or payment.
