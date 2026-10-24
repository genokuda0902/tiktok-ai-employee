# cycle813 — cinematic motion (human review only)

**Change from cycle812:** a continuous 30fps, gentle pan (13px horizontal, 16px vertical) and Lanczos 3% reframing, plus restrained contrast, saturation and sharpening. cycle812 used 24 caption-phase still images with no continuous camera motion.

**Input:** a locally generated, 1080×1920, H.264 30fps MP4 with Japanese AAC 48kHz and the existing 24 caption states. The voice and captions are preserved, **not regenerated**.

**Run (offline):**

```bash
python quality/cycle813/motion_filter.py --input previous_review.mp4 --output cycle813_review.mp4
python quality/cycle813/test_motion_filter.py
```

This repository contains the motion renderer and tests, not the source portrait, licensed voice, or completed review MP4. The complete locally verified MP4 and QA report are attached to the conversation. CI uses a synthetic video/audio fixture to verify output resolution, decode and audio integrity; CI success does **not** establish quality parity with a reference TikTok video.

**Local review evidence:** 1080×1920 H.264 30fps, 775 decoded frames, 25.833s, AAC 48kHz; audio SHA-256 equal to cycle812. First scene same-caption frames 10 and 30 had a mean absolute difference of 9.64 (0–255) vs 0.002 in cycle812, proving temporal motion rather than a repeated still.

**10 genre keys:** `ai_work`, `beauty`, `love_psychology`, `money_saving`, `sales_business`, `career`, `health_life`, `science`, `travel_food`, `product_life`.

**Limitations:** inherited image and Open JTalk voice rights and any attribution requirements are not cleared. Naturalness of voice, word-level caption synchronization, smartphone playback, reference video parity, and employee approval are not verified. Do not publish, auto-post, merge, subscribe, or incur charges.

**Status:** `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`. Employee approval is required before **manual** publication.
