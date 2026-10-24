# cycle803 — original centered CTA (REVIEW ONLY)

## What changed
Replaces ONLY the final 20.8–23.8 s (90 frames) of the previous local 23.848 s review video with a newly drawn 1080×1920 CTA scene. Centered full robot (no cropped face), larger readable Japanese SAVE call-to-action, original procedural bokeh/light and animated highlight. Ten genre palettes share one renderer; one AI-work-efficiency example was rendered. This is a vector/gradient illustration, **not** reference v33's cinematic 3D render.

## Local command (source rights unverified; NEVER commit source footage)
```bash
python -m pip install Pillow
python quality/cycle803/cinematic_cta.py --frames /tmp/cycle803-frames --source-video /private/cycle802_OPTICAL_CENTER_REVIEW_ONLY.mp4 --output /private/cycle803_REVIEW_ONLY.mp4 --review-only
python -m unittest discover -s quality/cycle803 -p 'test_*.py' -v
```

Free Japanese Noto CJK font and FFmpeg are required. Only the last 90 frames change; AAC packets are stream-copied from the local inherited video. Source image/voice rights and speech/caption semantic matching are **unverified**.

## CI (original synthetic-only media)
CI generates a **3.0s 1080×1920 30fps H264/AAC MP4 with a synthetic 440Hz tone**, not the 23.848s Japanese-voice review video. It includes no inherited image/audio, no external commercial assets, no automatic post, no merge. The original image source is Pillow drawing code; Noto CJK font is installed as a system dependency (do not redistribute fonts).

## Safety
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Original v33 MP4 and full TikTok市場分析/TikTok動画研究 task transcripts were not accessible; user's 16-panel storyboard and prior summaries were inspected. Actual comparison with v33, speech meaning/naturalness, phone playback, original inherited media rights, employee approval are pending. Only approved assets may be used in a future reproducible full-length CI pipeline. No TikTok auto-posting.
