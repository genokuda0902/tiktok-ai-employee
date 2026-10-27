# cycle913 — guided source-backed Calc annotation (REVIEW ONLY)

## Improvement vs cycle912
cycle912 shows three enlarged real LibreOffice Calc screenshots but they are static. cycle913 adds an **animated, clearly labeled editorial attention guide** to the existing 87 frames (2.9–5.8s): source totals → B5=46 → SUM(B2:B4) formula. The annotation is **not an actual mouse recording**. The screenshots come from a self-created fictional workbook, not Microsoft Excel or a verified customer dataset. No private screenshots, audio, or MP4 are committed.

Ten genre accent presets are implemented; **only ai_work** was rendered and inspected. The source video is inherited from cycle912 and its publication rights are not verified.

## Reproduction with separately supplied private source
Requires Python 3, Pillow, FFmpeg, Noto Sans CJK and source MP4. Do not publish inherited inputs.
\`\`\`bash
python3 -m unittest discover -s review_cycles/cycle913 -p 'test_cycle913.py' -v
python3 review_cycles/cycle913/evidence_pointer.py \
 --source /private/cycle912_CALC_MAGNIFIER_JAPANESE_REVIEW_ONLY.mp4 \
 --expected-sha 457e001264d9bbdebcb8751243fc5628e0c5e8bff1f18abd770c6cda4b3eb80f \
 --output /private/cycle913_GUIDED_REAL_CALC_REVIEW_ONLY.mp4 \
 --frames /private/cycle913_frames --genre ai_work
\`\`\`

## Verified private review result (2026-10-28 JST)
- Source SHA256: \`457e001264d9bbdebcb8751243fc5628e0c5e8bff1f18abd770c6cda4b3eb80f\`
- Output SHA256: \`5a89bcbc8bdb477c1ac70544ba391e9b1f59cd90a5e789a8b8389c571e3e4eb0\`
- 1080x1920 H.264 30fps, 691 frames / 23.033333s, AAC 48kHz; full A/V decode PASS.
- AAC ADTS SHA256 identical before/after: \`2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9\`.
- 87/87 target frames visibly changed (>0.7 MAE at quarter scale); target min MAE 2.4219; outside max MAE 0.9396; caption-region max MAE 0.6691.
- 12 local stdlib tests PASS. CI tests source/policy only; **completed private MP4 is not uploaded or CI-tested**.

## Research and limits
Accessible past summaries of \`TikTok市場分析\` and \`TikTok動画研究\`: hook within first 1–1.5s, 6–10 purposeful cuts, real software demonstrations, Before/After, legible Japanese captions, and human-approved manual posting. User's 16-panel storyboard was previously inspected; **original file not directly accessible in this run**. Original research chats and original v33 MP4 are inaccessible. v33 original source remains unrecovered: this is a reimplementation, not equivalent quality.

Independent Japanese ASR and semantic/timing caption matching remain NOT_VERIFIED; no speech recognizer/model available offline. Rights for inherited media, employee approval, actual phone playback, and Actions actual charges remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, automated posting, public media upload, or paid service.
