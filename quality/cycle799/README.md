# cycle799 — cinematic reframe (HUMAN_REVIEW)

Compared with cycle798 guided-motion UI, this cycle makes the main image area larger
(912×669 → 940×770, **+18.6%**) and replaces the busy grid/chrome with a mobile-first
editorial card, darkened takeaway band and restrained 1.5% push-in. The previous
Japanese voice track and 16 subtitles are **inherited** from a local source MP4.

## Reproduce locally

Install Python packages `opencv-python-headless numpy pillow`, FFmpeg and
Noto Sans CJK fonts. Run:
```
python cinematic.py --source SOURCE_1080x1920_429frames.mp4 --output review.mp4 --genre science
python -m unittest -v test_cinematic.py
```

The full renderer **is committed here**. The CI job creates a synthetic source with
an electronic tone, executes this same renderer end-to-end, and uploads a synthetic
test artifact. The Japanese-narrated local MP4 is not uploaded to GitHub because
the inherited audio and image provenance have not been rights-cleared.

## Release gate

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No auto-post, no merge, no paid
service. Reference-video parity, natural Japanese pronunciation, phone playback,
asset rights and employee sign-off remain unverified. Manual posting only after approval.
