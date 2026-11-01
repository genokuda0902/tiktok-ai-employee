# cycle1128 — fictional period consistency correction (REVIEW ONLY)

Source: private cycle1126 23.033s video, SHA256 `68d13d172353e06fa6913a176de347a7eae1e592791fdd460ce760418007fc2e`.
Finished private MP4 SHA256 `8200e485fca3042424b7d6f78d43bbd8b7ec7b3893197a6bee61418d1348ded0`. **The finished MP4 and private source manifest are NOT committed**.

## Difference from cycle1126
The scene04 condition wrongly says "架空の4か月分を比較" while the visible fictional spreadsheet contains April, May and June (three months). Replace the digit "4" with "3" in frames 279–347 (9.300–11.567s). This is a semantic consistency repair, not a claim of improved cinematography. All other scene content and narration are retained. The module validates unique month labels, the claimed/corrected count, genre, exact source SHA, private-review policy, and a safe patch rectangle.

## Reproduction (private, locally held inputs)
```bash
python quality/cycle1128/period_consistency.py \
 --source /private/cycle1126_COMPLETION_REUSE_CUE_JP_REVIEW_ONLY.mp4 \
 --output /private/cycle1128_PERIOD_CONSISTENCY_JP_REVIEW_ONLY.mp4 \
 --manifest /private/source_manifest.private.json \
 --report /private/qa1128.json
```
Manifest keys: policy, asset_approval, source_sha256, genre, period {month_labels,claimed_month_count,corrected_month_count}, patch {start_frame,end_frame,digit_bbox,digit_origin,replacement}. Geometry for this example: 1080x1920, frames 279..347, bbox [301,694,334,737], digit_origin [306,691]. Never commit private manifest/source media.

## Local verification
10/10 unit tests including synthetic 2-second H.264/AAC render PASS. Completed private MP4: H.264 1080x1920 30fps, 691 frames, 23.033s, AAC 48kHz Japanese-tagged; full A/V decode PASS, AAC ADTS bitstream unchanged, 0 soft subtitle streams. All 69 targeted frames show changed digit; sampled caption-region max mean difference 0.720/255; other-frame max sampled mean difference 0.976/255 from re-encoding. Human visual inspection of 10.0s crop confirms 4→3.

## Research, scope and limitations
Consulted accessible summaries of TikTok市場分析 and TikTok動画研究 and directly viewed user 16-panel Excel storyboard. Original v33 MP4 and full chat transcripts unavailable. Reference has 16 storyboard panels / ~36s and richer cinematic visuals; current 8 scenes / 23s remains substantially different. Independent Japanese ASR/semantic speech-caption matching, rights, employee approval, actual phone playback, and billing are NOT VERIFIED. CI tests synthetic media only. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, posting, paid service, or confidential asset upload.
