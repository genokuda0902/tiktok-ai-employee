# cycle923 — prompt/voice-caption visual consistency (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Independent reimplementation, not recovered v33. No automatic posting, no merge, no private media upload.

## Why this change
The previous cycle922 review MP4's scene04 (8.700–11.600 seconds) showed a fictional chart while its burned Japanese caption said 「指示は、目的と条件を具体的に伝える。」. The chart did not explain the spoken/subtitled instruction.

This cycle replaces **scene04 frames 261–347** with a three-beat, clearly labeled **fictional input example**: purpose → condition → output. Other seven scenes and the inherited Japanese narration are retained. This is a visual/topic alignment fix, **not** independent speech recognition.

## Actual local MP4 (not in public GitHub)
- Input SHA256: `55df9ea3a14d7fc92b75b92ada1139a8d1329d26f448377c46f3b042af58fc38` (cycle922 private review MP4)
- Output SHA256: `59213c1766f7455b65f57c6accb38ee4cce074d995464471baaa0720b4200a70`
- Output name: `cycle923_PROMPT_SCENE_ALIGNMENT_REVIEW_ONLY.mp4`
- 1080×1920, H264 30fps, 691 frames, 23.033333 seconds, AAC 48kHz stereo.
- Full video/audio decode PASS; AAC ADTS elementary-stream SHA256 unchanged: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Scene04 87/87 frames changed; mean pixel difference in top-content region 43.493–72.185.
- Outside scene04, maximum mean pixel difference 2.244 (lossy recompression).
- Subtitle y1490:1700 maximum mean pixel difference 1.734 (lossy recompression).
- Local Python unit tests: 15/15 PASS. CI checks code and synthetic overlays, **not** the private MP4.

## Reproduce locally with authorized private source
```bash
python -m pip install pillow numpy opencv-python-headless
python -m unittest discover -s video_engine/review_quality/cycle923 -p 'test_*.py' -v
python video_engine/review_quality/cycle923/prompt_alignment_cycle923.py \
  --source /PRIVATE/cycle922_SPEECH_TIMELINE_REVIEW_ONLY.mp4 \
  --output /PRIVATE/cycle923_PROMPT_SCENE_ALIGNMENT_REVIEW_ONLY.mp4 \
  --report /PRIVATE/manifest923.json --genre ai_work
```

The source file must be an authorized private 691-frame review master. Do not commit or upload it, output MP4, audio, extracted screenshots, or private manifest. The renderer has original fictional data for ten genres, but only `ai_work` was rendered as a complete MP4.

## Research and limitations
- Accessible prior `TikTok市場分析` / `TikTok動画研究` summaries: hook within 1.5s, concise purposeful cuts, authentic UI evidence, readable captions, Before/After, staff-reviewed manual posting. Full original chats not available.
- Directly inspected user-supplied `ChatGPT×Excel時短術16コマ絵コンテ.png`. The reference has 16 visually diverse panels with cinematic robot/person and real-looking UI; this remains an 8-scene video, with an original **mock** prompt UI, not genuine ChatGPT footage.
- Original v33 MP4 unavailable; no direct video quality comparison.
- Japanese voice pronunciation and **meaning/timing agreement** with captions not independently verified (no offline Japanese ASR); this cycle only fixes one obvious *visual-to-caption topic mismatch*.
- Smartphone playback, asset publication rights, staff approval, actual GitHub Actions billing, reference equivalence and TikTok retention are NOT verified.
- No paid service, publishing, auto-post, unapproved merge or media upload.

## Next
Obtain a legally usable offline Japanese ASR model and independently compare transcript/word timing against captions. Fix remaining scene-topic mismatches; expand diverse approved 9:16 source images, then conduct manual smartphone and staff review.
