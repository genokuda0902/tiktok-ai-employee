# Cycle 1181: protected-panel shadow recovery

- Previous cycle1179: diagram sharpening / contrast restoration.
- New, different improvement: bounded shadow/midtone lift (gamma 1.08–1.15) inside the central diagram panel only.
- Input: cycle1179 22.5 s MP4; output: 1080x1920, 30fps, H.264/AAC, 675 frames.
- 10 configurable genre presets, one rendered AI genre.
- Local unit/synthetic integration tests: 9/9 PASS.
- Full output decode: PASS.
- Sampled dark-region mean luma gain: +11.78/255 (8 sampled frames; not a perceptual readability score).
- Header, subtitle, footer sampled mean absolute pixel differences: max 0.345, 0.126, 0.035 /255 respectively.
- Audio AAC bitstream: identical to previous output.
- Independent Japanese ASR, subtitle semantic match, original v33 reference comparison, commercial rights and smartphone hardware playback: NOT VERIFIED.
- No paid services, merge, posting or employee approval.
- Publication status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- Source output MP4 and QA are delivered separately as conversation artifacts; CI uses synthetic media only.
- Next: independent Japanese ASR and timed caption meaning checks, then rights and mobile playback verification.

To test:
```
python -m unittest discover -s quality/cycle1181/tests -v
```
To render:
```
python quality/cycle1181/code/shadow_recovery.py SOURCE.mp4 OUTPUT.mp4 --genre ai
```
