# Cycle1264
Review-only 15s animation and Japanese SRT; no narration. Prior cycle1263: static 3-scene Japanese captions at 1080p; this cycle adds progress motion but reduces resolution to 720p. Local render: H264 720x1280, 15s, full decode pass; 3 local unit tests pass. GitHub-source rerender and CI not yet verified. No approved publishing.

Run: `python quality/cycle1264/render_cycle1264.py` then inspect output. Requires Pillow, FFmpeg and Noto CJK fonts.
