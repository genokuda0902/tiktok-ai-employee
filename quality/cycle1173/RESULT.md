# cycle1173 — clean narration rail (review-only)

Based on unmerged PR #571's 23.033-second Japanese narration MP4. This is a different improvement from cycle1172's three-beat opening: the distracting technical audio waveform at the bottom is replaced across all 691 frames by a minimal moving timeline and review label. Subtitle region is protected (all pixels y<1708), audio AAC bitstream copied, 10 genre accent palettes available. Only AI-work sample rendered and visually checked; no 10-genre publication claim.

## Offline local reproduction

python quality/cycle1173/clean_audio_rail.py --source /private/cycle1172_KINETIC_HOOK_JP_REVIEW_ONLY.mp4 --output /private/cycle1173_CLEAN_RAIL_JP_REVIEW_ONLY.mp4 --manifest /private/manifest.review.private.json --report /private/qa1173.json

python -m unittest discover -s quality/cycle1173/tests -p 'test_*.py' -v
python quality/cycle1173/tests/ci_smoke.py

Private manifest: policy, asset_approval, manual_post_only, roi_reviewed, source_sha256, genre, caption_safe_bottom. Never commit private manifest, MP4, audio or screenshots. Actions tests synthetic media only.

## Local QA 2026-11-03 JST

Actual output: H264 1080x1920 30fps 691 frames / 23.033333s, AAC 48kHz jpn, full A/V decode PASS; AAC ADTS SHA256 unchanged. Output SHA256 96b10095f562e32078e3bf4ec78d1c00ec4e87cc419c72448c95c30343629876. All 691 frames compared at 1/4 grayscale: protected upper region mean MAE 0.139/255, max frame MAE 0.275/255; changed bottom band mean MAE 17.34/255. Audio signal in 8/8 equal time windows. Local 8 unit tests and 60-frame synthetic smoke PASS. The actual MP4 is shared separately through ChatGPT, not GitHub.

## Research, provenance and limits

Available TikTok市場分析 / TikTok動画研究 summaries consulted: opening hook, purposeful cuts, real UI, readable Japanese subtitles, employee-reviewed manual posting. Full original chats unavailable. User's ChatGPT×Excel時短術16コマ絵コンテ.png directly inspected (16 panels, ~36s); original v33 MP4 unavailable. Current 8-scene/23s 2D video is not reference-equivalent. Main 18e084c, open PRs #571 and #572, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py checked. Independent Japanese speech transcription, caption meaning/timing, mobile playback, rights, employee approval and actual Actions charges NOT VERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid API, external media upload or auto-post.
