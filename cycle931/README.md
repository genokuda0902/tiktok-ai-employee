# cycle931 — original scene-change sound design (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Distinct improvement
cycle929 (#314) added **8 scene-keyword ribbons**; parallel cycle930 (#315) replaces scene06 evidence comparison. cycle931 instead adds **7 original, quiet sound effects at the seven scene cuts**, with amplitude reduced when narration RMS is high. This is a genuine audio-track change, not another visual overlay. It is an optional audio design experiment and does **not** certify intelligibility, word-level caption synchronization, or reference-quality parity.

No third-party sound sample, paid service, external upload, TikTok posting or merge. A deterministic sound stem can be reused for 10 genre pitch presets; one full AI-work MP4 was rendered locally. It inherits all source visuals and Japanese narration. The source video stream is copied bit-for-bit; audio is mixed and re-encoded AAC 192k.

## Local reproduction
Requires Python 3.11+, ffmpeg and an authorized local review-only source:
```bash
python cycle931/src/transition_sound.py \
  --source /private/cycle929_KEYWORD_RIBBON_JP_HUMAN_REVIEW.mp4 \
  --output /private/cycle931_ORIGINAL_SFX_JP_HUMAN_REVIEW.mp4 \
  --sfx-wav /private/cycle931_original_transition_sfx.wav \
  --genre ai_work \
  --expected-source-sha 7fe622488252605a4e2dbf23d2c28f66b325ee4addb460a2ba549d7251145342
python -m unittest discover -s cycle931/tests -p 'test_*.py' -v
```

## Private local validation
Source SHA256: `7fe622488252605a4e2dbf23d2c28f66b325ee4addb460a2ba549d7251145342`
Output SHA256: `61a856120cf613e1944c94af3fd9992c8f2eda3f82d33b062084e3c38fb27c32`
Video bitstream SHA256 (same for both): `a9c7800fb4aa8a85180b7f108f000ef57660568e8d2be3e2569d3ab7462c3890`

H.264 1080×1920 / 30fps / 691 frames / 23.033s; AAC 48kHz mono. Entire A/V decoded. 7 cue locations confirmed; output peak -1.83dBFS (no clipping); narration correlation outside cues 0.999983. 15/15 local technical checks, 12/12 local synthetic unit tests. **The MP4 is private and not uploaded to this public repo.** Public CI tests only code and synthetic data, not the MP4.

## Research and unresolved gates
Prior TikTok market/video-study summaries and user reference storyboard: 0–1.5s hook, 15–25s, 6–10 cuts, high-quality images, natural Japanese narration, subtitle safe zones, action/CTA and human approval. Original reference v33 MP4 not directly available. No independent Japanese ASR or narration/subtitle semantic timing test; no actual phone playback, inherited commercial-rights clearance, employee approval, or GitHub Actions billing verification. The source style is still below the reference's cinematic 16-panel visual variety. Manual posting only after employee approval.
