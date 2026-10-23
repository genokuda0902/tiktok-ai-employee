# cycle796 — original audio gap ambience (review-only)

## Problem and delta
cycle795 retained the previous narration but had eight 0.8–1.1 second silence gaps detected at -36 dBFS. This experiment adds a very low-level, wholly code-synthesized chord bed, stronger **only inside gaps**, so the pauses sound intentional without editing speech timing or video pixels. It is a subjective audio design candidate, not a proven improvement in engagement or naturalness.

## Run

```bash
python quality/cycle796/audio_gap_bed.py --config quality/cycle796/config.json \
  --source /local/review-only-cycle795.mp4 \
  --output /local/cycle796_AMBIENT_GAP_REVIEW_ONLY.mp4 \
  --bed /local/cycle796_bed.wav --report /local/qa.json
```

Requires Python 3.11+, FFmpeg/ffprobe. No downloaded music, voice model, paid service or personal data. The inherited source MP4/audio is not committed and remains **rights-unverified, employee-unapproved**. The render copies the video bitstream and re-encodes a mixed AAC track; compares decoded voice with source, packet hash, duration, codec and full decode. The bed is generated from sine waves and has no externally sourced samples. Do not infer commercial rights of inherited material from this change.

Actual ten genres follow `TikTok_10ジャンル_初期100企画.xlsx` rather than the placeholder genre set from earlier drafts.

GitHub CI creates a separate synthetic-color + sine-tone MP4 to prove reproducibility, NOT the user's Japanese-narrated video. `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`. No automatic publishing, merging or purchasing. Speech content, voice naturalness, semantic subtitle alignment and device playback still require human/independent checks. Original v33 MP4 and complete TikTok research task transcripts were not retrieved.