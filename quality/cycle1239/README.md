# cycle1239 — Save/Reuse clarity (human review only)

## Change from cycle1237
- cycle1237 repaired scene 6's Before/After ghost outline.
- cycle1239 replaces scene 7's overlapping library labels with a clean, original two-step diagram: summarize instruction → save it → reuse next time.
- Ten genre-specific palettes share the same layout and text-overflow tests.
- Only illustration ROI x=50–1029, y=431–1125 is altered during chapter 7 (16.633–19.167 s). Existing subtitles, narration panel, headers, footer, eight chapters, and AAC bitstream are preserved.

## Offline reproduction
```bash
python quality/cycle1239/code/save_reuse_panel.py \
  --source cycle1237_CLEAN_BEFORE_AFTER_HUMAN_REVIEW.mp4 \
  --output cycle1239_SAVE_REUSE_CLARITY_HUMAN_REVIEW.mp4 \
  --report qa1239.json
python -m unittest discover -s quality/cycle1239/tests -p 'test_*.py' -v
python quality/cycle1239/tests/ci_smoke.py
```

The actual source MP4 is not stored in this public repository, to avoid distributing unreviewed media. The finished MP4 is supplied separately for human review. CI uses an original synthetic test video, not the finished asset.

## Local verified output
22.237 s; 1080×1920; 30 fps; 667 frames; 8 chapters; AAC bitstream SHA-256 `81d4fe4994db105fe81fca9a47ec470c0f245a39c0c16a4be0da2ed5cf3055b3`; local 9/9 tests; full audio/video decode PASS. Actual narration transcription and subtitle meaning/timing are NOT verified.

## Publication gate
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Reference v33 original, source rights, smartphone playback, and employee approval are not verified. No automatic posting, paid API, or merge.
