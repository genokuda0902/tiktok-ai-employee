# cycle1064 — cinematic motion over real Calc screenshot (review only)

Difference from cycle1062: the prior 82-frame scene (5.800–8.533s) used a static Calc screenshot and three fixed steps. This cycle adds a subtle original 8.5% push-in and eased movement over the *same private, sanitized static screenshot*, plus depth/shadow, compact three-beat chips, and a visible non-live-screen-recording disclosure. It does **not** depict actual live UI operations, nor prove an AI performance improvement.

Full 23.033s review-only MP4 is generated privately in ChatGPT; neither private screenshot, audio, nor video is pushed to GitHub. The reusable rendering algorithm supports ten approved genres. The CI tests a synthetic 0.5s H264/AAC video, **not** the private 23s final MP4. The original Japanese AAC audio and eight burned captions are retained; independent semantic ASR, word-level sync (especially 20.300s), rights, mobile playback and employee approval remain outstanding.

Local private run: `python -m quality.cycle1064.cinematic_ui_motion --source /private/cycle1062.mp4 --screenshot /private/calc.png --source-sha256 <sha> --screenshot-sha256 <sha> --out /private/cycle1064.mp4 --work /private/work`.

Sources: available summaries from TikTok市場分析 and TikTok動画研究, user-provided 16-panel ChatGPT×Excel storyboard as summarized in prior records. Full original research chats and v33 original MP4 not available in this run. Reference gap remains 8 scenes/23s vs 16 panels/~36s, high-quality humans/robot and true continuous operation recording. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, posting, paid services, or private media uploads.

## Verified local result (2026-10-31 JST)
- Review-only private MP4: cycle1064_CINEMATIC_CALC_MOTION_JP_REVIEW_ONLY.mp4; SHA-256 87ea4a7995f726edcb12739a7b6a6ce08bc13ce3ef5ffe61cf7cd8ca01581bfd.
- H264 1080x1920 30fps, 23.033333s / 691 frames; inherited Japanese AAC 48kHz; full A/V decode PASS.
- Source and output AAC ADTS SHA-256 identical: 76801539a721f7d968b5a8bf725fd056ab00de5a74bd09caf50112993c4aa2f8.
- Exactly 82 modified frames 174–255; changed upper-region mean pixel delta 34.3889/255. Caption ROI y>=1270 maximum all-frame mean pixel delta 0.5328/255. Unchanged upper-region maximum 0.9126/255.
- Local 7/7 tests and synthetic H264/AAC smoke PASS. GitHub Draft PR #465: https://github.com/genokuda0902/tiktok-ai-employee/pull/465 . CI only validates synthetic media, not final private MP4.
