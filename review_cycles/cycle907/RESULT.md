# cycle907 — three-act story rail + independent Japanese ASR fail-closed gate

Date: 2026-10-28 JST. Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Research / prior work
- Consulted accessible summaries of TikTok市場分析 and TikTok動画研究, and directly inspected user Library image ChatGPT×Excel時短術16コマ絵コンテ.png (16 visual panels). Full research chat/task transcripts and original v33 MP4 not accessible.
- Reviewed main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PRs including #279/#277, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and src/build_daily.py (still silent -an).
- cycle906 previously introduced 3-stage proof UI within scene05. This cycle instead adds an always-visible 3-act narrative orientation rail in upper y28–100, x355–715, highlighting 課題 / 手順 / 確認 at 0, 5.667 and 17 seconds, without intentionally covering captions.

## Actual private local MP4 (NOT committed)
- Input cycle906 SHA256: 9594572d211c14d7bdcd292a251ce16c50fb9cf069b76c5286c4a4cde49b261e.
- Output cycle907 SHA256: 4a3b86f703e788cf578acc98f747a7499e83bcb769bbabf11bb5c15807bbbf70.
- H264 1080x1920 30fps 691 frames 23.033333s, inherited Japanese AAC 48kHz; full A/V decode PASS; AAC elementary stream unchanged.
- All 691 frames changed in top rail ROI (mean sampled pixel MAE 49.852). Subtitle region y1280+ max per-frame sampled MAE 0.418 from re-encoding, not direct overlay. Other region average sampled MAE 0.427.
- 16 local tests PASS. CI tests code and PNG smoke only; it does NOT contain or test private finished MP4.

## Japanese speech / caption audit
- New independent-ASR vs subtitle cue comparison function normalizes Japanese Unicode, compares text similarity and timing drift, rejects missing ASR by default. **No independent Japanese ASR model or verified transcript was available. Actual output returns INDEPENDENT_JAPANESE_ASR_MISSING, so semantic/timing match is NOT VERIFIED.** This is a safety improvement, not proof of alignment.

## Safety and remaining gap
- Source media rights, privacy approval, employee approval, smartphone playback and actual GitHub Actions billing are unverified.
- This is a reimplementation, not recovered v33 source; no real 16-cut cinematic footage, original robot, or real ChatGPT/Excel operation recording. Ten genre identifiers tested; only AI-work full video rendered.
- No merge, auto-post, paid service, or public upload of inherited private media.
- Next: obtain a rights-cleared Japanese ASR model/transcript, run actual caption semantic/timing checks, then build original approved image-first scenes to close the 16-panel gap.
