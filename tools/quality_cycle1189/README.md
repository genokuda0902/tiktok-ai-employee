# Cycle 1189 — UI save motion, review only

## Distinct improvement from cycle1187
- cycle1187: audio-only EQ (80Hz highpass and +1.3dB at 3.2kHz), no visual change.
- cycle1189: scene 07 UI operation gets a vector cursor moving from prompt editor to save library, a click ripple and a checkmark. This improves the **demonstration of an action**, not only image sharpness.
- No real mouse operation or actual external save was performed: it is a motion graphic on synthetic sample UI.
- Source Japanese narration bitstream is preserved exactly, 8 chapters and burned subtitles are retained.
- Ten genre IDs/palettes and configurable safe-area UI coordinates are available; only the AI-work genre was rendered as a final 22.5s MP4.

## Reproduction
```
python -m pip install Pillow
python tools/quality_cycle1189/code/ui_save_motion.py SOURCE_1080x1920.mp4 REVIEW_ONLY.mp4 --genre ai
python -m unittest discover -s tools/quality_cycle1189/tests -p 'test_*.py' -v
python tools/quality_cycle1189/tests/ci_smoke.py
```

## QA boundaries
Local real 22.5s output: 1080x1920 30fps H.264, 675 frames, 8 chapters, AAC 48kHz Japanese-tagged audio. Audio stream SHA256 equal to source, full decode PASS. 15 unit tests pass. Overlay is constrained to x260–970/y650–1160, leaving y1350–1920 narration captions/footer untouched except H.264 re-encoding differences (sampled max MAE 0.6557/255).

GitHub CI uses synthetic 2.2s color footage and sine tone only. **No private source video, real Japanese narration or final MP4 is committed.** CI does not verify the actual private MP4.

Unverified: independent Japanese ASR/semantic alignment, reference v33 original comparison, real smartphone playback, commercial-use rights, staff approval, actual GitHub Actions billing. Do not merge or post without staff approval.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**
