# cycle912 — mobile-readable real Calc source magnifier (REVIEW ONLY)

## What changed vs cycle911
cycle911 used three actual local LibreOffice Calc screenshots in scene02, but the formula bar and cell B5 were small at mobile viewing scale. cycle912 replaces **frames 87–173** with a pixel-backed 3-stage magnifier: (1) fictional source rows and totals, (2) selected B5 value 46, (3) actual formula-bar text \`=SUM(B2:B4)\` plus referenced cells 12/16/18. Original narration and subtitle band are retained. Ten accent presets exist; **only ai_work was rendered and inspected**.

This is not a Microsoft Excel recording or proof of productivity gains. Source screenshots are from a self-created fictional workbook. Source assets, screenshots, voice and final MP4 remain in private ChatGPT review attachments, not GitHub.

## Local reproduction
Requires FFmpeg, Pillow, Noto Sans CJK and the separately approved/private source inputs:

\`\`\`bash
python3 -m unittest discover -s review_cycles/cycle912 -p test_cycle912.py -v
python3 review_cycles/cycle912/legible_calc_focus.py \
  --source /private/cycle911_REAL_CALC_CAPTURE_REVIEW_ONLY.mp4 \
  --output /private/cycle912_CALC_MAGNIFIER_JAPANESE_REVIEW_ONLY.mp4 \
  --expected-sha 4587ba15fb3a3cf871e486eb9caec884efdfeac8ec74898c927bf02a88c1a28d \
  --captures /private/calc_01.png /private/calc_02.png /private/calc_03.png \
  --frames-dir /private/cycle912_frames --genre ai_work
\`\`\`

## Verified private review output (2026-10-28 JST)
- Output SHA256: \`457e001264d9bbdebcb8751243fc5628e0c5e8bff1f18abd770c6cda4b3eb80f\`
- Source SHA256: \`4587ba15fb3a3cf871e486eb9caec884efdfeac8ec74898c927bf02a88c1a28d\`
- 1080×1920 H.264 30fps / 691 frames / 23.033333s, inherited AAC 48kHz.
- Full video and audio decode PASS. Original and new AAC ADTS SHA256 identical: \`2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9\`.
- All 691 frames compared at 1/4 resolution. All 87 target frames changed (minimum scene mean absolute difference 48.029); outside-target maximum 1.405, caption-region maximum 0.929.
- 15 local stdlib tests PASS. Eight private per-scene audio clips and a caption review CSV prepared for a human reviewer. These are **not independent ASR** and do not establish spoken-text/subtitle semantic alignment.
- CI checks source/policy only; **the completed private MP4 is not CI-tested or uploaded**.

## Research and publication gate
- Accessible prior summaries of TikTok市場分析/TikTok動画研究: hook in first 1–1.5s, short purposeful cuts, real UI, Before/After, readable Japanese captions, employee-reviewed manual posting. Original task/chat transcripts inaccessible.
- User's original 16-panel \`ChatGPT×Excel時短術16コマ絵コンテ.png\` directly inspected this cycle. Original v33 MP4 unavailable. 8-scene review is still far below reference cinematic person/robot visuals and 16-shot diversity.
- Binding documents: \`PROJECT_HANDOFF.md\`, \`recovery/v33/RECOVERY_STATUS.md\`. Original v33 source unrecovered; this is a **reimplementation**.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Unverified: independent Japanese ASR, subtitle meaning/timing, inherited media publication rights, employee approval, phone playback, actual Actions charges. No merge, posting, paid contract, or public private-media upload.
