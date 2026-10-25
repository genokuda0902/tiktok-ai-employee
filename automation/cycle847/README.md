# Cycle847: independent native-vector TikTok slides (review only)

## Change from cycle846
Eight **new independently generated 1080x1920 vector editorial slides** replace the reused photo cards in a separate creative route. They use eight different AI-work visual concepts, a common ten-genre palette, original vector graphics, and strict review-only gates. The local MP4 includes 7 full-scene dissolves (9 frames each), the inherited Japanese AAC voice and 24 time-coded Japanese subtitle beats.

## Scope of this PR
`editorial_core.py` is a compact, reproducible common-layout reference and `test_editorial_core.py` checks the ten genres, native size, 8 scenes and fail-closed safety. **It is not the byte-identical local video renderer**: the full 8-illustration production renderer, actual slide PNGs, captions, QA and MP4 are delivered separately in the cycle847 ChatGPT ZIP. This avoids uploading unapproved media. CI tests this compact core only; it does not generate or certify the Japanese MP4.

## Local verification (outside CI)
1080x1920 H.264 30fps, 691 frames / 23.033s, AAC 48kHz 23s, 24 captions, 8 unique native PNGs, 7 transitions, full A/V decode, 16/16 local QA checks, 16/16 local production tests. Source narration AAC bitstream preserved. This is a new vector design, **not 8 new photorealistic photographs**.

## Safety / outstanding
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid API, billing, external media upload, or automatic posting. Japanese voice naturalness, exact speech-caption semantic sync, smartphone playback, original reference parity, original narration rights and employee approval are unverified. Manual publication only after approval.
