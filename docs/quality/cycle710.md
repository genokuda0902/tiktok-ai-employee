# cycle710 — 8-scene chapter rail (HUMAN REVIEW)

This zero-cost cycle improves the existing 1080×1920 / 30 fps image-slide MP4 by adding an eight-segment animated progress rail in the upper safe area (x=64, y=166, width=792, height=36). It is a *new* improvement after cycle709's scene-8 checklist and peak audio reduction.

## Reproduce
```bash
python -m pip install Pillow
python src/quality/cycle710_chapter_rail.py --source previous.mp4 --output cycle710.mp4 --frames /tmp/cycle710-rail --genre science
python -m unittest tests/test_cycle710_chapter_rail.py -v
ffprobe -v error -show_streams cycle710.mp4
ffmpeg -v error -i cycle710.mp4 -f null -
```
Requires ffmpeg/ffprobe, Python, Pillow. Original media and permission to use it must be supplied. No network requests, paid APIs, automatic posting or merge. Audio is stream-copied from the source; new Japanese narration and semantic subtitle/audio matching are **NOT verified**.

Supported palettes: ai_work, beauty, love_psychology, saving, sales_business, career, health, science, travel_food, product_comparison. Only science MP4 was rendered in this cycle; palette tests are not 10 rendered videos.

Local QA: 15/15 technical checks passed; 12/12 unit tests passed. Local deliverable MP4 and full QA report are in the conversation artifact ZIP, not committed as a binary. Employee approval and rights review required before manual posting.