# cycle947 — protected content microbeats (2026-10-29 JST)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Research and previous cycle
- Reviewed accessible summaries of `TikTok市場分析` and `TikTok動画研究`: hook <1.5s, readable Japanese captions, image-first and purposeful cuts; original full chat transcripts unavailable.
- Directly inspected the user's `ChatGPT×Excel時短術16コマ絵コンテ.png`: 16 cinematic robot/person/ChatGPT/Excel panels. Original v33 MP4 unavailable; handoff says original code not recovered.
- Latest main checked: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`; `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, and `src/build_daily.py` checked. Current main daily builder is still silent (`-an`).
- Previous cycle946 added voice-presence EQ and acoustic scene-cut audit; this cycle changes **visual composition** instead, without altering AAC stream. Parallel PR #340 is an independent hard-cut smoothing experiment and was not changed.

## Actual local MP4
- Private file: `cycle947_FOCUS_MICROBEATS_JP_REVIEW_ONLY.mp4`, SHA256 `a2e786cf9586af97e5771bd41920c5ccc770f2ec4cac09615ecb675e9155dcc5`.
- Source cycle946 SHA256 `6c101bd2b00b7ed5a9d6dfa4329d0e64d3a493a48be87c694d761febc0f456e1`.
- H264 1080x1920 30fps 691 frames, 23.033333s; AAC 48kHz stereo, ADTS stream SHA256 identical `37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27`.
- 8 source scenes retained, each with one additional mild 1.055x smooth focus emphasis in second half (366 changed frames). This is 16 *composition beats*, **not** 16 unique narrative shots.
- Full A/V decode PASS. 1/4 sampled max per-frame mean pixel delta in lower protected Japanese subtitle area y>=1460: 1.273; top header y<180: 3.231, attributable in part to re-encoding. Source pixel editing excludes y>=1440, but encoded pixels are not bit-identical. Existing Japanese narration is carried through unchanged; no independent Japanese ASR or semantic timing verification.
- Local tests: 11 PASS; 10 genre intensity presets covered, actual MP4 only for AI-work.
- First trial clipped titles at y240 seam; revised camera target to top-anchored and expanded protected region. Final output re-rendered and visually reviewed at 4 sampled before/after times.

## GitHub and safeguards
- Draft PR #341: https://github.com/genokuda0902/tiktok-ai-employee/pull/341
- Stacked on unmerged PR #339; no merge. Source/test/workflow/README saved. CI tests synthetic arrays, not the private MP4. Private media stays in ChatGPT review attachment, not public GitHub.
- Source commercial rights, employee approval, phone playback, Japanese transcript alignment, actual Actions billing, v33 quality parity: **unverified**. No paid services, auto-posting, external media publishing or confidential asset commits.

## Next
Prioritize **independent Japanese narration transcription and word/phrase-to-caption alignment** using a zero-cost, licensed offline ASR model if available; otherwise keep explicit manual review status. Compare recovered original v33 only if original becomes accessible. Continue work toward approved cinematic images and genuine UI captures rather than further minor cosmetic overlays.
