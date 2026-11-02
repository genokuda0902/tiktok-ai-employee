# cycle1160 — review-only scene-local parallax (2026-11-02 JST)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid API, automatic posting, or public upload of the private real MP4.

## Prior state and reference
- Previous reviewed MP4: cycle1158, SHA256 b0b508b13d812130d2b088d8d0aff54e91db2edee9d3700e6f3ccb97a38996b7.
- Consulted accessible TikTok市場分析/TikTok動画研究 summaries: strong first-second hook, purposeful visual changes, real UI, Before/After, readable Japanese subtitles, employee-reviewed manual posting. Full chat/task transcripts unavailable.
- User 16-panel/36s ChatGPT×Excel storyboard directly inspected; source v33 MP4 unavailable, so reference quality comparison is qualitative only.
- main 18e084c38db0dc55db7dfc0532b9451b1167f2aa; base open PR #559, other unmerged PRs not modified; PROJECT_HANDOFF.md and recovery/v33 reviewed. This is not the original v33 engine.

## New change
- Added genre-agnostic, source-SHA-pinned, review-only motion renderer with a 10-genre allowlist, layout guard and caption-protected region.
- Gentle scene-local 2D parallax in two illustrative scenes only: robot opener 0.36–2.52s (65 changed frames) and repetitive-task paperwork 3.18–5.34s (65 changed frames).
- 130 of 691 frames changed intentionally. Title, spreadsheet UI, chapter strip, Japanese burned subtitles and audio meter are not intentionally modified.
- Rejected early drafts: global panel zoom clipped title/BEFORE label; spreadsheet zoom softened text. Final ROIs limit motion to illustrations, preserving readable spreadsheet.
- These are subtle digital push-ins, not 3D character animation or real camera footage. 10 genre configurations tested, but only AI work genre real MP4 rendered.

## Real local MP4 QA
- Filename: cycle1160_SCENE_PARALLAX_JP_REVIEW_ONLY.mp4; SHA256 9fbae3325136e0da41e7b8fe55c1f5c816d296c3dd9b2d781d4b06271e762026.
- 1080x1920 H264 30fps, 691 frames / 23.033s, AAC 48kHz Japanese-tagged inherited audio. Full A/V decode PASS.
- Source/output AAC ADTS SHA256 identical: 27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65.
- Full 691-frame caption safe-zone (y1280:1880) 1/4-sampled maximum MAE 1.459/255; chapter strip (y1000:1280) max 1.820/255, attributable to full-video reencoding rather than intentional graphic edits.
- Mean illustrative ROI pixel difference at 0.9s 10.515/255, 4.3s 5.978/255; non-target 21.57s 1.755/255 (reencoding only).
- Local 8/8 tests PASS; synthetic 60-frame 1080x1920 H264/AAC render + full decode PASS. CI tests synthetic data only, never private source video.
- Not independently verified: Japanese transcript, spoken/caption semantic or word timing, source-media rights, smartphone hardware playback, employee approval, actual Actions charges.

## Next
1. Secure genuinely accessible free Japanese ASR model and compare all eight captions with speech and timestamps; until then do not claim semantic sync.
2. Review source rights and smartphone playback; request human review before any posting.
3. Improve original imagery and 16-scene cinematic variety using approved/public-safe sources, rather than repeating minor overlays.
