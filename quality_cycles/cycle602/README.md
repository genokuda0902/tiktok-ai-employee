# cycle602 — ambient circuit continuation (review only)

**Cost:** ¥0. **State:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Change from cycle601
Replace the large flat/empty lower third with a subtle palette-driven circuit background and a slow 24px drift. No critical text in the TikTok UI region. The upper 1230 pixels, Japanese caption artwork and CTA remain visually unchanged (encoding MAE < 1.5). AAC audio packets are copied without modification.

## Reproduce
The original `cycle601_baseline.mp4` is NOT stored in GitHub; obtain it from the separately supplied cycle602 ZIP. Put it at `quality_cycles/cycle602/assets/cycle601_baseline.mp4`. Install `numpy` and `Pillow`; install `ffmpeg`. Then:

```bash
cd quality_cycles/cycle602
python build_cycle602.py
python -m unittest discover -s tests -v
```

Default output: `output/cycle602_AMBIENT_CANVAS_HUMAN_REVIEW.mp4` (1080×1920, H.264/AAC, 15.6s). The GitHub test suite covers only deterministic renderer properties; **it does not validate the MP4** without the separately supplied baseline and QA script.

## Approval gate
Japanese pronunciation, speech/subtitle semantic sync, rights to inherited audio/images, TikTok mobile playback and reference-video quality parity are NOT verified. No auto-posting, paid services, merge or publication approval.
