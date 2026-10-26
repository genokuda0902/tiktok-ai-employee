# cycle861 — local QA checkpoint (2026-10-26 JST)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Private completed MP4 is in the ChatGPT review attachment, NOT GitHub.

## Verified delta vs cycle860

- Source SHA-256: `ae3966da37aebaa243f201bbbcdf967db1167e650fbfb3b2eac6bde704b501c0`.
- Output SHA-256: `bfc5b31ab0a53eb69a57b5b90915254a409a670d6ba2445262517c52365780e3`.
- Scene 2, frames 89–169 (81 frames, 2.967–5.667s): static task checklist replaced with TWO sequential 1.4-second excerpts of genuine recorded Calc/Writer interaction from this same private review source. Dynamic crop, crossfade and large task labels; original fictional data. Not new recordings.
- Other seven scenes unchanged except unavoidable re-encoding.
- 1080×1920 H.264 30fps, 691 frames, 23.033s; AAC 48kHz stereo, ADTS SHA-256 `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9` identical to cycle860.
- Local **10/10 unit tests PASS**; full video/audio decode PASS; **12/12 technical QA checks PASS**. Sample changed-picture mean pixel difference 91.69–106.96; protected Japanese caption region (y1490–1840) difference 0.183–0.322; outside changed scene mean difference 0.488.
- GitHub CI tests synthetic data and a synthetic H.264/AAC MP4; it does NOT render or verify the private finished Japanese video.

## Research provenance and remaining gaps

Accessible summaries from `TikTok市場分析` and `TikTok動画研究`: immediate hook, short purposeful shots, real UI demonstration, Before/After, legible Japanese subtitles and manual employee review. Original full chat/task contents unavailable. User's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` directly opened and inspected; source v33 MP4 not available for this cycle. Current eight-scene video is still much less cinematic and varied than the reference storyboard.

Japanese speech transcription/naturalness and semantic timing with captions, media/voice publication rights, smartphone real-device playback, original reference parity, employee approval, viewer retention and actual GitHub Actions charges remain **unverified**. No auto-post, no merge, no paid service, no public media upload. Next: independently verify narration/caption semantics and add approved distinct high-quality visual sources rather than another UI crop.