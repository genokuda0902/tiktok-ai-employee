# cycle802 — optical centering, scene-safe (REVIEW ONLY)

The cycle801 MP4 is 1080x1920 but its opening and end-card information group was left-heavy (approx x=60..770, center=415 vs canvas center=540). This cycle shifts **only** 0.0–3.2s and 20.8–23.85s 136px right (new centre approx 551). Intermediate scenes are intentionally untouched: they have UI near the right edge and shifting would crop it. This was caught during local preview and fixed before the final render.

The left extension repeats the first two source pixel columns instead of adding a hard black seam. Important content remains <=906px, leaving >=174px for right-side TikTok UI. No aspect ratio stretch or new images, voices, captions, music or numbers. Same config validation for 10 genres; one AI-workflow video was rendered locally.

Local (do not commit inherited video): `python quality/cycle802/reframe.py --config quality/cycle802/config.json --source-video <LOCAL_REVIEW_MP4> --output <LOCAL_OUTPUT_MP4> --review-only`

CI creates only a 2-second synthetic video and sine tone, **not** the 23.8-second Japanese narrated completed video. User media and audio rights are unverified, so NEVER upload to GitHub, merge, publish, auto-post or deliver to employees. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Japanese speech meaning/naturalness, semantic subtitle sync, v33 original comparison and mobile playback remain unverified. This is a reimplementation, not recovered v33 source. Budget: 0 JPY.
