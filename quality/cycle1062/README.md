# cycle1062 — real Calc sample scene (review only)

**Difference from cycle1060:** cycle1060 repaired Japanese-text occlusion in scene07 (Writer). This cycle changes scene03, frames 174–255 (5.800–8.533s), from a simulated spreadsheet graphic to a genuine *static* LibreOffice Calc GUI capture of entirely fictional monthly data. Three beats: check app screen, compare numbers, keep the completed example. This is not a live operation recording, and no productivity claim is made.

Full review-only MP4 generated privately in ChatGPT: 23.033333s, 691 frames, H.264 1080×1920 30fps, inherited Japanese AAC 48kHz stereo and burned captions (8 sections). Local full video/audio decode PASS; original/output audio ADTS SHA-256 identical. Modified 82 frames, changed upper-region mean pixel difference 55.0956/255; all-frame protected subtitle ROI max mean pixel difference 0.6022/255; unchanged upper-region max 0.7922/255. Output SHA-256: 37cdf96b73988ce085f6ba199da087bb448b12f3ab7a5ee3be4443529f5e05b4.

Run locally with a private sanitized screenshot and private source MP4 (neither committed):

`python -m quality.cycle1062.real_calc_sample --source /private/cycle1060.mp4 --screenshot /private/calc_real_optimal.png --source-sha256 <sha> --screenshot-sha256 <sha> --out /private/cycle1062.mp4 --work /private/tmp`

Tests: `python -m unittest quality.cycle1062.test_real_calc_sample -v`. CI smoke uses **synthetic 0.5s H.264/AAC**, NOT the real 23-second review MP4. Generic palettes for 10 genres, only AI-work full MP4 generated; unknown genres and wrong input hashes rejected.

Research: accessible previous summaries of TikTok市場分析/TikTok動画研究 (strong 1.5s hook, real UI, purposeful short cuts, clear captions and manual review), and the user's original 16-panel storyboard, directly inspected from the Library this run. Full original research chats and original v33 MP4 are not accessible. Main checked: 18e084c; base draft PR #461; PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md reviewed.

Reference gap: 8 scenes/23s vs 16 panels/~36s with cinematic human/robot imagery and continuous screen interaction. Japanese spoken-word transcription/pronunciation/semantic subtitle sync (especially 20.300s), rights, mobile playback, employee approval, and actual Actions billing remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, posting, paid service, public media upload or distribution of unapproved assets.
