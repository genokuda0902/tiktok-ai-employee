# cycle833 — cinematic image-led hook (2026-10-25 JST)

## Sources and baseline
- Baseline: **unmerged Draft PR #154**, itself stacked on unmerged #153/#150. Alternative #155 is a geometry-only PR; do not merge either automatically.
- Current main checked at `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- TikTok市場分析 / TikTok動画研究: prior **summaries only** accessible; full task transcripts unavailable.
- User's 16-panel ChatGPT×Excel storyboard: previously inspected; original v33 MP4 **unavailable in this run**, no direct quality parity comparison.
- PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md read. v33 source code and original prompts still missing.

## Actual change
- Reimplementation, not original v33. First 101 frames (0–3.367s) of the AI仕事術 video can now use an independently generated cinematic desk still with gentle horizontal pan and alpha fades.
- Only image region x=54..1026, y=390..1210 is replaced. Original title, CTA (y>=1240), Japanese burned-in captions (y>=1450) and subsequent scenes remain in place.
- Original AAC narration stream is copied bit-for-bit, **not** newly generated or independently speech-recognized.
- Ten-genre safe-zone validation, fail-closed invalid inputs, and synthetic AV integration test. CI runs only fictional PPM + synthetic sine tone; it does **not** render the final Japanese MP4 with the private local review image.
- AI-generated source photo is local only and **not committed** pending public-use review; CI parity is not claimed.

## Local reproducible command
```bash
python quality/cycle833/photo_insert833.py --base path/to/cycle832_PHOTO_FIRST_JAPANESE_HUMAN_REVIEW.mp4 --photo path/to/approved-or-review-only-photo.png --out path/to/cycle833_CINEMATIC_HOOK_JAPANESE_REVIEW_ONLY.mp4
python -m unittest discover -s quality/cycle833 -p 'test_*.py' -v
```

## Local measured checks (full review MP4, separate from synthetic CI)
- H.264, 1080x1920, 30fps, 775 frames, 25.833s, AAC/48kHz, full AV decode PASS.
- Original and revised AAC ADTS SHA256: `c0fdb1450eea77f8f2a0f08ff07c71469fd275252feea40efc082792805256d9` (identical).
- MAE vs cycle832 at 1.2s: 48.4583/255; at 4.2s: 1.4327/255 (re-encode difference). Camera motion ROI MAE 1.2→1.8s: 10.765.
- QA first used a too-strict scene2 MAE<1 threshold and failed; corrected to <2 to account for re-encoding. No hidden failure.
- Japanese pronunciation, semantic caption sync, smartphone playback, source rights, employee approval and v33 parity NOT verified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, no automatic posting, no paid APIs, no private customer data.

Next: independent speech verification, source image rights review, genuine sanitized workflow footage, more varied original photos across the remaining seven scenes, and actual smartphone QA.
