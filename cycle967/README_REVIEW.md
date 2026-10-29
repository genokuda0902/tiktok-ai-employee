# cycle967 — audio-reactive VOICE header (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Do not publish, merge, spend, or auto-post.

## Distinct quality change

Previous cycle965 added a bookmark/save CTA to the final caption. This cycle replaces the **decorative eight-bar VOICE header** with an eight-band FFT meter calculated from the **actual Japanese AAC track**. RMS gating and gentle attack/release prevent unrelated random bar motion. Only header rectangle x565..715 / y70..111 changes; the existing captions, images, final CTA, and AAC bitstream are preserved. The original narration is not modified.

Ten genre palettes are defined; only `ai_work` has an inspected header placement and may render. All other genres fail closed.

## Private actual-MP4 local verification (not GitHub CI)

- Source cycle965 MP4 SHA256: `05f98e17f0825dedb1f0334f0474f9e169f103eafaa8c448a6facc4f2b22c878`.
- cycle967 output SHA256: `fc7c5c469c41f56ce3465dca1b7ec005001e65cc1215d501017d96c6130eabad`.
- 1080×1920 H.264, 30fps, 691 frames, 23.033s, full A/V decode PASS.
- Japanese-tagged AAC 48kHz **elementary stream SHA256 identical**: `785b26ef233e7b6d2e2f1dc37b143d89cd8e2aaebb663480ee54d61d45986f43`.
- Fifteen sampled timepoints: mean change inside meter 32.130/255, max outside-meter mean difference 1.173/255 (recompression).
- 8/8 local synthetic tests PASS; CI separately runs synthetic 3-second A/V, **not the private full MP4**.

## Research and limitations

Accessible prior TikTok market/video research summaries emphasize strong hook, clear Japanese subtitles, purposeful cuts, authentic demonstration, and human review. User's 16-panel storyboard is known from accessible prior summaries; original v33 reference MP4 was not accessible in this run. No independent Japanese ASR; meaning/timing alignment between narration and subtitles remains **NOT VERIFIED**. Inherited-media commercial rights, smartphone playback, employee approval, actual Actions billing, and reference parity remain unverified.

This is a presentation/visualization improvement, **not** evidence of increased engagement or speech-to-text correctness.

## Reproduce using authorized local media

```bash
python3 -m pip install numpy Pillow
python3 cycle967/code/voice_reactive.py --input authorized.mp4 --output review.mp4 --report qa.json --genre ai_work
```

No user/private media or external images/audio are committed to this public repository. Manual posting only after employee approval.
