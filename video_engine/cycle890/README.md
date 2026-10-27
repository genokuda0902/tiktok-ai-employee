# cycle890 — Japanese prompt typing reveal (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is an offline fictional demonstration, **not** a recording of ChatGPT or Excel. Do not publish, merge, upload inherited media, or call paid services.

## Distinct change
- Source is the accessible **cycle889** completed review MP4, not a claimed original v33 source.
- Scene04 frames **251–335** (8.367–11.200s): replaces the previously static white prompt input with a progressively typed **three-line Japanese prompt**, visible cursor and final source-verification emphasis. The final text preserves the three original prompt lines.
- Scene06 correction 17→18 / total 45→46, scene07 offline Chromium screenshots, 8 existing Japanese captions and inherited audio remain unchanged except H264 re-encoding artifacts.
- 10 genre templates share the same renderer and safety checks. Only `ai_productivity` was rendered as a completed MP4.

## Verified private local MP4
- Input cycle889 SHA-256: `0edfc3bd34ba6b1beccfd9a7016219178dc709d276dee40fa0454ec9dce2d99c`
- Output cycle890 SHA-256: `a255c93f861897f07ea48debaa1a293177fab94bda008b0a1219345dd9ce3c08`
- H264 1080×1920, 30fps, 691 frames / 23.033s; AAC 48kHz stereo.
- All 85 target frames changed. All 691 frames sampled: outside-target mean pixel delta max 1.297, caption band max 0.970, header band max 1.162. Full video/audio decode PASS.
- AAC elementary bitstream SHA-256 source = output = `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 18 local unit tests PASS. GitHub CI tests **only code + synthetic 1-second video/audio**, not the private Japanese finished MP4.

## Local reproduction
Requires Python 3.11+, Pillow, FFmpeg, Noto Sans CJK. Run `PYTHONPATH=video_engine/cycle890 python -m unittest discover -s video_engine/cycle890 -p 'test_*.py' -v`. For local rendering, supply an untracked JSON manifest with exact `POLICY` fields and the input file SHA-256, then call `prompt_typing.py --source SOURCE.mp4 --output PRIVATE_REVIEW_ONLY.mp4 --manifest PRIVATE.json --work PRIVATE_DIR --report PRIVATE_REPORT.json`. Do not commit the input, output, screenshots, inherited audio, or manifest.

## Research, rights, remaining gaps
Accessible summaries of 「TikTok市場分析」 and 「TikTok動画研究」: 1–1.5s hook, purposeful cuts, actual UI proof, Before/After, readable Japanese captions and employee approval. User's original **16-panel / ~36s** ChatGPT×Excel storyboard inspected this cycle; original v33 MP4 and complete research chats unavailable. This 23s / 8-scene reimplementation still lacks the reference's real-person/robot imagery and real ChatGPT/Excel capture. Independent Japanese ASR, semantic subtitle sync, pronunciation, inherited rights, smartphone playback, employee approval, TikTok performance and actual GitHub Actions charges remain **UNVERIFIED**. No auto-posting, paid service, private media upload, or merge.
