# cycle937 — subtitle-aware template detail microcuts (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is a reimplementation, not the recovered v33 original. No auto-post, merge, paid API, external private-media upload, or publication approval.

## Verified change from cycle936

- Input private MP4 SHA256 `9ba495276c6d42ffb178a58c80b2d8164bc21a98f330cb44270925413faa77a2` (cycle936 PR #323). Source includes fictional template and inherited Japanese narration/subtitles.
- The previous scene07 template remained small, while at **19.57s** the burned-in caption already switched to the final message but the video still showed a mismatched illustrative scene. This cycle renders two larger **source-derived fictional template detail shots** at 18.30–18.93s and 18.93–19.57s, then shows the inherited **unapproved scene08 checklist** from 19.57–20.30s to match the already-switched subtitle. Changed frames **549–608 (60 frames)**. Source images are extracted from the private input and are not new real ChatGPT/Excel recordings. No numerical values or spoken audio were rewritten.
- Ten genre-specific heading presets. Each genre needs its own approved input template and outro frame in the same layout. Only `ai_work` was rendered as a complete MP4.

## Local technical evidence

- New MP4 SHA256 `9c98d96d8b5596b80b099da98fbc266b2d2b76409a32cfe7dcd9939644a876a0`.
- H.264 1080×1920 / 30fps / 691 frames / 23.033s; inherited AAC 48kHz audio elementary stream unchanged.
- Full audio/video decode PASS; 60/60 edited frames visibly changed (minimum 1/8-scale MAE 28.885), outside edit maximum MAE 0.193, caption region maximum MAE 0.332. Eight time windows have nonzero audio energy, **not independent Japanese speech recognition**.
- 20/20 local unit tests PASS. GitHub CI tests code and synthetic images only, not the private full MP4.

## Reproduce privately

Use free FFmpeg, Python, Pillow, NumPy, Noto CJK fonts. **Do not commit source/output video, extracted frames, audio, private assets, secrets, or rights evidence.**

```bash
PYTHONPATH=cycle937/src python -m unittest discover -s cycle937/tests -p 'test_*.py' -v
python cycle937/src/template_detail_microcuts.py --source /PRIVATE/cycle936_REVIEW_ONLY.mp4 --output /PRIVATE/cycle937_REVIEW_ONLY.mp4 --workdir /PRIVATE/tmp --genre ai_work --expected-source-sha 9ba495276c6d42ffb178a58c80b2d8164bc21a98f330cb44270925413faa77a2
python cycle937/src/verify_review.py --source /PRIVATE/cycle936_REVIEW_ONLY.mp4 --output /PRIVATE/cycle937_REVIEW_ONLY.mp4 --report /PRIVATE/verification.json
```

## Reference, limitations and next

Consulted accessible summaries of `TikTok市場分析` and `TikTok動画研究` (hook, purposeful cuts, real evidence, Before/After, captions, manual approval). Directly viewed user's `ChatGPT×Excel時短術16コマ絵コンテ.png`: 16 cinematic panels/36s, robot/person, ChatGPT/Excel demonstrations, CTA. Complete task/chat text and original v33 MP4 remain inaccessible. This 8-scene/23s UI-led video does not meet that cinematic diversity. No independent Japanese ASR, word-level semantic subtitle timing, rights review, phone playback, employee approval or Actions actual charges verified. Next priority: permitted offline ASR/human transcription and approved cinematic imagery, then phone/human QA.
