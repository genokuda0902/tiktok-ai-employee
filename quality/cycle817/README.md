# cycle817 | clean-source Japanese slide renderer

This branch is review-only. It **does not post, merge, buy, or call paid APIs**.

## Change from cycle816

- cycle816 overlays captions on an already-encoded video, leaving room for inherited captions and repeated lossy encoding.
- cycle817 renders from the eight original 1080×1920 PNGs and original Japanese voice file.
- It removes the source slide's old caption panel and draws a clean caption panel.
- It preserves eight scenes, 24 pause-guided Japanese karaoke states, subtle zoom and ten genre accent themes.
- It normalizes narration to target -18 LUFS / -2 dBTP; this is a loudness adjustment, **not** a new voice model.
- It encodes video first and muxes the full narration in a second stage to prevent truncated audio on interrupted renders.

## Run locally with approved assets

Install FFmpeg, Pillow, and Noto Sans CJK JP. Create:
- source/scene_01.png through source/scene_08.png (1080×1920)
- source/voice.m4a (Japanese narration)
- source/voice_timing.json (8 sentences and durations)

Then:

python quality/cycle817/render817.py --root /path/to/cycle817 --output /path/to/cycle817/output/cycle817.mp4

Tests:

python -m unittest discover -s quality/cycle817 -p 'test_*.py' -v

CI runs only source-level tests. It does **not** produce the real video artifact, because media inputs have not been published to the repository. The complete media package is available only in the conversation artifact. Voice model/image rights, smartphone playback, exact word-level synchronization, employee review and publication are NOT confirmed.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Manual posting only after employee approval.
