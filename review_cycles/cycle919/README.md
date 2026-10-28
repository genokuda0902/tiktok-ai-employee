# cycle919 — emotional before/after comparison (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Original illustrated office vignette, not real footage and not the original v33 engine. No private media committed, no merge, posting, or paid service.

## Change from cycle917 and parallel cycle918
- cycle917 PR #297: scene07 reusable Japanese prompt template (purpose → constraints → output).
- Parallel cycle918 PR #298: scene01 three-task opening hook.
- cycle919: scene08, 19.600–23.033 s (103 frames): stressed illustrated office worker / unverified draft → source-check display with fictional 18. Animated wipe; 10 genre text presets. Earlier scenes and inherited audio retained. No new source media or third-party downloads.

## Local reproduction (private source file required)
Requires Python 3 + Pillow, ffmpeg, Noto Sans CJK fonts. `python emotional_before_after.py --out /private/cycle919/frames --genre ai_work`
Then:
```sh
ffmpeg -framerate 30 -i /private/cycle919/frames/%03d.png -i /private/cycle917.mp4 -filter_complex '[0:v]setpts=PTS+19.6/TB[ov];[1:v][ov]overlay=x=0:y=150:format=auto:eof_action=pass:shortest=0[v]' -map '[v]' -map 1:a:0 -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p -r 30 -frames:v 691 -c:a copy -movflags +faststart /private/cycle919.mp4
```
Source MP4 is private to the user conversation; never upload it to public GitHub. CI tests code/policy, **not the completed private MP4**.

## Verified local output and limits
23.033s, 1080×1920 H.264/30fps/691 frames, AAC/48kHz. Full A/V decode PASS. Audio elementary stream SHA unchanged. 103/103 target frames changed (quarter-resolution MAE >5), outside max MAE 0.546, subtitle band max MAE 0.569. 17 local tests PASS (10 renderer + 7 policy); CI runs 7 stdlib policy tests. Final local MP4 SHA256: `d5a4b8f8cbc418dd62484caabd3a7e2c4ed1270e02e1fbf7014d302cd116881e`.

## Research, reference and safety
Consulted accessible summaries of TikTok市場分析 / TikTok動画研究: 1–1.5s hook, purposeful cuts, image-first, real UI, before/after, readable Japanese subtitles, manual employee-approved posting. Directly inspected user 16-panel ChatGPT×Excel storyboard. Full original research chat texts and v33 MP4 inaccessible. Original reference has cinematic human/robot scenes and 16 cuts; this is an illustrated 8-scene / 23s reimplementation, **not quality-equivalent**.

Independent Japanese speech recognition, subtitle meaning/timing, inherited rights, smartphone playback, employee approval, retention and actual GitHub Actions charges remain unverified. No merge, auto-post, paid contract, confidential image, or external media upload.
