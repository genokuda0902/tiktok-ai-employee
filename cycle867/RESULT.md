# TikTok video quality cycle867 — local verified result

Date: 2026-10-26 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Deliverables
- `cycle867_AUDIT_FOCUS_JAPANESE_REVIEW_ONLY.mp4`: SHA-256 `1527220d5092c43d75f6aee756f4773d6618246bf5e81937865f89b52867770b`.
- `before_after867.jpg`, `scene_contact867.jpg`, source renderer/tests/verification.
- Local test: 13 tests passed.

## Delta from cycle866
- Original scene 05 contained over-cropped Calc source rows and a step label hiding the table header.
- Replaced frames 336–421 with original 3-stage proof: source rows → arithmetic → fictional totals 46/29.
- Original 8-scene / 23.033s structure retained, existing AAC audio preserved bit-for-bit at ADTS payload level.
- Entire subtitle area y1490:1840 checked on all 691 frames; max per-frame mean difference 0.113, p95 0.080. Full A/V decode PASS.
- Supports 10 genre-specific headline strings, only AI-work full MP4 generated.

## Research and reference
- Consulted accessible summaries of `TikTok市場分析` / `TikTok動画研究`, not complete transcripts.
- Directly inspected the user's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png`; particularly the realistic prompt, chart, and evidence scenes. Original v33 MP4 inaccessible this run.
- Still not a match for the cinematic, 16-panel photo/robot/scene diversity of the reference.

## GitHub
- Verified main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- Draft PR #219: https://github.com/genokuda0902/tiktok-ai-employee/pull/219
- Base unmerged PR #217; parallel PR #218 left untouched. No merge.
- GitHub Actions run: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40312875211 (check status before citing success).
- Private real MP4 was NOT uploaded to GitHub. CI uses synthetic one-second A/V.

## Limitations
No independent Japanese pronunciation/transcription or semantic subtitle timing verification. No source rights approval, mobile device test, employee approval, v33 direct comparison, or GitHub Actions actual billing verification. No posting or public distribution.