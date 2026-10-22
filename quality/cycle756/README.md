# cycle756 — mobile-legible result-first hook (REVIEW ONLY)

Baseline cycle755 SHA-256: `9a1903f2cd5299409e4f8b2352a3b020ebe5d09565da3f5c2f700d8b405c04b0`.

Problem: at phone-preview size the proof result in the first 1.5 seconds was too small. Change: 0.0–3.2s uses original high-contrast Japanese typography with a large 65万円 result and a cropped local Calc screenshot (synthetic sales values). Audio is copied bit-for-bit; other scenes are not intentionally altered.

Renderer (exact code used locally): `quality/cycle756/src/mobile_hero.py`.
Tests: `quality/cycle756/tests/test_mobile_hero.py`.
CI: `.github/workflows/cycle756-mobile-hook.yml`.

Reproduction requires local review-only cycle755 MP4 and `calc_b6.png` from the cycle747 local QA bundle; neither binary is committed because voice/asset rights and publication are not approved. Never use confidential images. Run:

```bash
python quality/cycle756/src/mobile_hero.py --source cycle755_EVIDENCE_CHART_REVIEW_ONLY.mp4 --screenshot calc_b6.png --output cycle756_REVIEW_ONLY.mp4
python -m pytest -q quality/cycle756/tests/test_mobile_hero.py
```

Original v33 source not found; v33 MP4 not directly available this run. This is a reimplementation, not proof of equivalence. Japanese pronunciation, speech-caption timing, real-device preview, and rights require human review. No merge, no auto-post, no paid services. Employee approval and manual TikTok posting only.
