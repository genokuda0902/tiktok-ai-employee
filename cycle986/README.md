# cycle986 — formula readability / review only (2026-10-30 JST)

**Status:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Original reimplementation; NOT v33 source.

## Change from cycle984 (parallel cycle985 left untouched)
The real Calc GUI formula bar in scene 03 was tiny on a phone. During frames 174–260 (5.80–8.70s), the existing top header is replaced with a readable, source-labeled formula evidence strip: `営業A =SUM(B2:B4) 46` then `営業B =SUM(C2:C4) 29`. The actual Calc worksheet and existing lower Japanese burned captions remain unobstructed. These are fictional demonstration figures, not real productivity outcomes.

This is a genre-common **focus callout renderer**, but real-video coordinates have been reviewed only for `ai_work`; all nine other genres fail closed. Synthetic CI can test all ten IDs without publication approval.

## Reproduction with private source, not included in public GitHub
```bash
python cycle986/formula_focus.py --source /private/cycle984_CTA_FOCUS_JP_REVIEW_ONLY.mp4 --output /private/cycle986_FORMULA_MAGNIFIER_JP_REVIEW_ONLY.mp4 --work /private/cycle986-work --expected-sha 1e03d7274d2d11c5c2ed80ebd4254bd972cc5acfb251abfa76aec06f5207c63e
PYTHONPATH=cycle986 python -m unittest discover -s cycle986 -p 'test_*.py' -v
```
Requires ffmpeg, ffprobe, Python/Pillow, Noto CJK and DejaVu fonts. Never commit private MP4, extracted voice, or user images.

## Local full-MP4 QA
Input SHA256 `1e03d7274d2d11c5c2ed80ebd4254bd972cc5acfb251abfa76aec06f5207c63e`; output SHA256 `8cabfb8af96a4c1373905b232d571944337aedc22d88ac56b05d1d7292590f9b`. H264 1080×1920 30fps / 691 frames / 23.033333s, AAC 48kHz stereo. Full video/audio decode PASS; AAC ADTS elementary stream SHA identical `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`; 10 local tests PASS. All-frame 1/4-scale caption ROI y1440:1840 max mean pixel diff 0.256/255. Changed header ROI mean 30.612/255; outside edited scene max 0.499/255. These are technical metrics, not viewer quality scores.

## Research and reference
Read accessible prior `TikTok市場分析` / `TikTok動画研究` summaries (strong first 1.5s, 15–25s, demonstrative UI, Before/After, Japanese captions, human approval). Directly inspected user's `ChatGPT×Excel時短術16コマ絵コンテ.png` from Library: 16 panels/~36s, robot/person, realistic ChatGPT→Excel and graph shots, CTA. Full research chat transcripts and original v33 MP4 unavailable for direct comparison. Current 8 scenes/23s are not reference-equivalent.

## Publication and CI limits
Synthetic-only CI never uses the private completed video. Independent Japanese ASR, spoken-text/semantic caption timing, source rights, smartphone playback, employee signoff, and Actions actual billing NOT VERIFIED. Do not merge, auto-post, distribute, spend, or claim publication readiness.
