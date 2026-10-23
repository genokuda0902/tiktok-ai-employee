# TikTok cycle787 — Artwork-only enhancement

Previous cycle786: high-contrast Japanese captions.
This cycle: **artwork-only** shadow/detail lift on x=42,y=378,w=846,h=662 (1080x1920).
The header and caption region are outside the processing ROI. The AAC Japanese narration is stream-copied.
Output: H.264 30fps 1080x1920, AAC 48kHz, faststart.

Run: `python cycles/cycle787/src/artwork_enhance.py --input master.mp4 --output enhanced.mp4 --genre science`
Test: `python -m unittest discover -s cycles/cycle787/tests -v`

Ten genre presets are defined, but only the science video was rendered this cycle. No posting, no paid service, no merging. Existing master asset rights, smartphone playback, and human voice naturalness remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
