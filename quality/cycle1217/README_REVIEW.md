# Cycle 1217 — Japanese narration loudness mastering (REVIEW ONLY)

**Distinct from cycle1215:** Previous cycle aligned 8 H.264 keyframes to scene starts and reduced file size. This cycle changes **audio mastering only**: two-pass FFmpeg `loudnorm` to about -16 LUFS, with a -1.5 dBTP target. The H.264 bitstream, all burned-in Japanese subtitles, slide visuals, scene keyframes and 8 chapter markers are unchanged.

## Actual local 22.5s review MP4 (not uploaded to GitHub)
- Source: cycle1215 review MP4; output: `cycle1217_VOICE_LEVEL_HUMAN_REVIEW.mp4`.
- Integrated loudness **-16.85 → -16.04 LUFS** (+0.81 LU).
- True peak **-1.59 → -1.46 dBTP** (within +0.15 dB measurement tolerance of -1.5 dBTP target).
- H.264 1080×1920, 30fps, 675 frames, 22.5s; 8 chapters unchanged; video elementary bitstream SHA256 identical; Japanese AAC 48kHz.
- Full video/audio decode PASS; local 8/8 unit tests and synthetic 3s encode/master/decode PASS.
- The first render had a **22.6s AAC tail**; fixed with output trim to source video duration, re-rendered and verified at **22.5s**. Retain regression test for duration in next cycle.

## Prior research/reference
Accessible `TikTok市場分析` / `TikTok動画研究` summaries emphasize a 1–1.5s hook, short 15–25s story, genuine UI evidence, Before/After and legible Japanese captions. User's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` was previously inspected; the original v33 MP4 is unavailable. This cycle does not claim reference-level quality or full 16-panel equivalence.

## CI and safety
CI executes 8 unit tests and synthetic 3s 1080×1920 A/V test; it does **not** run on or upload the private 22.5s MP4. Mastering is genre-agnostic across `ai,business,money,learning,health,food,travel,beauty,career,life`; only `ai` real MP4 was rendered.

No independent Japanese ASR transcript/semantic subtitle timing test (no offline ASR model available), commercial rights clearance, physical smartphone playback, employee approval, or GitHub Actions billing confirmation. No external imagery, paid services, merge, or auto-post. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**; manual posting only after staff approval.
