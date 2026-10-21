# Cycle733: Japanese-only CTA (review only)

Reimplementation of the final 90 frames of a 27.343-second, 1080x1920 video. No reference v33 assets or confidential source files are committed.

## Local reproduction
Prerequisites: Python 3.11, Pillow, FFmpeg, Noto Sans CJK, and the **locally reviewed** cycle732 MP4 (819 frames, H.264/AAC, 1080x1920).

```bash
python video_engine/cycle733/cta_scene.py --source cycle732.mp4 --output cycle733.mp4 --genre ai_work
python -m unittest discover -s video_engine/cycle733 -p 'test_*.py' -v
ffmpeg -v error -i cycle733.mp4 -f null -
```

Changes from cycle732: replaces the old English 'SAVE THIS' final slide with three Japanese-native CTA beats, glass-like lighting, bookmark cue and clear caption safe-zone. Keeps the source AAC track. Ten genres have distinct palettes/copy but only ai_work has been rendered end-to-end.

Rights and approval: synthetic data; no public distribution or automatic posting. Voice rights, pronunciation, word-level subtitle timing, smartphone playback, reference-v33 visual parity and employee approval remain unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

The exact input video is not stored in GitHub. CI can run source/artwork tests, but not full end-to-end video QA without an approved source asset.
