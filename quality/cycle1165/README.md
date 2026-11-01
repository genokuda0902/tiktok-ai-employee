# TikTok image-slide quality cycle1165 — human review only

## Distinct change
Cycle1163 repaired doubled Japanese status-strip text in scene05 (48 frames). Cycle1165 adds seven **cyan light sweeps along the chapter-title divider**, one per detected scene cut (frames 42,94,168,250,330,412,499), each 13 frames. The effect is confined to x70–889, y354–381, outside subtitles and narration. No new claims, personal data, third-party images, or paid assets.

## Local actual-MP4 QA
- Real review file: cycle1165_CHAPTER_DIVIDER_SWEEP_HUMAN_REVIEW.mp4 (provided separately, not committed).
- H264, 1080×1920, 30fps, 675 frames, 22.5s, full video/audio decode: PASS.
- Japanese-tagged AAC 48kHz copied bit-for-bit (ADTS SHA256 equal).
- Caption/footer protected region (y>=1120) maximum per-frame mean difference 0.7086/255, due to lossy video re-encoding.
- Seven transition midpoint header mean differences 7.953–9.185/255.
- 12/12 local tests PASS; 10 genre presets; only one genre rendered.

## CI limitations
GitHub Actions uses **synthetic** 22.5s H264/AAC input and tests unit tests, render, frame count, resolution, full decode. Private MP4 and Japanese speech are not available in CI.

## Research and references
Previously accessible TikTok market-analysis/video-research summaries emphasize first 1–1.5s hook, 15–25s duration, legible Japanese captions, live UI proof, Before/After. User-provided 16-panel ChatGPT×Excel storyboard includes richer people/robot/live UI than the current 8-scene video. Original v33 reference MP4 was not accessible for direct comparison.

Independent Japanese ASR, caption semantics/timing, source commercial rights, phone playback, employee approval, and Actions billing remain unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No automatic posting, paid service contract, or merge.
