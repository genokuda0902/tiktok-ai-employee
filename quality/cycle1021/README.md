# cycle1021 — audio-reactive VOICE meter (HUMAN_REVIEW)

Source: cycle1019 local 22.5s, 1080x1920, 30fps, Japanese AAC 48kHz and burned-in subtitles.

## Change vs cycle1019
- cycle1019: scene06 timed red/teal BEFORE→AFTER glow outlines.
- cycle1021: top VOICE bars are now driven by the decoded real narration's 30fps RMS envelope, with a short attack/release and silence gate. Replaces decorative animation only in x574..718, y73..108.
- No new text, soundtrack, images, third-party assets or external APIs.
- Ten genre colors are configurable; only ai_work has been rendered as a full-length MP4.

## Local full-length QA
- 22.500s; H.264 1080x1920 30fps, 675 frames; 8 chapters; AAC 48kHz.
- Full A/V decode PASS; audio bitstream identical (stream copy).
- Audio amplitude / cyan-meter correlation: 0.6506 → 0.7946 (sampled all 675 frames).
- Max sampled subtitle-region mean absolute pixel difference: 0.644/255.
- Max sampled other-scene region mean absolute pixel difference: 1.228/255.
- Six unit tests PASS.
- The real 22.5s MP4 is delivered in the chat's local artifact, **not** in this public GitHub repository.
- GitHub CI tests a synthetic 2s MP4 only, not the private full video.

## Not verified
Independent Japanese ASR, speech-to-caption semantic timing, v33 reference original, media rights, smartphone playback, employee approval, actual Actions charges, audience retention and perceived quality.

Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, payment or automatic posting. Employee approval is required before manual posting.
