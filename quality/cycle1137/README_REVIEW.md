# cycle1137 — chapter-synchronized transition timing (REVIEW ONLY)

## Problem / distinct change from cycle1135
cycle1135 placed seven light sweeps at assumed 2.8-second intervals. The actual
source MP4 has nonuniform scene starts at 3.133, 5.600, 8.233, 11.000,
13.733, 16.633, and 19.167 seconds. Six of seven old sweeps missed their
cut, with absolute offsets of 0.167–0.433 seconds (mean 0.224 s).

This change reads actual MP4 chapter boundaries using ffprobe, snaps them to
30fps frames, and draws each 0.22-second accent only after the correct cut.
The effect is an original PIL alpha gradient; 10 genre palettes are supported.
It is a **timing and quality-gate fix**, not a new cinematic scene.

## Reproduction and tests
- `python -m unittest discover -s quality/cycle1137 -p 'test_*.py' -v`
- `python quality/cycle1137/chapter_sync.py source_with_chapters.mp4 review.mp4`
- GitHub CI uses **synthetic** color+sine media with embedded chapter metadata.
- Private full Japanese video is **not uploaded to public GitHub**.

## Local full MP4 validation (not CI)
- 22.5 s, H.264, 1080x1920, 30fps, 675 frames, full decode passed.
- Original AAC 48kHz bitstream copied identically.
- Burned-caption region compared against the pre-sweep source for all 675
  frames; mean absolute pixel difference 1.07/255 from re-encoding,
  max per-frame mean 1.267/255.
- Seven true cuts verified by chapter metadata and frame-difference peaks.
- 10 genre palettes and 7 regression unit tests passed locally.

## Unverified / restrictions
Japanese speech **content**, independent ASR, semantic speech-caption timing,
commercial rights for inherited narration, direct v33 original comparison,
phone playback, employee approval, and actual CI billing remain unverified.
User-provided 16-panel storyboard was reviewed, but this is not v33 parity.
No merge, paid services, auto-posting, or public user-media upload.
**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
