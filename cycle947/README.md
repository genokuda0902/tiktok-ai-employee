# cycle947 — review-only second-angle microbeats

This experiment creates eight additional *composition beats* (one mild focus push-in in the second half of each of the eight existing scenes). It does not create eight new story scenes or reproduce the user's 16-panel cinematic storyboard. Content rectangle only (x20:1060, y155:1440); existing Japanese subtitle strip, top header, and lower meter are protected in source pixels. Ten genre-specific camera intensity presets; only AI-work MP4 generated privately.

Run locally with OpenCV, numpy, ffmpeg:

```bash
python cycle947/src/focus_microbeats.py --source INPUT_REVIEW_ONLY.mp4 --output OUTPUT_REVIEW_ONLY.mp4 --genre ai_work
python -m pytest -q cycle947/tests/test_focus_microbeats.py
```

**Security:** No private footage, narration, subtitles or MP4 committed. Source MP4 is inherited from prior review cycles and **not rights-cleared**. No publishing or auto-posting. Output is HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Not a substitute for independent Japanese ASR, caption semantic/timing check, smartphone playback, reference v33 comparison or employee approval.
