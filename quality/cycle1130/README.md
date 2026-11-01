# cycle1130 — formula vs source-cell consistency (REVIEW ONLY)

Previous cycle1128 repaired a 4-month/3-month claim in scene04. This cycle addresses a **different** error left by cycle1124: at 6.0–7.233 seconds, the top instructional overlay shows \`=SUM(B2:B4)\`, but the **selected cell is C5** and the actual visible formula bar reads \`=SUM(C2:C4)\`. Fictional data B2:B4 = 12+16+18 = 46; C2:C4 = 8+9+12 = 29. The screenshot shows 29 in C5. The top overlay is therefore the inaccurate element.

The local private review MP4 corrects the overlay on frames 180–217 (6.000–7.233s) to \`① 数式：=SUM(C2:C4)\`. This does not alter the source spreadsheet screenshot, voice track or burned-in subtitle. The formula/selection/row-total audit is a **10-genre reusable** validation gate; the particular rectangle/font is authored for this example and must be re-reviewed for other videos. It fails closed on wrong source hash, missing private-review policy, bad geometry, wrong totals and mismatched selected cells. There is no OCR or independent ASR.

## Private local QA (not performed by CI)
- Input cycle1128 SHA256: \`8200e485fca3042424b7d6f78d43bbd8b7ec7b3893197a6bee61418d1348ded0\`.
- Output cycle1130 SHA256: \`f20bcd0ca234cc68fa7eec82d6d07aa23775f4c44210a8aa7dcb333b8450b91e\`.
- H264 1080×1920, 30fps, 691 frames, 23.033s; AAC 48kHz Japanese-tagged. Full video/audio decode PASS; original AAC ADTS elementary stream unchanged; no soft subtitle track.
- All 691 frames decoded for before/after comparison; 38 patched frames show formula-region mean pixel difference >=44.5/255. Caption-protected region max mean difference 0.498/255 on changed frames; sampled unpatched frames max full-frame MAE 1.077/255 from re-encode.
- Local tests: 10 PASS (GitHub CI has an additional negative test).
- Completed MP4 is a **private ChatGPT review artifact only**, not committed to public GitHub or published.
- Exact private manifest/source media not committed.

## Reproduce with approved private local inputs
\`\`\`bash
python quality/cycle1130/formula_audit.py \
  --source /private/cycle1128_PERIOD_CONSISTENCY_JP_REVIEW_ONLY.mp4 \
  --output /private/cycle1130_FORMULA_SOURCE_ALIGNMENT_JP_REVIEW_ONLY.mp4 \
  --manifest /private/source_manifest.private.json \
  --report /private/qa1130.json
\`\`\`

Manifest keys: policy, asset_approval, source_sha256, genre, sheet {columns,selected_cell,visible_formula,visible_total,other_total,incorrect_overlay}, patch {start_frame,end_frame,bbox,text_origin}. The private manifest must be authored only from checked source frames and must match the exact source hash.

## Evidence, limitations and next task
- Reviewed accessible past summaries of \`TikTok市場分析\` / \`TikTok動画研究\` and directly viewed the user 16-panel Excel storyboard. Full chat transcripts and original v33 MP4 not available this cycle. The storyboard uses 16 cinematic panels/~36s; current reimplementation remains 8 scenes/23s.
- Independent Japanese speech-to-text and subtitle semantic timing, original v33 visual parity, rights/consent, real phone playback, actual Actions billing and employee approval remain **NOT VERIFIED**.
- CI only tests synthetic H264/AAC media, not the completed private MP4.
- Next: independent Japanese ASR when an offline model is available; then increase image-first visual diversity with approved assets and human review. No merge, auto-post, paid service or private media upload.
