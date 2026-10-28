# cycle916 — source-diff correction animation (review only)

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No auto-posting, public media, merging or paid service.

## Change from cycle914 and parallel cycle915
Cycle914 introduced a missing-June-data hook in scene01; cycle915 PR #294 adds a separate evidence-check animation in scene05. Cycle916 improves scene06, frames 435–509 (14.5–17.0s) with a legible source-backed three-step example: AI draft value 17 → fictional source value 18 → confirm one correction. The 17/18 values are editorial fictional examples, not real sales. Ten genres share the same renderer; only ai_work full MP4 was made.

## Local reproduction (private media)
Python 3, Pillow, FFmpeg and Noto Sans CJK fonts required.
Run local Pillow tests: PYTHONPATH=review_cycles/cycle916 python3 -m unittest discover -s review_cycles/cycle916 -p test_cycle916.py -v.
Generate 75 overlay frames: python3 review_cycles/cycle916/source_diff.py --genre ai_work --out /private/cycle916_frames.
Overlay onto the private cycle914 MP4 at y=300 from 14.5 to 17.0 seconds using FFmpeg; copy original AAC. Do not commit any inherited private media. CI runs 10 standard-library-only source and policy tests, not the private MP4.

## Verified private MP4 (2026-10-28 JST)
Source SHA256: c8fad3896247c97a0a0fab3c2d442f910fd34293f8fb1b6bc4d9d543a85c45e1.
Output SHA256: 73e4b722e0bab48d4d77d249b89394510da36dfb22c941a028e5f8f3a1c081ec.
1080×1920, H.264, 30fps, 691 frames, 23.033333s, AAC 48kHz. Full A/V decode PASS. All 75 changed frames mean pixel MAE >70 at quarter resolution; outside target max 0.273; subtitle band max 0.162; AAC ADTS SHA matches original 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9. Local Pillow unit tests 14 PASS.

## Research and gates
Consulted accessible summaries of TikTok市場分析 and TikTok動画研究, directly inspected the user's 16-panel ChatGPT×Excel storyboard in Library. Original full chats and original v33 MP4 inaccessible this run. This eight-scene video still lacks the reference's cinematic/3D imagery, live ChatGPT UI and 16 cuts. Independent Japanese ASR/caption meaning and timing, publication rights for inherited assets, smartphone playback, employee approval, actual Actions billing and viewer retention are NOT VERIFIED. Manual employee-approved posting only.
