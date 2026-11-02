# Cycle 1213 — transition deghosting (review only)

**Previous:** cycle1211 focused on 8 action regions. This cycle instead removes double Japanese title/illustration text during 8 scene crossfades.

- Input: privately held cycle1211 22.5s H264/AAC review MP4 (not committed).
- Generic ten-genre renderer; transition frames are supplied as editorial metadata.
- Replaces 88 frames' upper illustration/title region with clean source frames at ±8 frames from each transition. Subtitle/narration/footer region y >= 1140 is never intentionally modified.
- Source AAC elementary stream is copied byte-identically. No external images or media uploaded.
- Local full 675-frame MP4: H264, 1080x1920, 30fps, 22.5s, AAC 48kHz; full video/audio decode PASS. Source/output AAC ADTS SHA256: `fd5646d1d9ba6b340f39d353cf55f711a37393636ca650c78666495683a7239c`.
- Mean title-region L1 difference to clean reference at 24 transition samples: 11.657 before -> 1.267 after; this is a deghosting proxy, not a human readability study.
- Protected region max sampled mean pixel difference: 1.046/255 (lossy re-encode only).
- Initial local attempt froze subtitles and failed protection check (max 9.691/255). Recovered by restricting replacements to y<1140 and rerendering.
- Local tests 12/12 PASS; local synthetic 60-frame render and decode PASS. CI tests synthetic only; full private MP4 remains outside GitHub.

## Unverified / policy

Independent Japanese ASR, narration/subtitle semantic and timing match, reference v33 source MP4 comparison, media rights, phone playback, employee approval and Actions billing are unverified. Prior market/video research accessible as summaries; the full reference MP4 was not accessible.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Do not auto-post, merge without review, buy services, or disclose private assets. Only employee-approved manual posting.
