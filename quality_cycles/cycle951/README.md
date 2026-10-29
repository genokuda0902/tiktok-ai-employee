# Cycle951 — Ghost-free cut repair (review only)

Local source: cycle950 STEP_BADGE MP4, 23.033333s, 691 frames. Prior cycle950 enlarged chapter badge; this cycle **removes double-exposed scene text** at 7 cut boundaries using fade-through-solid and only one clean scene snapshot at any time. Unlike cycle946's 3 adaptive wipes, this is 7-cut ghost-artifact repair and does not blend text from two scenes.

Reproduce locally (requires authorized source MP4, Python OpenCV/numpy and FFmpeg):

```bash
python quality_cycles/cycle951/deghost_transition.py --input SOURCE.mp4 --output REVIEW_ONLY.mp4 --genre ai_work --qa render_manifest.json
pytest -q quality_cycles/cycle951/tests
```

10 genre palettes configured. The source video and output are **not uploaded to public GitHub**. MP4 is supplied separately in the user's conversation. Audio AAC bitstream is copied unchanged. 77 transition frames modified; header and caption zones protected. Offline technical QA: 1080x1920, H264, 30fps, 691 frames, 23.033333s, AAC 48kHz, full A/V decode PASS, 26/26 unit tests PASS.

Not verified: independent Japanese ASR/caption semantic timing, source media commercial rights, original v33 reference side-by-side, smartphone playback, employee approval, actual GitHub Actions billing. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No auto-post, no merge, no paid contract.
