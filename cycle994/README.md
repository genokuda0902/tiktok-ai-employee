# cycle994 | shadow lift in safe content area

Compared with cycle992's three-beat prompt focus, this pass lifts dark image/UI midtones within a feathered ROI. It deliberately leaves top titles, burned Japanese captions (y>=1490), and bottom footer untouched before lossy video re-encoding. All ten genre profiles use the same renderer, but only the AI-work video was produced. No new third-party assets.

## Local reproducible review command

Python Pillow and FFmpeg are required. Input is a private, user-review-only MP4 and must **not** be uploaded to public GitHub.

```bash
python cycle994/tone_pass.py --input PRIVATE_PREVIOUS.mp4 --output PRIVATE_REVIEW_ONLY.mp4 --genre ai_work --review-only --report private_report.json
```

Synthetic CI tests only synthetic color/tone, audio, and captions. No private source media, audio, or output MP4 in the repository.

## Private local result (not GitHub artifact)

- Source cycle992 SHA256 `13fac87d69ff42ee0f8bf7f17bf3ee94fef2826b2afd1725bf16785f05aad1d1`.
- cycle994 MP4 SHA256 `b9e99c1b3878815d78bd9c76391fa995739a92b2962909be1eb8b4803f90a443`.
- 1080×1920, 30fps, 691 frames / 23.033s. H.264/AAC 48kHz/mov_text; audio and optional Japanese subtitle packets identical to cycle992. Full A/V decode PASS. 5 unit tests PASS.
- Sampled 230 frames (every third frame, 1/8 pixel stride): central ROI mean luma 93.571→102.507 (+8.936/255), shadow-region mean +12.603/255; caption area max frame-mean absolute difference 0.699/255; max bright clipping increase +0.00828 fraction. Measurements are **not** a human quality score.
- The original 16-panel / ~36s storyboard has brighter cinematic scenes and more shot variety; this 8-scene / 23s video is not equivalent.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Japanese speech has not been independently transcribed or aligned to subtitles. Commercial source rights, actual v33 original MP4, phone playback, employee approval, and Actions actual billing are unverified. No auto posting, merge, paid contract, or public release.
