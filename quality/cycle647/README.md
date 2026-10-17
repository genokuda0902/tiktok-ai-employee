# cycle647 — Audio-aware scene cuts (DRAFT)

This cycle adds a reusable audio-energy scene-boundary helper supporting 10 genres.
The rendered 1080x1920 H.264/AAC MP4 (15.6 seconds, 8 scenes) and the complete local renderer, assets, and tests are provided in the separate downloadable ZIP.

## Difference from cycle646
- Scene cuts are shifted by at most 12 frames to nearby low-energy moments in the existing Japanese audio.
- Mean RMS at 7 cuts: 0.011782 before; 0.008870 after (about 24.7% lower).
- New slides use a single large editorial caption and reduced visual clutter.
- Japanese audio was REUSED, not synthesized. These are editorial captions, NOT verified transcriptions.

## Local QA
- 15/15 technical checks passed, 7/7 local regression tests passed.
- Full video/audio decode passed; 1080x1920, H.264, AAC 48kHz, 468 frames.
- The cut heuristic does not establish spoken sentence boundaries or content-level narration/caption agreement.
- New narration, smartphone playback, visual parity with reference clips, and rights verification are pending.

## Publication controls
HUMAN_REVIEW / NOT_APPROVED. No auto-posting, merge, payment, or rights approval. Employee must review before any manual posting.
