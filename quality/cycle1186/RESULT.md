# Cycle 1186 — 2026-11-03
Previous: cycle1185 added arbitrary 25/50/75% chapter ticks. This cycle adds cut-time-aware ticks at observed high-difference frames 3.0s, 6.0s and 20.5s (threshold >35 grayscale mean absolute difference on 90x160 sampled frames every 3 frames). These are candidates, not human-confirmed scene boundaries. Existing ticks are not removed; new ticks are additive.
Input: prior local cycle1185 MP4; output local review-only MP4, not committed due to approval/asset constraints.
Local tests: 3 PASS; ffmpeg full decode PASS; ffprobe H264 1080x1920 30fps, AAC, 23.033333 seconds, 11834501 bytes.
Not validated: Japanese spoken content, subtitle semantic synchronization, visual quality, rights, smartphone playback. v33 original unavailable. No posting or merging.
Reproduce with Python import of render() from scene_ticks.py and the locally approved input video. CI may not run on stacked draft PR branches.
