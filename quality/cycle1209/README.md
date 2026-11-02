# Cycle 1209 — Original scene-transition sound polish (review only)

- **Previous:** cycle1207 central illustration midtone/shadow lift.
- **New:** original 115 ms soft digital page-turn cue at 7 scene boundaries. No downloaded/third-party audio.
- Narration RMS >= 0.06 automatically ducks the cue by 6 dB. Opening hook is kept silent of added effects.
- Video H.264 bitstream is copied without re-encoding; original burned-in Japanese captions, image composition and 1080×1920 remain unchanged.
- Audio is remixed/re-encoded as mono AAC 48 kHz, Japanese-language tag.
- 10 configurable genre pitches share one implementation.
- Unit tests and a synthetic 2-second H.264/AAC smoke test run in GitHub Actions.
- A separate local 22.5-second review MP4 is required for full QA. **The full MP4 is not stored in GitHub**; the synthetic CI smoke is not a substitute.
- Local QA: 675 frames, 30 fps, 1080×1920, H.264 video stream SHA unchanged, full audio/video decoding PASS; non-cue narration correlation 0.999994, 0 ms lag.
- Reference v33 direct comparison, Japanese speech-to-caption semantic verification, rights, smartphone playback, and human approval are **not verified**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid services, or automatic posting.
