# cycle897 — eight safe editorial accents, 16 visual beats (review only)

2026-10-27 JST. This is an **incremental reimplementation**, not recovered v33.

- Previous local source: cycle896 evidence magnifier, SHA256 `8be7da9de4ad858563713342f47a6c7083810a9d98db6034083aa60c5a8b2946`.
- New local review MP4 SHA256 `d969140aae9c054f5084a0d4138fd9ff952f55babb8e9c99b6c0e134dfcf53d7`. **Private local artifact only; not uploaded to GitHub.**
- 8 existing scenes / 23.033s, each divided into two visual phases. Second phase: 6 non-cropping cyan focus accents (scenes 1–6), 2 subtle reframes on evidence / Before-After (scenes 7–8). These are **not 16 different shots**.
- The first attempted all-scene zoom cropped some Japanese headings. That was rejected, not delivered; safe-zone-specific approach is the delivered change.
- Local tests: 12/12 PASS; FFmpeg full decode PASS; 1080x1920 H264 30fps, 691 frames, AAC 48kHz stereo.
- Source/output AAC ADTS SHA256 identical `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Subtitle-protected y1490:1840, all 691 frames compared; max sampled MAE 0.2409, p95 0.2248. No ASR or semantic match inferred.
- Ten-genre IDs validated by shared fail-closed code; only AI-work MP4 rendered.

## Reproduce with locally approved exact-hash source
```bash
python -m unittest discover -s quality/cycle897 -p 'test_*.py' -v
python quality/cycle897/editorial_beats.py \
  --source /private/cycle896.mp4 --output /private/cycle897.mp4 \
  --manifest /private/review_manifest.json --report /private/cycle897.json
```
Manifest requires exact `POLICY`, genre ID, source SHA256, `real_service_footage=false` and `reference_equivalent=false`. No source video, extracted voice, private manifest, or confidential media committed.

## Reference & restrictions
Consulted accessible TikTok市場分析/TikTok動画研究 summaries and directly inspected user's 16-panel ChatGPT×Excel storyboard. Original reference v33 MP4 and full original research chats unavailable. This 8-scene result does not match the storyboard's cinematic people, robot, 16 independent cuts, or genuine ChatGPT/Excel demos. Independent Japanese ASR, spoken/caption meaning, pronunciation, source rights, phone playback, employee approval and actual Actions billing **UNVERIFIED**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, posting, paid services or external media upload. GitHub CI runs Python unit tests and static checks only (network-independent); local FFmpeg verified the private finished MP4.
