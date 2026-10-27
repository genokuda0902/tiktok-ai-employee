# cycle889 — Pause-aware Japanese captions (HUMAN REVIEW ONLY)

## Distinct change from cycle888
cycle888 added eight editorial focus highlights to the mock-UI demonstration.
cycle889 uses **offline FFmpeg speech/silence detection** to shorten caption visibility during measured speech pauses, while preserving the existing Japanese caption strings, eight scene images, and original AAC audio elementary stream.

- Source: separately shared cycle888 23.033s MP4 and inherited cycle885 24-interval ASS subtitle source.
- Detection: -38 dB, minimum silence 0.20 s; display tolerance 45 ms before and 70 ms after speech.
- Actual local video: 1080×1920, H.264 30 fps, 691 frames, AAC 48 kHz; full A/V decode successful.
- 17 detected pauses; subtitle overlap with detected silence **4.246 s → 1.122 s** (73.6% less), with 24 caption events and original text preserved.
- Local checks: **17/17**, unit tests **12/12**.
- Ten genre labels share one reusable caption retiming function; ten finished genre videos are **not** claimed.

## Local usage
```sh
python render.py /private/cycle888.mp4 /private/inherited_captions.ass /private/cycle889.mp4 /private/work
python -m unittest -v test_pause_aware.py
```

## Evidence boundaries
Speech-activity timing is **not independent Japanese ASR**, and does not establish spoken-word correctness, word-level alignment, or human-perceived readability. The local QA validates the completed MP4; GitHub Actions validates source code and a **synthetic 2-second video only**. Private inherited media and commercial rights are not uploaded or verified. User-provided v33 reference original was unavailable for direct comparison.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Employee approval, inherited image/audio reuse rights, physical smartphone playback, and actual Actions billing remain unverified. No posting, merging, paid contract, subscription, or public private-media upload.
