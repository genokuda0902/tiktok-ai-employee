# cycle820: ten-genre complete action plan (review-only)

Self-contained 15–18s overlay for a 1080×1920, 30fps MP4 with audio. Requires Python 3, Pillow, ffmpeg/ffprobe and Noto Sans CJK fonts. No private or rights-unverified media is committed.

Run tests:
```bash
PYTHONPATH=quality/cycle820 python -m unittest discover -s quality/cycle820 -p 'test_*.py' -v
```
Render only from a rights-approved source:
```bash
python quality/cycle820/action_story.py --source INPUT.mp4 --output review_output/REVIEW_ONLY.mp4 --genre sales_business
```
CI creates a 19-second synthetic-tone test MP4. It is NOT Japanese-narrated and NOT publication-ready. See CYCLE820_DELTA.md.
