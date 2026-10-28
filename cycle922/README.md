# cycle922 — cinematic layered-paper slide (review only)

**Change:** scene03 (5.800–8.700 seconds / 87 frames) uses an original textured desk, layered paper, warm moving light, subtle parallax and three progressive highlights. The message remains "prepare an example of the finished weekly report". Unlike cycle921's save workflow and cycle920's audio-driven camera accent, this is an image-first depth/lighting improvement. The earlier cycle914 paper report was flat UI; this version adds synthetic paper depth and lighting, but **does not claim photorealism or reference v33 parity**.

- 10 genre-safe presets in `cinematic_sample.py`; one rendered MP4 (AI仕事効率化) locally.
- Test: `python -m unittest cycle922/test_cinematic_sample.py -v` (requires Pillow, NumPy and Noto Sans CJK fonts).
- Generate: `python cycle922/cinematic_sample.py --out frames --genre ai_work`.
- Render scene patch: `ffmpeg -framerate 30 -start_number 174 -i frames/frame_%04d.png -frames:v 87 -vf scale=1080:1130 -c:v libx264 -crf 17 scene03_patch.mp4`.
- Compose over an authorized local **baseline** MP4: `ffmpeg -i baseline.mp4 -i scene03_patch.mp4 -filter_complex "[1:v]setpts=PTS-STARTPTS+5.8/TB[p];[0:v][p]overlay=0:315:eof_action=pass:repeatlast=0,format=yuv420p[v]" -map "[v]" -map 0:a:0 -c:v libx264 -crf 18 -c:a copy output.mp4`.
- Local output verified: 1080x1920, 30 fps, 691 frames, 23.033 s, H264/AAC 48 kHz, complete A/V decode, original AAC elementary stream SHA unchanged, title and subtitle/footer outside changed region preserved, 15/15 QA checks PASS. These claims apply to the **private local MP4**, not GitHub CI.
- Public GitHub contains **source and tests only**. No baseline MP4, inherited voices, user reference images or final MP4 are uploaded. Any user-facing MP4 is delivered as a private ChatGPT artifact.

Research basis: accessible summaries of TikTok市場分析/TikTok動画研究 (0–1.5 s hook, 15–25 s, one message, image-first, clear Japanese subtitles, before/after, safe areas), user 16-panel storyboard notes and prior cycle921 result. Original v33 MP4, independent Japanese ASR, inherited asset commercial rights, phone playback, employee approval and actual Actions billing remain **unverified**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, paid service, posting, external publication or personal data.
