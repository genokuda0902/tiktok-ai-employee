# Cycle1427: review-only reproduction

Reimplementation, not recovered v33. Run: `python -m pip install Pillow==11.3.0 pytest==8.4.2`; install ffmpeg and Noto CJK fonts; `python quality/cycle1427/render.py`; `python -m pytest -q quality/cycle1427/test_render.py`.

15s 1080x1920 H264/AAC, scene-timed Japanese text, synthetic cue only (NO Japanese narration, NO speech synchronization). Original reference unavailable. No publishing, merge or automatic posting. Difference from cycle1426: 3-step visible progress bar, and complete renderer plus CI artifact workflow in same PR.
