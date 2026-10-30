# cycle1028 — storyboard-aligned finished-output scene (review only)

2026-10-31 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original reimplementation, not recovered v33 source. No merge, paid service, confidential-media upload, or TikTok posting.

## Research and reference
- Consulted accessible summaries of TikTok市場分析 / TikTok動画研究: 0–1.5s hook, purposeful cuts, real UI, Before/After, readable Japanese subtitles, retention/save/CTA feedback, employee-reviewed manual posting. Full original research chat/task transcripts inaccessible.
- Directly viewed user-provided ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels, about 36s; 3D robot/person, app demo, before/after, charts, CTA). Original AI_Jitan_v33_REAL_SPREADSHEET(1).mp4 unavailable; no direct original-video comparison.
- Read main PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, .github/workflows/daily-v2.yml (legacy, not proof of v33), prior cycle1026 source/test/PR #427 and parallel #428. Do not merge either.
- PR #427 CI run https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/41111848655 completed SUCCESS, correcting the prior queued report.

## Distinct change versus cycle1026
- Cycle1026 highlighted A=46/B=29 calculation while the Japanese subtitle at 5.8–8.52s said 「次に、完成形の見本を用意する。」 (visual/narrative mismatch).
- Cycle1028 replaces ONLY scene03 picture area at 5.95–8.52s with a two-beat finished-output sample: (1) decide spreadsheet columns, (2) show totals and review field. Values explicitly fictional; this is not a real UI recording.
- Generates Japanese panel art locally using Pillow/Noto CJK and composites with FFmpeg fades. Preserves burned Japanese subtitles (y>=1490), original AAC bitstream and other scenes.
- Ten genre text presets supported; full actual MP4 rendered only for ai_work. Does NOT claim Japanese speech-to-subtitle alignment.

## Local verified artifact
- Input SHA256: 69d56c2cbfe9047b83700d20e11a7c906ea117ee1c703dad18ddbddea8143657.
- Output SHA256: 49c1d5aaf88e62ad2d8faff04cada0c97dc00b15f2dc1bd99cd2820a1b3c93b7.
- 1080x1920 H.264 30fps, 691 frames, 23.033333s, AAC 48kHz Japanese-tagged. Full A/V decode PASS, AAC elementary stream SHA identical.
- 8 local unit tests PASS, 2s synthetic render/decode PASS.
- 21 sampled frames: changed scene picture ROI MAE mean 46.217/255 across 9 changed samples; burned caption ROI max MAE 0.5618/255; outside changed scene ROI max 0.88/255. Visual inspection at 7.75s PASS for readable sample and preserved bottom subtitle.
- Source assets' publication rights, smartphone playback, employee approval, Japanese voice semantic/phonetic match, actual GitHub Actions charges: NOT VERIFIED. **Do not publish.**

## Reproduce with private review media

Install Pillow 11.3.0 and free FFmpeg/Noto CJK, then run:

    python -m unittest discover -s cycle1028/tests -v
    python cycle1028/source/storyboard_match.py --source /private/cycle1026_SPREADSHEET_PROOF_FOCUS_JP_REVIEW_ONLY.mp4 --output /private/cycle1028_STORYBOARD_MATCH_JP_REVIEW_ONLY.mp4 --report /private/cycle1028_qa.json --genre ai_work --expected-source-sha 69d56c2cbfe9047b83700d20e11a7c906ea117ee1c703dad18ddbddea8143657 --review-only

## Next
1. Obtain independent Japanese speech transcript or documented human listening check of all eight caption segments; do not equate audio waveform presence with Japanese speech accuracy.
2. Improve visual variety with approved high-quality image-first material, without unapproved private assets.
3. Check smartphone playback, rights and employee approval before manual posting.
