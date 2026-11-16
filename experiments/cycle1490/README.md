# Cycle 1490 — REVIEW ONLY / PUBLICATION_NOT_APPROVED

Improvement over cycle1489: the Japanese SRT is **burned into the MP4** instead of only being supplied as a separate sidecar. This avoids missing captions in players that ignore sidecar SRT. Same 15 seconds, 1080×1920, 30 fps. No Japanese narration; audio intentionally absent and publication forbidden.

Source input: cycle1489 synthetic video and SRT (local artifacts, not included in GitHub). No private photos or voice assets used.

Reproduce with ffmpeg/libass and Python 3:
```bash
python experiments/cycle1490/render.py INPUT.mp4 captions.srt cycle1490_REVIEW_ONLY.mp4
cd experiments/cycle1490 && python -m unittest -v test_render.py
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate -of json cycle1490_REVIEW_ONLY.mp4
ffmpeg -v error -i cycle1490_REVIEW_ONLY.mp4 -f null -
```

No automatic upload, publication, employee delivery or merge. CI status and recipient-side checksum require independent verification. Reference v33 original and market research/reference source video not directly accessible in this cycle. Next priority: real Japanese TTS, phrase-timed captions, source delivery, and CI.
