# cycle1024 — scene02 Japanese readability regression repair (review only)

2026-10-31 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
Independent reimplementation, NOT recovered v33 code. No publication, merge, paid contract, or auto-post.

## Why this cycle
- Read accessible summaries of TikTok市場分析 / TikTok動画研究 (first-second hook, short visual beats, actual UI, Before/After, large Japanese subtitles). Original full task transcripts unavailable.
- Directly inspected the user-provided ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels/~36s); original v33 MP4 unavailable this run. The reference's second panel uses clear separated task/problem callouts.
- Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py (still silent -an), unmerged PR #423 and parallel #424. The new work stacks only on #423.
- Prior cycle1022 was 8-scene 23.033s and added a story rail + mixed-audio boundary diagnostics. Its scene02 had crowded overlapping task UI. Parallel cycle1023 edits the opening, not this scene.

## Specific visual change
- Rebuild only scene02 (2.90–5.80 seconds) into a high-contrast three-beat task list with sequential reveals at 3.080 / 3.760 / 4.440 seconds.
- Ten genre-specific Japanese title/card sets share the same safe rendering engine. The completed real MP4 has been generated/tested only for ai_work.
- Preserve original background imagery beneath translucent panels; retain existing Japanese burned subtitles below y=1490 and story rail at top. No external image, model, music, or API.
- Fail closed on unknown genre, incorrect SHA, missing source, output overwrite, incorrect A/V spec, selectable subtitle streams or missing review flag.

## Actual private review MP4 QA (not committed to public GitHub)
- Input: cycle1022 SHA256 e734bccfc0152c22a11f1f600008067e414bca08d59227c12d29cce3d2437099
- Output: cycle1024 SHA256 9c1fc7d59b767f83eaedbef94bb102df2a88c486bb8b7a2099978a7c59f02cf5
- 1080×1920, H.264, 30fps, 691 frames, 23.033s; Japanese-tagged AAC 48kHz. Full video+audio decode PASS; AAC ADTS elementary stream SHA matches input.
- Frame-by-frame (691/691) sampled caption ROI y1490–1840: max per-frame mean pixel delta 0.946/255, p95 0.823/255.
- Modified scene ROI x42–1038/y210–1425: mean pixel delta 40.348/255, min 30.192/255; other scene ROI max sampled delta 0.879/255.
- 10/10 unit tests PASS; 2-second synthetic smoke MP4 and full decode PASS. GitHub CI must be checked independently.
- Real private MP4 and original reference assets are never uploaded to GitHub. See ChatGPT private review attachment.

## Reproduction (private source must be explicitly allowed for local review)
Run with FFmpeg and Noto CJK fonts installed:

    python cycle1024/source/scene2_clarity.py --source /private/cycle1022_REVIEW_ONLY.mp4 --output /private/cycle1024_REVIEW_ONLY.mp4 --report /private/cycle1024_qa.json --expected-source-sha e734bccfc0152c22a11f1f600008067e414bca08d59227c12d29cce3d2437099 --genre ai_work --review-only
    python -m unittest discover -s cycle1024/tests -v

## Remaining gates
Independent Japanese ASR/transcript, word-level caption semantic/timing verification, original v33 direct video comparison, commercial media rights, smartphone playback, employee approval and Actions actual billing NOT VERIFIED. Not a publication-ready or reference-equivalent video. The current review source has 8 scenes, reference storyboard 16; cinematic shot variety and continuous genuine UI demonstration still lag. Next cycle should prioritize audio-text verification or licensed/approved visual diversity without redoing scene02.
