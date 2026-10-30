# cycle1029 — three-stage CTA focus (HUMAN_REVIEW)

Distinct from cycle1027's shadow lift: this cycle highlights three actionable CTA cards in sequence in scene 8 (19.767–22.5s). Source is the locally verified cycle1027 MP4, not a new generative clip. The renderer changes only a narrow border around each card; no audio, burnt captions, or top navigation are intentionally modified.

## Reproduce with local review source
```bash
python quality/cycle1029/code/focus_3steps.py input.mp4 output.mp4 --genre ai_work
python -m unittest discover -s quality/cycle1029/tests -v
```

10 genre palette presets are defined, but non-ai_work footage requires the matching three-card layout or explicit `--boxes-json` coordinates. Only the AI-work real MP4 has been visually tested. CI creates and decodes synthetic AV media only; no user video or private assets are uploaded to GitHub.

## Actual local review MP4 QA
- 22.500s, 1080×1920, 30fps, H.264, 675 frames, 8 original chapters.
- Japanese-tagged AAC 48kHz audio packet stream SHA256 identical to source: `da601fdd17eae3cc1c0fe9a0d93843f6c07e1321d33f84f92474819c477d8b18`.
- Full AV decode PASS; 9/9 local unit tests PASS.
- Active border MAE 41.430 / 44.612 / 42.438 (three stages), while protected caption area MAE 0.342 / 0.360 / 0.463 (0–255 scale).
- Independent Japanese ASR, subtitle semantic sync, original v33 comparison, phone playback, source commercial rights, employee approval, and viewer retention are NOT VERIFIED.

## Restrictions
PUBLICATION_NOT_APPROVED. No paid service contract, automatic posting, unauthorized merge, or asset redistribution. Employee approval then manual posting only.
