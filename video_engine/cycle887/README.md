# cycle887 — narration-reactive seven-band header (review only)

## Difference from prior cycles
- cycle885 (accessible local MP4): 71px Japanese captions with safe-width validation; header remained static.
- cycle886 (GitHub PR #253 only): offline Chromium fill/verify/save scene; its MP4 is not available in this run.
- **cycle887:** seven independently measured frequency-band bars animated at 30fps in the empty header (x=570..750, y=61..115), preserving all previous scenes and Japanese captions.

## Offline generation
`python render.py /path/to/approved_review_input.mp4 /path/to/review_output.mp4`
Needs ffmpeg, numpy, scipy, opencv-python-headless. Source MP4 is **not** committed.
Output inherits narration and images. No assertion of rights or public-posting quality.

## Verified local MP4 (not a CI artifact)
- 1080×1920, H.264 30fps, 691 frames, 23.033333s; AAC 48kHz.
- Full A/V decode passed, audio elementary stream MD5 unchanged.
- 24 preexisting caption intervals unchanged, each contains measurable audio signal; this does **not** prove spoken words match captions.
- 637 distinct waveform states, QA 22/22, unit tests 13/13.
- Local output SHA256: see QA package; MP4 is supplied in ChatGPT, not GitHub.

## CI and limitations
CI uses only synthetic audio/video; no user assets or reference video. It cannot independently verify Japanese pronunciation, word-level sync, reference-v33 comparison, commercial reuse rights, actual phone playback, or employee approval.
Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
No paid subscriptions, posting, merging, or automatic publication. Actions billing not independently verified.
