# cycle752 — animated focus light (review-only)

Difference from cycle751: a moving cyan spotlight on diagrams in scenes 3, 5 and 6 (150/429 frames), not a global sharpening pass. No geometric warping of text. Top hook and subtitles are protected. Original Japanese AAC is copied unchanged.

Local render: 1080x1920 H.264 30fps, 14.3 seconds, 16 subtitle cues. QA 15/15; local tests 10/10. The MP4, source media, full local QA, screenshots and complete reproduction package are supplied separately in the conversation ZIP.

To reproduce: install ffmpeg, Python 3.11, numpy, opencv-python-headless, pytest; then run `python experiments/cycle752/render.py --source input/previous.mp4 --output output/cycle752.mp4` from repository root, with a rights-cleared input MP4.

Limitations: no verified rights for inherited source, no phoneme-level sync or voice-naturalness rating, no physical phone playback, no reference-video equivalence. Publication not approved. Employee review and manual posting only; no paid services, auto-posting, or auto-merge.
