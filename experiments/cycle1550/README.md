# cycle1550 — review only

Independent synthetic Excel SUM demonstration with animated cell highlight, formula typing and result reveal. No external or private assets. No narration or synchronized spoken captions; publication blocked.

Run on Ubuntu with ffmpeg, fonts-noto-cjk and Pillow:

```bash
python -m pip install Pillow
python -m unittest discover -s experiments/cycle1550 -p 'test_*.py'
cd experiments/cycle1550 && python render.py
ffmpeg -v error -i cycle1550_REVIEW_ONLY.mp4 -f null -
```

Local run: 3 tests passed, 720x1280 H.264, 12 seconds, no audio stream. Next: approved offline Japanese TTS, timestamped subtitles and CI artifact upload. Prior cycle1549 burned Japanese captions but had no narration. Original reference v33 not accessible; no equivalence claimed.
