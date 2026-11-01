# cycle1199 — content-only feathered slow push-in (HUMAN_REVIEW)

Previous cycle1197: narration RMS-driven seven-bar animation. This cycle: a different visual change — subtle content-panel camera push (1.000x to 1.018x) with a 36px feathered mask. Header, Japanese subtitle/narration region, audio meter and compliance footer remain outside the modified ROI. No third-party assets, network calls, automatic posting, merge, or paid services.

## Usage
```bash
python quality/cycle1199/code/content_parallax.py source.mp4 output.mp4 --genre ai
python -m unittest discover -s quality/cycle1199/tests -p 'test_*.py' -v
python quality/cycle1199/tests/ci_smoke.py
```
Requires FFmpeg, Python, numpy, Pillow. Input is H264/AAC 1080x1920 30fps. AAC is stream-copied; original source media is never uploaded to CI. Genre color metadata has ten reusable configurations; content ROI is common. Actual other nine genres still need layout QA.

## Local result (2026-11-02)
- Review MP4: cycle1199_CONTENT_PUSH_HUMAN_REVIEW.mp4 (local artifact, not committed)
- Output SHA256: `2acd5e7e90ab5b40cff7a0f05559f4931ebea241a449af95004b8c79472810c9`
- 22.5s, 675 frames, 1080x1920, 30fps, H264/AAC 48kHz, full decode PASS
- AAC bitstream SHA256: `76bcb9897c914d5ecebe97650cae6fc317b168fffcf19d2891ce4135627babfe` (equal to prior)
- Protected header/subtitle/footer region sample MAE: max 0.937/255 (8 sampled frames)
- First render bug: `-shortest` cut video to 670 frames; removed `-shortest`, rerendered, 675 verified.
- Unit tests 7/7; synthetic render and full decode PASS.

No claim of Japanese semantic subtitle alignment, direct v33 comparison, rights approval, phone playback or publication readiness. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Employee approval and manual posting only.
