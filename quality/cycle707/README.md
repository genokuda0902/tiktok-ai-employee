# Cycle707: process Before/After proof (REVIEW ONLY)

**Baseline:** cycle706 (20s, 1080x1920, 30fps, synthetic sales data).  
**Change:** animated process-comparison card during 17.5–20.0s, replacing the static end card. This shows manual steps vs AI-assisted steps **without claiming measured time savings**.

## Files
- `before_after.py`: genre-neutral process-comparison overlay and fail-closed claim validation.
- `test_before_after.py`: unsupported numeric/performance claims, caption length, scene animation bounds, and 10-genre configuration regression checks.

## Verified local output (not committed to GitHub)
- `cycle707_before_after_BGM_ONLY_REVIEW_ONLY.mp4`
- SHA-256: `bb098b5f2b7d1ed6ad7ca316d92a7abf9b13db9046d333be17a175e71343a0d4`
- 20s, native 1080x1920, H.264 30fps, AAC BGM-only; all 600 frames decoded.
- 7 local pytest cases passed.
- 19s image difference vs cycle706: mean absolute RGB difference 14.78; 16.2s unchanged frame: 0.0.
- Local full render source and QA bundle are available in the ChatGPT run attachment, **not in GitHub**.

## Blockers and release gates
- No Japanese narration: local Open JTalk unavailable and free gTTS connection failed. Captions are timed to scenes, **not speech-synchronized**.
- GitHub Actions workflow creation was blocked by connector safety checks. **No CI run / Actions artifact**.
- No verified v33 reference MP4 comparison, no mobile-device test, no human publication approval.
- The reference 16-panel storyboard was inspected for creative direction only; reference pixels were not embedded.
- No merge, posting, private media, or paid services.

## Reproduction
The local renderer is a reimplementation derived from cycle706 source, imports `before_after.draw_comparison`, and invokes it for the last scene. To reproduce exactly, use the attached full renderer and test bundle; this repository currently stores only the reusable overlay and its regression tests. Do not represent this as a reproducible clean GitHub build until the renderer and CI are checked in.

Next: recover zero-cost Japanese TTS, synchronize narration to captions, commit the full renderer and CI, then compare visually against the approved v33 source.
