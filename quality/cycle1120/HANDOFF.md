# cycle1120 — single-caption compatibility, REVIEW ONLY

## Research and context
- Accessible prior summaries of **TikTok市場分析** and **TikTok動画研究** emphasize first-second hooks, meaningful cuts, real UI, readable Japanese captions, manual employee review. Full original task/chat transcripts were unavailable.
- User's 16-panel / ~36s ChatGPT×Excel storyboard was described and reviewed in prior Library results, but the original reference v33 MP4 was not accessible for direct comparison in this run.
- Checked main PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py, open PRs #519 and #520. Main's daily generator remains silent (-an) and is NOT v33.
- This branch stacks on unmerged #519 (commit 9f7151c); parallel PR #520 is untouched.

## Distinct finding and change vs cycle1118
- The cycle1118 MP4 has H264 + AAC + mov_text and its sole soft subtitle stream is **default=1** in ffprobe, despite an attempted disposition=0. Some players may double-display the already burned-in Japanese captions.
- The new export keeps the existing burned-in Japanese captions and H264/AAC elementary streams byte-identical but removes the soft subtitle track from the primary review MP4. SRT remains a separate optional text file, explicitly **NOT independent ASR**.
- Ten genres use the same fail-closed SHA guard, no-overwrite rule, H264/AAC full-decode and stream-identity QA.

## Actual private review result (NOT committed)
- Source SHA256: 0bad2e8a6940458a98e13aa6c5e38208145aef53580ab194d8f4193861c7eb22
- Result SHA256: 8aa7ec8fb2c3db22a924c8be1762de5ba0529a794f36b29cea434a609fc70449
- SRT SHA256: 124eb227de0803fc771919566eca459a2f7499a95bc779ed4c39ad9622034177
- 23.033333s / 691 frames / 1080x1920 / 30fps H264 / 48kHz AAC; full A/V decode PASS; H264 and AAC bitstreams unchanged; output subtitle streams=0; local 6 tests PASS.
- GitHub Actions only tests synthetic 1.2s color + tone media, NOT this private MP4.
- Private review MP4/SRT/verification JSON shared in conversation only. No confidential media committed.

## Unresolved gates
- Spoken Japanese independently transcribed and aligned to on-screen captions: NOT VERIFIED.
- Original v33 MP4 comparison, phone playback, media/voice rights, employee approval, Actions actual billing: NOT VERIFIED.
- Current 8-scene/23s review master remains visually less varied than the 16-panel/~36s storyboard.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, auto-post, paid contract, or public upload of private media.
