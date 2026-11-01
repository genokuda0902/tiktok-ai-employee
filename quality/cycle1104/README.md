# cycle1104 — truthful numeric proof repair (REVIEW ONLY)

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. This is a reimplementation, not recovered v33 code. No merge, publication, unapproved media distribution, auto-posting or paid services.

## Distinct change vs cycle1102
Direct visual inspection of the actual cycle1102 MP4 found a persistent numeric inconsistency in scene06: the fictional spreadsheet shows sales A=46 and B=29, total 75, but intermediate cards briefly displayed 25 and 26. This persisted despite the earlier cycle1092 attempt.

At 14.3–17.333 seconds, the three numeric cards are replaced with strict manifest-driven values. Stage 1: 46 + 29 = 検算中; stage 2: 46 + 29 = 75. Source Calc footage and the lower Japanese subtitle area are preserved. The generic numeric-proof component validates arithmetic, privacy/review-only status and ten genre-specific palettes; it is not an identical full-video template for ten genres. Only ai_work was rendered as a complete MP4.

## Reproduction
Requirements: Python3, Pillow, FFmpeg/ffprobe, Noto Sans CJK.
Run: cd quality/cycle1104 && python3 -m unittest -v test_truthful_numeric_proof.py
Render: python3 truthful_numeric_proof.py --source /PRIVATE/cycle1102.mp4 --source-sha fe10b5dfe6ddab7fe1de208146eea5fe62147fded29ed8ddb7de6ff6c0ff3ca6 --manifest manifest.json --out /PRIVATE/cycle1104.mp4 --report /PRIVATE/qa.json

Private input SHA256: fe10b5dfe6ddab7fe1de208146eea5fe62147fded29ed8ddb7de6ff6c0ff3ca6.
Private output SHA256: 074d169d08cb74778b314592d97a07cfd7b769574bbe64c0c08d9175a43c87f1.
Local actual MP4: H264 1080x1920 30fps, 691 frames / 23.033s, AAC 48kHz. Entire A/V decoded; ADTS audio bitstream unchanged. 12 local tests passed. All 691 frames decoded for visual QA: sampled caption-region max mean pixel difference 0.4938/255, sampled outside-window max 0.4056/255, changed-card mean 13.4317/255. Private media is not committed to GitHub. CI tests synthetic 18-second H264/AAC only.

## Research and remaining gates
Prior accessible TikTok市場分析 / TikTok動画研究 summaries consulted: 1.5-second hook, purposeful cuts, real UI, accurate before/after, readable Japanese subtitles, employee-reviewed manual posting. Full original chat/task bodies unavailable. User's ChatGPT×Excel時短術16コマ絵コンテ.png directly inspected: 16 panels/~36s, cinematic person/robot, ChatGPT/Excel demos, before/after and CTA. Original reference v33 MP4 inaccessible this run. Current 8-scene/23.03s video does not match the reference's cinematography or scene variety.

Not independently verified: Japanese ASR and eight subtitle semantic/timing matches (especially after 20.3s), pronunciation, inherited media/audio rights, smartphone playback, employee approval, reference-video parity, actual Actions billing. Next: independent offline Japanese ASR if a legitimately available zero-cost model can be used; otherwise manual transcript review. Do not claim a semantic QA pass without evidence.
