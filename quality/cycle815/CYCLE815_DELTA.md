# cycle815 — animated KPI gap review (2026-10-24 JST)

## What changed from cycle814
- cycle814 improved the readability of real LibreOffice Calc footage (3–6 s), but its KPI chart (6–9 s) remained nearly static.
- cycle815 replaces **only frames 180–269** (6.0–9.0 s) with a fully opaque 3-beat KPI overlay: 接続率 18%/25% (7pt short), 成約率 12%/20% (8pt short), 継続率 68%/80% (12pt short). Each is highlighted in turn with an animated target-relative progress bar.
- All values are **fictional**, not customer results. Japanese subtitles remain outside the overlay. Existing Japanese AAC audio is copied bit-for-bit.
- Generic ten-genre accent configuration, safe-area validation, fictional-data opt-in, no posting.

## Local review artifact and QA
- Prior cycle814 input: `66ebd1f7fd81dcdfef2ce1fba09106f91f28fd36140d68cfcc799402fb8feda2` (as reported in cycle814).
- Private cycle815 MP4 SHA256: `c90c94e40af64aeb2932ab70c9b5acf57cae09d9baff8bb157da80a674f91402`.
- 1080x1920, H.264 30fps, 718 frames, 23.933333s, AAC 48kHz, full A/V decode PASS.
- 12 local unit tests PASS; AAC ADTS bitstream identical to prior cycle814.
- Mean RGB pixel difference versus cycle814: 6.4s **8.5018**, 7.4s **9.2201**, 8.4s **9.2136**; unchanged control 4.5s **1.4309**, 9.4s **1.3012**, 16.2s **1.3578** (re-encode).
- Audio signal exists (ffmpeg volumedetect mean -24.8 dB, max -5.9 dB). This does **not** establish accurate Japanese speech or narration naturalness.
- The private Japanese-narrated MP4 is supplied only as a conversation download. GitHub Actions artifacts use synthetic video and sine-wave audio and must not be described as Japanese-narrated output.

## Research and reference provenance
- Prior confirmed summaries of 「TikTok市場分析」「TikTok動画研究」 consulted: first ~1.5s hook, short cuts, actual operations, Before/After, safe subtitles, human review, retention metrics. **Full original task/chat transcripts not accessible.**
- User-supplied 「ChatGPT×Excel時短術16コマ絵コンテ.png」 **directly inspected** this cycle: glossy 3D robot, human/office shots, real operation/UI, chart, Before/After, CTA. New KPI motion addresses only the chart's static presentation.
- Original reference v33 MP4 unavailable this cycle; **no direct comparison** or quality parity claim.

## GitHub and approval
- Latest main checked at `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- Stacked on unmerged PR #122, this cycle's Draft PR #123. No merges.
- CI creates a synthetic-only MP4 and tests; no inherited private audio or capture uploaded to the public repo.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Independent Japanese ASR/caption semantics, visual/voice rights, phone playback and employee approval are pending.
- No billing, contracts or automated TikTok posting.

## Next
Prioritize independent Japanese speech-vs-caption verification and license review, then add licensed/approved cinematic imagery and test against actual v33 reference when available.