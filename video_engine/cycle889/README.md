# cycle889 — arithmetic-grounded correction motion (review only)

This is a **reimplementation**, not recovered v33. It builds on the unmerged cycle886 local review MP4, which itself contains offline fictional browser interactions. Do not publish, merge, or externally upload inherited media.

## Change vs cycle886 and parallel PRs

cycle886 replaced scene07 with 3 real offline Chromium DOM states. Parallel unmerged #254/cycle887 added narration-reactive header and #255/cycle888 added editorial focus corners; neither was merged or used as video source here. This cycle instead replaces **scene06 frames 422–509 (14.067–17.000s)** with a 3-stage animated arithmetic correction: detect 17 vs source 18, show the single-row fix, recompute total 45→46 from fictional [12,16,18]. The totals are calculated from data, not hardcoded. Safe overlay geometry preserves original scene header, Japanese burned captions and AAC audio.

## Local real review MP4 (not in GitHub)

- Source: cycle886_REAL_OFFLINE_SAVE_JAPANESE_REVIEW_ONLY.mp4 SHA256 090e9ebe87a2aa8e05beba75b3b4f628f1bbcbf069807e64d2720773c7465d10.
- Output: cycle889_CORRECTION_TRACE_JAPANESE_REVIEW_ONLY.mp4 SHA256 0edfc3bd34ba6b1beccfd9a7016219178dc709d276dee40fa0454ec9dce2d99c.
- 1080×1920 H264 30fps, 691 frames/23.033s; AAC48kHz stereo.
- All 88 scene06 frames visibly changed (min sampled MAE 27.349); outside-scene max sampled MAE 1.385, caption band max 0.956, header max 1.206; audio ADTS SHA identical 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9; full A/V decode PASS. Local 15 tests PASS.
- Video and visual QA are available in a **private ChatGPT sandbox ZIP**, not committed to GitHub. CI validates code and a **synthetic** 1-second H264/AAC clip only.

## Reproduce locally

Install Python 3.11+, Pillow, FFmpeg, Noto Sans CJK Bold. Run python -m unittest discover -s video_engine/cycle889 -p 'test_*.py' -v. To render, create an untracked JSON manifest with exact POLICY fields in correction_motion.py and source_sha256 pinned to your **locally authorized** input; call correction_motion.py --source INPUT.mp4 --output REVIEW_ONLY.mp4 --manifest manifest.json --work PRIVATE_TMP --report report.json. This code deliberately refuses unpinned inputs or publication approval.

## Research and limits

Consulted accessible summaries of TikTok市場分析 and TikTok動画研究: first 1–1.5s hook, purposeful edits, visual proof/Before–After, legible Japanese subtitles, human approval. Full research chat transcripts unavailable. User's 16-panel/~36s ChatGPT×Excel storyboard reference is known from prior inspection; original v33 video was not retrieved this run. This is a small visual improvement, **not** reference-quality parity.

Independent Japanese speech transcription, pronunciation, word-level caption sync, inherited voice/photo rights, mobile device playback, employee approval, TikTok retention and actual Actions charges remain **UNVERIFIED**. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, external private-media upload, paid API, or auto-posting.
