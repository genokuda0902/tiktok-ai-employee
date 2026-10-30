# Cycle1019 — staged visual focus (HUMAN_REVIEW)

## Previous cycle vs. this cycle

- cycle1017: 2.6% masked push-in of slide imagery across 8 scenes.
- cycle1019: **new** timed attention guide in scene 06, highlighting the existing
  BEFORE card first (coral) and AFTER card second (cyan) using soft outer glows.
- Does not redo zoom, sharpening, scene dips, caption tracks, or pause trimming.
- Existing 8 scenes, 22.5s, 675 frames, 1080x1920 H.264/30fps, Japanese
  AAC/48kHz, burned-in captions and chapter boundaries remain unchanged.

## Local verified deliverable

Full 22.5s MP4 was rendered and checked locally (not committed to GitHub):
`cycle1019_STAGED_FOCUS_JP_HUMAN_REVIEW.mp4`.
SHA256: `d28d693be193d2352db04b64cf8664606142c1af5c706a6cd10703716693fc55`.

Verified: full AV decode; 675 frames; 8 chapters; bitstream-identical
source/output AAC; scene06 border changes 27.446/255 (BEFORE) and
22.453/255 (AFTER) in test ROIs; subtitle ROI change 0.672/255;
7 sampled other-scene full-frame MAE values below 1/255; local unit
tests 9/9 PASS.

CI generates and decodes a separate **synthetic two-second** sample.
It does not test the full 22.5s file, which is local-only.

## Usage

```bash
python -m pip install Pillow
python quality/cycle1019/scene_focus.py INPUT.mp4 OUTPUT.mp4 \
  --genre ai_work --start 14.1 --end 16.767
python -m unittest discover -s quality/cycle1019 -p 'test_*.py'
```

Ten configurable palettes exist, but the full MP4 was tested only for
`ai_work`. Card coordinates are template-specific and must be recalibrated
for other content. The reference v33 MP4 was not directly compared.
No independent Japanese ASR, narration/caption semantic sync verification,
smartphone test, rights clearance, or employee approval. The video is
**NOT APPROVED FOR PUBLICATION**. Employee review then manual posting only.
No auto-posting, paid contracts, unauthorized merge, or new paid APIs.
