# cycle800 — Readable Japanese captions (DRAFT / HUMAN_REVIEW)

**New vs cycle799:** rebuild the existing 16 Japanese burned-in subtitle phrases in larger Noto CJK type, with a cyan emphasized keyword, underline, opaque dark background and per-genre accent colors. Caption safe area: y=1510..1770 on 1080x1920. 10 genre configurations. No changes to source video outside the caption band (except unavoidable H.264 re-encoding). Audio stream copied.

## Reproduce (source rights required)
Install FFmpeg, Python 3.11+, OpenCV, Pillow, NumPy, Noto CJK font.

```bash
python -m unittest -v quality/cycle800/test_caption_rebuild.py
python quality/cycle800/caption_rebuild.py \
 --source /path/to/authorized_source.mp4 \
 --output /tmp/cycle800_REVIEW_ONLY.mp4 \
 --captions quality/cycle800/captions_science_review.json --genre science
```

Input contract: 1080x1920, 30fps, 429 frames for the included caption JSON; AAC audio must be present. Other lengths and genres work with their own properly timed JSON cues. **This code does not generate new Japanese speech.** The local review MP4 uses inherited Japanese audio whose provenance and publication rights have NOT been verified. No media from prior cycles is committed here.

Local final: 14.314s, 429 frames, H.264/AAC 48kHz; 16/16 local checks pass; 8/8 unit tests pass; PCM audio MD5 same as cycle799. The CI MP4 uses a 440Hz electronic test tone, **not** Japanese speech. No automated posting, merge, purchase, employee approval or claim of reference-video equivalence.

## Prior cycle and delta
- cycle799: enlarged illustration + restrained zoom.
- cycle800: replaced small subtitles with high-contrast keyword-highlighted captions; exact original 16 phrase intervals were manually transcribed from local frame review.
- First local attempt failed visually due to incorrect alpha normalization (white cards); fixed by dividing RGBA alpha by 255, re-rendered and visually inspected.
- Remaining: rights-cleared offline Japanese TTS, genuinely new genre MP4, actual phone playback, reference-video comparison, employee sign-off.
