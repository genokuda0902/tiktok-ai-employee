# cycle1026 — spreadsheet evidence focus (review only)

2026-10-31 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
Reimplementation, not recovered v33 source. No merge, paid service, upload of private MP4, or TikTok posting.

## Verified inputs and reference
- Latest main checked: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- Read `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py` (still silent `-an`).
- Prior completed review PR #425 head: `f644ab0863c8c194974c0ff8b27c2f7ef4e6069b`; its previously queued PR CI #41103233893 now succeeded.
- Parallel unmerged PR #426 edits a different 22.5s video branch. Do not merge or modify it.
- Consulted accessible summaries of TikTok市場分析 / TikTok動画研究. Full original chat/task transcripts unavailable.
- Directly inspected user-supplied `ChatGPT×Excel時短術16コマ絵コンテ.png`: 16 panels, ~36s, cinematic robot/person shots, UI operation, spreadsheet, chart, Before/After and CTA. Original v33 MP4 not accessible in this run.

## Change distinct from cycle1024
- Previous cycle1024 repaired crowded scene02 at 2.90–5.80s.
- This cycle highlights spreadsheet scene03 at 5.95–8.55s, focusing on A=46 then B=29, with a two-beat Japanese evidence banner and a result-card focus ring.
- Uses only inherited private local video, no third-party assets, and retains the original audio bitstream. Burned subtitles stay in y>=1490, untouched by overlays.
- 10 genre labels/configurations and fail-closed guards; only ai_work real 23s MP4 tested.

## Local verified artifact (never uploaded to public GitHub)
- Input SHA256: `9c1fc7d59b767f83eaedbef94bb102df2a88c486bb8b7a2099978a7c59f02cf5`.
- Output SHA256: `69d56c2cbfe9047b83700d20e11a7c906ea117ee1c703dad18ddbddea8143657`.
- 1080×1920 H.264, 30fps, 691 frames / 23.033s, AAC 48kHz Japanese-tagged.
- Full audio/video decode PASS; audio elementary ADTS bitstream matches source.
- 10 local unit tests PASS; synthetic 2s render/decode PASS. CI uses only synthetic media.
- Subtitle semantic/phonetic sync and independent Japanese ASR NOT VERIFIED; source rights, mobile playback, employee approval and actual Actions billing NOT VERIFIED.

## Reproduce locally (private, approved review access only)
```bash
python cycle1026/source/proof_focus.py \
  --source /private/cycle1024_SCENE02_CLARITY_JP_REVIEW_ONLY.mp4 \
  --output /private/cycle1026_SPREADSHEET_PROOF_FOCUS_JP_REVIEW_ONLY.mp4 \
  --report /private/cycle1026_qa.json \
  --expected-source-sha 9c1fc7d59b767f83eaedbef94bb102df2a88c486bb8b7a2099978a7c59f02cf5 \
  --genre ai_work --review-only
python -m unittest discover -s cycle1026/tests -v
```

## Next priorities
1. Obtain independent Japanese speech transcript or human-verified 8-part listen-through and match it to burned captions.
2. Validate licensed/public-safe source assets and smartphone playback.
3. Reduce 16-panel reference's cinematic/photo/UI diversity gap with approved image-first scenes.
4. Keep human approval before manual TikTok posting.
