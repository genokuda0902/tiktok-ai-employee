# cycle883 — kinetic scene-transition pass (REVIEW ONLY)

## Research / provenance
- Consulted accessible summaries of TikTok市場分析 and TikTok動画研究: hook in first 1–1.5 s, meaningful quick cuts, UI demonstration, Before/After, Japanese subtitle safe zone, employee-reviewed manual posting. Original chat transcripts inaccessible.
- Directly inspected user's 16-panel / 36-second ChatGPT×Excel storyboard from ChatGPT Library. Reference v33 MP4 is **not accessible** for direct comparison.
- Checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py`, unmerged #245 and #246.
- Based on open #246 (cycle882 Chromium DOM proof). **The cycle882 completed MP4 was not accessible locally**. This cycle's preview therefore uses accessible cycle881 MP4, not cycle882, and cannot claim a net improvement over cycle882. It does not replace #246's browser demonstration.

## Actual distinct change
- New ten-genre reusable FFmpeg/Pillow kinetic diagonal wipe at the seven existing scene boundaries: frames 89, 170, 251, 336, 422, 510, 588 (2.967, 5.667, 8.367, 11.200, 14.067, 17.000, 19.600 s).
- Each wipe spans 9 frames (±4) with dark navy moving mask and cyan streaks in upper 1438 px. Existing 8-scene timing, Japanese subtitles, voice and all other visual content are preserved.
- Pure-code safety: reject unknown genre, overlapping/too-long wipes, caption-area collision, missing source hash or non-review policy. No external network, proprietary footage or personal information added.
- Not the original v33 source, not a live ChatGPT/Excel recording. Only `ai_productivity` rendered; other genres require their own content.

## Reproduce locally with private source
Requires Python 3, Pillow, FFmpeg/FFprobe. **Do not commit or upload private source, audio, mask or MP4.**
```bash
python video_engine/cycle883/kinetic_wipe.py \
  --source PRIVATE_cycle881_SOURCE_PROOF_JAPANESE_REVIEW_ONLY.mp4 \
  --output PRIVATE_cycle883_KINETIC_SCENE_TRANSITIONS_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest PRIVATE_manifest.json --report PRIVATE_report.json
python -m unittest discover -s video_engine/cycle883 -p 'test_*.py' -v
python video_engine/cycle883/ci_smoke.py
```
Private manifest: `review_only=true, publication_approved=false, external_upload=false, automatic_posting=false, source_rights_reviewed=false, synthetic_ui=true, source_sha256=<actual input SHA>`.

## Local measured results (not CI)
- Source cycle881 SHA256: `e5dfc111ed8fe0af8c0735d3ac97fae4be939243b6b866ff859fbc5a10863149`.
- Output cycle883 SHA256: `595d365549373f0de96ae6e8868725bea038be903bb194a00983b432c0c7b1fc`.
- 1080×1920 H264 30fps 691 frames / 23.033s, AAC48kHz; full A/V decode PASS.
- 63 targeted boundary frames, 49 with sampled upper-area pixel difference >5; seven transitions individually changed.
- Subtitle safe band all 691 frames: max sampled mean delta 1.1074 (<2). Upper area outside target windows: max 1.2384 (<2).
- Inherited AAC elementary bitstream SHA256 identical `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 10 local unit tests PASS, synthetic 90-frame H264/AAC smoke PASS. GitHub CI tests only public code + synthetic video; **does not validate/upload the private completed MP4**.

## Limits / release
Japanese spoken-word accuracy, independent speech/subtitle semantic sync, smartphone playback, source rights, employee approval, reference parity, retention impact and actual Actions billing are unverified. The wipe may be judged too prominent by a human editor. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid service, automatic posting or external private-media upload.
