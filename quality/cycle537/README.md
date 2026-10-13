# Cycle537 — Clean CTA / loop (REVIEW ONLY)

Date: 2026-10-13 JST. This is a reimplementation, NOT original v33 source.

## Sources reviewed
- Main commit 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md (no confidential prototype or unapproved assets).
- Prior cycle536 source and review MP4 (SHA-256 8a0882637d8ab270968375d71c30a3ed2dac4289d6b5206673b29580f00cc7a0).
- Owner-provided ChatGPT×Excel 16-panel storyboard image. Reference v33 MP4 and full market-research task texts were NOT accessible.
- Research summaries: early hook, one message, clear Japanese text, operation demo, Before/After, CTA, safe areas.

## Implemented and verified
- Replaces 18.5-19.7s with a fully opaque synthetic Japanese save CTA; 19.7-20.0s holds the opening frame to eliminate the previous 19.3s double-image.
- Ten-genre configuration and fail-closed rights/privacy, fabricated-results and publication gates.
- Local MP4: 1080x1920, H.264, 30fps, 600 frames, 20s, AAC; full decode passed.
- Source audio stream MD5 == output audio stream MD5 (1bec744c7101be78368869e611b57b3e). This is NOT proof of Japanese narration.
- 19s image mean absolute difference vs cycle536: 31.99; unchanged 7s: 0.142; first/last frame difference 1.09 due to video compression.
- Output SHA-256: acb1fc2b07f5789bc675fbca23d16c867e6577c93d294cd9f0c1afd100d618ef.
- Local 11 tests PASS; Actions run 38335058948: SUCCESS, 11 tests PASS.
- Output MP4 is provided separately in conversation artifacts, not stored in this repository.

## Reproduce (requires the prior review MP4 as input)
Install ffmpeg, Pillow and Noto CJK fonts.
```
python -m unittest discover -s quality/cycle537 -p 'test_clean_cta_loop.py' -v
python quality/cycle537/clean_cta_loop.py --source cycle536_semantic_closeup_REVIEW_ONLY.mp4 --output cycle537_REVIEW_ONLY.mp4 --config quality/cycle537/config.json
```

## Blocking quality gates
New native Japanese narration: NOT GENERATED. Narration/subtitle synchronization: NOT VERIFIED.
Reference-v33 equivalence, human listening and posting approval: NOT APPROVED.
Never auto-post, auto-merge or upload private media. Employee manual posting only after explicit approval.
