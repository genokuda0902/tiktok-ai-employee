# cycle877 — truthful intermediate chart states + independent acoustic QA

**Review-only reimplementation. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## New vs cycle876
At ~6.7s the previous scene03 still displayed an intermediate ranking in which a partially drawn 6月 bar appeared smaller than 4月, although the true data have 6月 highest. This is a visual-state defect, **not** a defect in the completed final chart. This change renders each bar at its **final source-derived height** or not at all; complete groups reveal at local frames 9, 26, 43. All ten genre datasets are sourced from existing `cycle874.chart_truth.GENRES`. The review-only AI-work MP4 replaces only frames 170–250 (5.667–8.367s) inside y=285..1245, keeping inherited Japanese audio and subtitle strip unchanged.

## Audio/subtitle independent partial audit
New `audio_caption_audit.py` independently decodes audio to 16 kHz PCM and checks 20ms RMS acoustic activity against eight inherited sentence-caption windows. This is **NOT ASR**: non-silent music/noise may count as activity, and the audit **cannot** establish Japanese spoken content, caption meaning, phoneme alignment, or naturalness. This limitation must remain explicit.

## Local review-only rendering
```bash
PYTHONPATH=. python -m unittest discover -s cycle877 -p 'test_*.py' -v
PYTHONPATH=. python cycle877/chart_reveal.py --source /PRIVATE/cycle876.mp4 --output /PRIVATE/cycle877.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/render.json
PYTHONPATH=. python cycle877/audio_caption_audit.py --video /PRIVATE/cycle877.mp4 --report /PRIVATE/audio_audit.json
```

The exact manifest is `POLICY` plus SHA256 of the private source. Do not commit private media, audio, frames, customer data, or unapproved user storyboard. GitHub CI only checks code and **synthetic** A/V. Original v33 reference video, full research chat transcripts and smartphone playback unavailable; inherited rights and staff approval unverified. Manual posting after staff approval only. No merge, paid services, or automatic posting.

## Verified local review result (2026-10-27)
- Input SHA256 `c4fd5618ca2b626e990b3f7507eb03b30d1b63611adb6ed3499d7759333845f6`.
- Output SHA256 `510cf34d7094539ff1472142a6b48ebc7282fb198844d8a732918150e598632e`.
- H264 1080x1920, 30fps 691 frames 23.033s, AAC 48kHz; full video/audio decode PASS.
- Source/output AAC ADTS hash identical `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 81/81 target frames changed; subtitle/footer ROI full 691 frames maximum mean pixel delta 0.0372; outside target max 0.1031 (downsampled 135x240).
- 12/12 local unit tests PASS. All eight caption windows contain non-silent audio by RMS threshold; **not** a speech transcript or semantic timing check.
- User storyboard previously directly inspected; this run re-used accessible storyboard findings, original file and v33 MP4 not accessible.
