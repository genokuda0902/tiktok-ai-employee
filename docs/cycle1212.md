# cycle1212 — review-only safe-caption demonstration

Previous cycle1211: structural subtitle/audio QA only; MP4 generation blocked.

This cycle: overlay Japanese caption placement at 16–20s, x=100..980, y=1260..1460 within conservative caption-safe zone. The text is an explicit review cue, **not a synchronized transcription**. Source is cycle1209 local review MP4, not original v33.

Local sample: 1080x1920 H.264 30fps, AAC, 23.033333s, 566663 bytes, FFmpeg full decode PASS, SHA256 cab73f11b2ae264430f67a900e6132237e94ddca8d18aeb639e2958b0407bddf. Sample is shared in conversation only, not committed. Audio semantics, caption sync, smartphone playback, rights and human approval not verified.

Reproduce with: python src/review_caption_safe_area.py INPUT.mp4 OUTPUT.mp4 --font /path/to/NotoSansCJK-Regular.ttc

No automatic posting, merge or publication authorization.
