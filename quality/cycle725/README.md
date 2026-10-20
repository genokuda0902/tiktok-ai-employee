# cycle725 — semantic circuit animation (human review)

A zero-cost, reusable 10-genre motion overlay for vertical image slides. Unlike cycle724's caption-card work, cycle725 animates the *meaning* of the image: GPIO → resistor → LED → GND and LED glow in scene five.

Source: cycle724 human-review MP4; 1080x1920 H.264/AAC, 30 fps, 605 frames, Japanese narration from cycle719 stream-copied and 16 Japanese captions retained. No auto-posting, paid services, merging or public approval.

Run: `python -m unittest discover -s quality/cycle725/tests`; `python quality/cycle725/src/focus_motion.py --input cycle724.mp4 --output cycle725.mp4` (Pillow + FFmpeg).

Nine additional genre palettes are configured but full video generation for them is not tested. Voice naturalness, rights to inherited assets, reference parity, and smartphone playback need human review.
