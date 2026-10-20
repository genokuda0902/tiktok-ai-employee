# cycle716 caption quality

- 24-second review-only MP4 is generated locally from the cycle715 review-only baseline.
- Caption overlay is positioned inside a 200-pixel bottom exclusion zone.
- No Japanese speech is generated. On-screen captions are NOT speech-synced.
- Original reference v33 was not accessed. Do not claim v33 equivalence.
- No publication, employee delivery, merge, or paid services.
- Local test command: `python -m unittest -v test_caption_overlay`.
- Run: `python caption_overlay.py INPUT.mp4 OUTPUT.mp4`.

## Verified local artifact (2026-10-20 JST)
- cycle716_japanese_focus_captions_BGM_ONLY_REVIEW_ONLY.mp4, 24.0s, H.264 1080x1920 30fps, 720 frames, AAC BGM/SFX, full decode PASS.
- SHA256: 08d38190fd326c41d5f2bece83338c12d7ba57b063f442e7513b244fd75cc569
- 8 local unit tests PASS. GitHub branch contains 2 compact QA tests; no CI run.
- At 13.5s upper-image mean difference 0.11 and caption-region mean difference 29.44 vs cycle715. Graph totals remain visible.
- Japanese narration MISSING, speech-sync NOT TESTABLE, smartphone playback NOT TESTED, rights and employee publication approval NOT GRANTED.
- Full local renderer + baseline MP4 + logs provided in ChatGPT cycle716 ZIP, not uploaded to public GitHub.
