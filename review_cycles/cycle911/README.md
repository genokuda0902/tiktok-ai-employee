# cycle911 — Real LibreOffice Calc GUI capture (review only)

## Distinct change vs cycle910
cycle910 animated a synthetic source table → chart in scene08. This cycle replaces only scene02 (frames 87–173; 2.9–5.767 seconds) with three actual locally captured LibreOffice Calc screenshots: fictional 4–6月 table → B5 selected → =SUM(B2:B4) shown in the formula bar. This narrows the reference's real-software-operation gap. The source is self-created fictional data; it is NOT Microsoft Excel, not a real account, and not a claim of productivity gains.

Only ai_work has been rendered. Ten genre color presets are available, but their output videos are untested.

## Local-only inputs
- cycle910 private MP4 source SHA256: 81a2fb09a50e050b3fe70d803583fa56233d380f61acb7b259bd060f9fc7361c
- Locally created fictional workbook fictional_calc_demo.xlsx; three local screenshots calc_01.png / calc_02.png / calc_03.png captured with xvfb-run, LibreOffice Calc, and pyautogui.
- Local dependencies: Python, Pillow, FFmpeg/libx264, Noto Sans CJK JP fonts, LibreOffice Calc (to capture images).
- Do not upload original or inherited video/audio/screenshots to public GitHub. They are available only in the private conversation review package.
- Run: python calc_capture_overlay.py --source SOURCE.mp4 --output cycle911_REAL_CALC_CAPTURE_REVIEW_ONLY.mp4 --expected-sha SOURCE_SHA --captures calc_01.png calc_02.png calc_03.png --frames-dir /tmp/frames911 --genre ai_work

## Verification, 2026-10-28 JST
- Review MP4: H.264 1080×1920, 30fps, 691 frames, 23.033333s; AAC stereo 48kHz copied with identical ADTS elementary stream SHA256 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9.
- Full audio/video decode PASS; 16 sampled changed scene02 frames; caption-safe region starts at y1490; sampled lower region max MAE 1.191/255 at quarter resolution due to video re-encoding.
- Completed local MP4 SHA256: 4587ba15fb3a3cf871e486eb9caec884efdfeac8ec74898c927bf02a88c1a28d.
- Local policy tests 9/9 PASS. CI checks only code and policy, NOT private completed MP4.
- Independent Japanese ASR and speech/caption semantic or timing match: NOT VERIFIED. Real smartphone playback, rights of inherited materials, employee approval, direct v33 comparison and Actions actual charges: NOT VERIFIED.

## Research and handoff
Accessible prior summaries of 「TikTok市場分析」「TikTok動画研究」 supported strong opening hook, purposeful cuts, real app operations, Before/After, safe readable subtitles and manual employee approval. User's 16-panel ChatGPT×Excel時短術 storyboard was referenced in earlier cycles, but its original image and original v33 MP4 were not directly accessible this run; full original research transcripts were also unavailable. PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md govern safety and image-first design. This cycle is a reimplementation, not original v33 source.

## Publication and security
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Do not merge or publish without human review. No automatic TikTok posting, confidential media, paid APIs, unapproved external upload or real personal data. Staff approval and manual posting only.
