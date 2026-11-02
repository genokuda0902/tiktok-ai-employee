# cycle1162 — efficient H.264 encode, review-only (2026-11-03 JST)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, automatic TikTok posting, paid service, or public private-media upload.

## Reference and prior state
- Accessible TikTok市場分析 / TikTok動画研究 research summaries: hook in first 1.5s, purposeful cuts, real UI, readable Japanese subtitles, Before/After, human-reviewed manual posting. Original full task/chat transcripts unavailable.
- Directly inspected user's ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels, ~36s); original v33 MP4 unavailable, so no direct original-MP4 parity test.
- Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, unmerged PR #561 and parallel #560, PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md.
- Parent branch: quality/cycle1160-scene-parallax (unmerged PR #561); no merge or modification to parallel PRs.

## Change
- Previous cycle1160 optimized illustration-only parallax, but size grew to 9,281,386 bytes.
- New 10-genre fail-closed H.264 medium/CRF21 encode with AAC stream-copy, exact 1080x1920/30fps/frame-count checks, full A/V decode, full-frame SSIM, caption-crop SSIM, audio ADTS SHA equality, and output size gate.
- Source remains local/private. CI creates a synthetic 2s video and does not upload user media.
- This cycle **changes compression, not storytelling or new scene visuals**.

## Real private local MP4 QA
- Source cycle1160 SHA256: 9fbae3325136e0da41e7b8fe55c1f5c816d296c3dd9b2d781d4b06271e762026.
- Output cycle1162 SHA256: 83895018e312dbb1e01b6b8c3ad603f0160aebeff46d515d3dfe656f4d19d614.
- Source 9,281,386 bytes → output 4,489,912 bytes: **51.62% smaller**.
- Both H264 1080x1920, 30fps, 691 frames, 23.033s. Output AAC 48kHz audio ADTS bitstream identical; full A/V decode PASS.
- Full-frame SSIM **0.997425**, caption-region (y1280:1880) SSIM **0.997679**.
- Local 8 unit tests PASS; synthetic 2s full A/V smoke PASS. CI uses synthetic media only.
- Video and before/after comparison shared privately in ChatGPT, not publicly on GitHub.
- Still NOT independently verified: Japanese speech transcription, caption meaning/timing, smartphone playback, source rights, employee approval, actual Actions charges.

## Next
1. Independent Japanese ASR + 8 chapter spoken/caption timing and semantic audit (if an offline model becomes available).
2. Improve approved visual assets / scene variety toward reference; 8 scenes/23s still differs from 16/36s cinematic storyboard.
3. Confirm rights, human review and smartphone playback before any manual posting.
