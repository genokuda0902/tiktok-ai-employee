# cycle1042 — proof-first three-cut teaser / PRIVATE HUMAN REVIEW ONLY

## Research and provenance
- Based on automation chain cycle1040 PR #441; parallel quality-chain PRs #440, #442 and #443 left untouched. Main at inspection: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Consulted accessible summaries of previous TikTok市場分析 and TikTok動画研究: strong 0–1.5s hook, one message, purpose-driven short cuts, actual UI, Before/After, readable Japanese captions and manual staff approval.
- Directly inspected user's original ChatGPT×Excel時短術16コマ絵コンテ.png: 16 panels, approximately 36 seconds, cinematic 3D robot/human, real UI demonstration, chart, Before/After and CTA.
- Full research chat/task transcripts and original v33 MP4 inaccessible. Original v33 source not recovered; this is a reimplementation.

## Unique change versus cycle1040
- Keep cycle1040's original robot intro 0–1.5s.
- Replace only frames 45–86 (1.500–2.900s) in upper picture (y < 1280) with three 14-frame source-derived proof cuts:
  1. completed-output example from original frame 195,
  2. completed AI prompt from frame 328 (the incomplete-typing frame 294 was rejected),
  3. manual Calc verification from frame 483.
- The source-derived screenshots come from the same SHA-locked private review MP4; no third-party material is introduced. This is a teaser, not an independent claim of factual results.
- All existing Japanese burned captions and original AAC are preserved. Source frames beyond 2.9s are unchanged in content except re-encoding drift.
- Ten genre-specific palettes tested; actual private video is only ai_work. Other genres fail closed until approved source media exists.

## Actual local MP4 (NOT uploaded to public GitHub)
- Input SHA-256: ac8cc088a379d21903b2bef186c451aa4d2b3acbe937c30cffb0b796d28702b4.
- Output SHA-256: 2bf5b682b427da56ce87ce0ea41e07c99298b1d42aa97ab1c21acd185cb02b1d.
- H.264 1080×1920 30fps, 691 frames / 23.033333s, AAC 48kHz Japanese tagged, full A/V decode PASS.
- AAC elementary ADTS SHA identical to input: ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e.
- All-frame 270×480 comparison: upper teaser mean absolute difference 56.1919/255, outside-teaser upper max 1.3247/255, protected lower caption max 1.1573/255.
- Eight SRT cues, no overlap, last cue ending 23.033s; audio signal measured in each cue. This is not Japanese ASR, pronunciation validation or semantic/timing alignment of spoken words.
- Six local unit tests PASS. GitHub Actions CI validates tests and a synthetic 2s H264/AAC clip, not this private 23s MP4.
- Review MP4 and comparison image are shared as ChatGPT conversation artifacts only; no private media committed or uploaded to public GitHub.

## Reproduce with private input
python cycle1042/source/proof_first_teaser.py --source PRIVATE_CYCLE1040.mp4 --dest PRIVATE_CYCLE1042.mp4 --report qa.json --expected-sha ac8cc088a379d21903b2bef186c451aa4d2b3acbe937c30cffb0b796d28702b4 --review-only

python cycle1042/source/verify_proof_teaser.py --source PRIVATE_CYCLE1040.mp4 --dest PRIVATE_CYCLE1042.mp4 --srt captions_review_only.srt --report roi_qa.json

## Gates and next
- Missing independent Japanese ASR/transcription, speech–caption semantic/phoneme alignment, original reference v33 direct comparison, inherited source media publication rights, smartphone playback, staff approval, retention measurements and actual Actions billing.
- Current 8-chapter / 23s output still differs significantly from reference 16-panel / ~36s cinematic human/robot visuals.
- Next: acquire an approved offline Japanese ASR model or arrange manual 8-cue speech review, then add distinct rights-approved high-quality image-first shots. Do not repeat the same 3-cut teaser.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, automatic posting, public private-media upload, paid API, contract or purchase.
