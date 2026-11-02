# Cycle 1215 — Mobile seek reliability and compression (REVIEW ONLY)

**Previous:** cycle1213 removed crossfade double-text in 8 scenes (88 frames). **This cycle** keeps all 8 slides, Japanese narration and on-screen captions, but packages H.264 with an I-frame at each scene start (1.4, 3.2, 5.7, 8.4, 11.1, 13.8, 16.7, 19.3 seconds), preserves 8 chapter markers and AAC stream, adds MP4 faststart and lowers file size at near-identical visual quality. Generic for 10 genres via per-video boundaries.

## Local real 22.5-second MP4 QA
- Source cycle1213: 8,214,525 bytes; output cycle1215: 7,233,899 bytes (**11.938% smaller**).
- H.264 1080×1920, 30fps, 675 frames, 22.5s; 8 chapters preserved.
- Source keyframes: 0, 8.333, 16.667s; output: 0, 1.4, 3.2, 5.7, 8.4, 11.1, 13.8, 16.7, 19.3, 22.3s.
- Original AAC 48kHz Japanese track **ADTS SHA256 identical**, full video/audio decode PASS.
- FFmpeg full-frame SSIM **0.998290**, average PSNR **51.213 dB**; faststart PASS.
- Local unit tests 12/12 PASS; synthetic 90-frame 1080×1920 render/decode PASS.
- Full review MP4 is a conversation attachment, **NOT uploaded to GitHub**. CI checks synthetic material only.

## Research and limits
Past TikTok market research/video study summaries recommend a 1–1.5s hook, 15–25s length, practical UI proof, Before/After, and readable Japanese captions. User-provided 16-panel storyboard summary was available, but original v33 MP4 was not. This is a playback/encoding improvement, **not** a new storyboard or new TTS. Independent Japanese transcription, subtitle semantic/word-level timing, commercial media rights, physical smartphone playback, employee approval and actual Actions billing remain unverified.

10-genre API: ai,business,money,learning,health,food,travel,beauty,career,life. Only ai has a real full-length MP4. No external assets, paid services, auto-merge, auto-posting or public upload. Manual posting requires employee approval.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**
