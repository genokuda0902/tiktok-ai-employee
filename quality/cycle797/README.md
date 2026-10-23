# cycle797 — crop-safe opening hook / review only

Purpose: repair cropped Japanese card footers in the first 3.2 seconds of the inherited local review video. Replace the opening with a deterministic image-first layout: full-width BEFORE/AFTER labels, a separate subtitle lane, and a distinct fictional-data notice. This is a **reimplementation**, not recovered v33 code.

## Safety

The source MP4s and extracted people/screenshots are unapproved local review assets. **Never commit/upload them**. This repository contains only Python, JSON, tests and synthetic CI. No external images, third-party music, private footage, publishing, merging, or paid services. 10 genres share the same safe-layout geometry. Fails closed on publication and rights flags.

## Local rendering (requires local review-only MP4s)

```bash
python -m unittest discover -s quality/cycle797 -p 'test_*.py' -v
python quality/cycle797/hook_layout.py \
  --config quality/cycle797/config.json \
  --source /local/cycle796_AMBIENT_GAP_REVIEW_ONLY.mp4 \
  --clean-hook /local/cycle790_OPAQUE_WIPE_REVIEW_ONLY.mp4 \
  --output /local/cycle797_CROP_SAFE_HOOK_REVIEW_ONLY.mp4 \
  --report /local/cycle797_qa.json \
  --opener /local/cycle797_opener.mp4
```

Requires Python 3.11+, Pillow, OpenCV, FFmpeg/FFprobe (local). Local reference MP4s are not in GitHub due to rights restrictions. GitHub CI validates synthetic layout only; it does **not** reconstruct a Japanese-narrated user video. Narration content, meaning alignment, rights, mobile-device playback and v33 visual parity still require human verification.

## Previous cycle and next

cycle796 changed audio bed and measured 8→4 long silences; cycle797 leaves AAC packets identical and fixes **visible clipped card footer text** in the opening. Next: transcript-based Japanese narration/caption semantic QA, and approved-assets-only reproducible GitHub render; don't claim approval or parity.
