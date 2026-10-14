# Cycle584: truthful temporal proof hook (review only)

Date: 2026-10-15 JST. Cost: JPY 0. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Baseline and change
- Baseline cycle583 local MP4 SHA-256: `f715195494b0ce40a4d13414bbb3ede63f45bdaa43fb47ba128fb2583b6092e0`.
- Previous opening showed an unsubstantiated intermediate counter (e.g. 277) although the validated sum was 720.
- Rebuild 0-2s and loop re-entry 19-20s. Only prefix sums 120, 270, 470, 720 can be displayed as intermediate totals.
- New MP4 SHA-256: `b9e7304e9929a521dfd03f3cb3c28a13bd8e29147642f48c9f03000b400ba191`.
- Reuse 2-19s and existing audio/subtitle streams. No new Japanese narration; soundtrack is inherited BGM/SFX.
- Genre-neutral arithmetic contract tested across 10 genre identifiers, not ten fully rendered videos.

## Reproduction
Requires Python 3.11, Pillow, ffmpeg, ffprobe and Noto CJK fonts.
Run from this folder with the verified local cycle583 MP4 (not committed due to media/rights controls):
```bash
python -m unittest -v test_cycle584.py
python build.py --source /path/to/cycle583_kinetic_contrast_REVIEW_ONLY.mp4 --output cycle584_truthful_hook_REVIEW_ONLY.mp4
ffmpeg -v error -i cycle584_truthful_hook_REVIEW_ONLY.mp4 -f null -
```
Source SHA mismatch fails closed. CI only tests source/logic, not MP4 generation (baseline video is not in GitHub).

## Provenance and release restrictions
- User storyboard `ChatGPT×Excel時短術16コマ絵コンテ.png` inspected for pacing/structure, **not** embedded.
- Original v33 MP4 unavailable in this run. Not a quality-equivalent reproduction.
- Original graphics are generated in Pillow. Inherited soundtrack and prior video assets lack complete rights approval.
- Japanese narration missing; semantic voice-caption sync not verified; rights not approved. No automatic upload or posting.
- Existing repo handoff: `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`.
- Next: secure free licensed Japanese TTS + timestamp alignment, and reference v33 direct comparison.

## Verification
- Local unit tests: 12 PASS.
- MP4: 20s, 1080x1920, H.264 30fps, AAC, Japanese mov_text subtitle track; full decode PASS.
- The frame renderer is a synthetic recreation, not a recorded AI operation.
