# cycle908 — data-to-chart evidence animation (review only)

Date: 2026-10-28 JST. Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Research / references
- Consulted accessible summaries of 「TikTok市場分析」「TikTok動画研究」: immediate hook, 15–25s, short beats, UI proof, Before/After, safe captions, human review. Full research transcripts inaccessible.
- Directly inspected the user's ChatGPT×Excel時短術16コマ絵コンテ.png: particularly panels 7–9, spreadsheet, chart, Before/After. Original v33 reference MP4 inaccessible.
- Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PRs including #281/#282, PROJECT_HANDOFF.md, archive/v33/README.md, and src/build_daily.py (still uses -an in legacy pipeline). Do not claim v33 equivalence.

## Distinct change from cycle907
- cycle907 added 3-act rail (課題/手順/確認). cycle908 animates data-consistent grouped bars in scene05 from 10.9s to 13.6s, matching the storyboard spreadsheet-to-chart sequence.
- Fictional demo values: 4月 A12/B8, 5月 A16/B9, 6月 A18/B12. The chart displays accurate totals A46/B29. Every frame labels the values 架空データ, not actual business results.
- Supports 10 genre IDs and strict fail-closed checks for rights, ASR, employee approval, and posting. Only ai_work review MP4 generated.
- Images rendered locally with Python/Pillow. Existing source video's rights not independently verified.

## Local verification
- Source cycle907 SHA256: 4a3b86f703e788cf578acc98f747a7499e83bcb769bbabf11bb5c15807bbbf70
- Output SHA256: d811aba20df5c2ef4a43742868035af60f494dc99c10651458da5ac4f5ae25ef
- 1080×1920 H.264 30fps 691 frames / 23.033333s, AAC 48kHz. Full video/audio decode PASS, AAC ADTS bitstream unchanged. 81/691 frames materially changed (327–407). Subtitle region all frames compared at quarter resolution: max MAE 1.3967, p95 1.3652 (re-encode differences). 11 local tests PASS.
- Independent Japanese ASR/transcription, pronunciation, caption semantic/timing alignment, smartphone playback, source rights, employee approval, actual Actions billing NOT VERIFIED. No merge, auto-post, public media upload, paid service or reference-parity claim.

## Reproduce privately
Requires Python 3, Pillow, FFmpeg and Noto Japanese fonts. Keep MP4 local. JSON manifest: genre, synthetic=true, source_sha256, values with A/B three nonnegative integers, all approval booleans false. Run python chart_motion.py --source ... --output ... --manifest ... --work ... --report ....

CI runs policy/math tests without downloading dependencies and does NOT validate the private completed MP4.
