# cycle948 — first-second hook reveal repair (HUMAN_REVIEW ONLY)

**Date:** 2026-10-29 JST. **PUBLICATION_NOT_APPROVED.**

## Why this differs from cycle947
Cycle947 added a mild camera push in eight scenes. In its opening scene the right-hand AFTER card was obscured by a dark reveal for much of the first 1.5 seconds, weakening the first-second hook. This cycle replaces only that panel with a clean later frame taken from the **same** private MP4, then fades back to the original at 1.98–2.18 s. No new claims, copyrighted music, auto-posting, external media, or synthetic replacement of actual UI.

## Local verified private review output (NOT in GitHub)
- Input cycle947 MP4 SHA256: a2e786cf9586af97e5771bd41920c5ccc770f2ec4cac09615ecb675e9155dcc5
- Output cycle948 MP4 SHA256: 94384406b7f4daafae16201d351fe68658800a7a363ee2f35417d4e1e77ebf10
- Video H.264 1080x1920 30fps 691 frames 23.033333s; audio AAC 48kHz stereo.
- Full video and audio decode PASS; extracted AAC elementary stream SHA256 unchanged: 37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27.
- First-second AFTER panel grayscale mean at frame 9 (0.3s): **26.35 → 56.69**; frame 21 (0.7s): **26.35 → 56.69**. This is a measured visibility change, not an engagement claim.
- 63 frames have panel-region mean difference >2 (1/4 sample); none after frame 70. Protected subtitle region max mean difference 0.868 (1/4 sample), attributable to re-encoding. No subtitle pixels deliberately edited.
- Local 17/17 tests PASS. GitHub CI runs only code/unit tests, **not** the private MP4.

## Reproduction
Use an explicitly inspected, pinned, review-only 1080x1920 30fps 691-frame source. The hard-coded rectangle/timing is approved for this one fictional AI-work example only; other genres must supply their own reviewed geometry. The shared geometry validation and compositing algorithm support ten genre labels; do not blindly reuse the same rectangle for different content.

\`\`\`bash
python -m pytest -q cycle948/tests/test_hook_reveal_repair.py
python cycle948/src/hook_reveal_repair.py \
  --source /private/cycle947_FOCUS_MICROBEATS_JP_REVIEW_ONLY.mp4 \
  --source-sha256 a2e786cf9586af97e5771bd41920c5ccc770f2ec4cac09615ecb675e9155dcc5 \
  --patch /private/cycle948_patch.png \
  --output /private/cycle948_HOOK_REVEAL_REPAIR_JP_REVIEW_ONLY.mp4 \
  --qa /private/qa948.json
\`\`\`

## Research, reference and safety
Read accessible previous \`TikTok市場分析\` and \`TikTok動画研究\` summaries: first 1.5-second hook, purposeful short cuts, real app demonstrations, readable Japanese captions, human approval. Full task/chat text unavailable. Directly viewed the user's 16-panel \`ChatGPT×Excel時短術16コマ絵コンテ.png\`; original v33 MP4 not accessible. Read \`PROJECT_HANDOFF.md\`, \`recovery/v33/RECOVERY_STATUS.md\`, current \`src/build_daily.py\`, and open PRs. Main remained 18e084c38db0dc55db7dfc0532b9451b1167f2aa; original daily builder still silent. This reimplementation remains an 8-scene, 23-second motion-graphic video, **not** reference-equivalent cinematic 16-scene footage.

No independent Japanese ASR/transcription or spoken-caption semantic alignment: no offline ASR model installed. Audio is technically preserved, not semantically validated. Smartphone playback, inherited asset rights, employee approval, and actual GitHub Actions charges are unverified. No merge, posting, paid services, or publication.
