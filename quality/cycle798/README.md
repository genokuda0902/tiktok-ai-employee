# cycle798 — guided image-slide motion (HUMAN_REVIEW)

**Changes from cycle797:** remove redundant large headings inside artwork, enlarge the main visual and add scene-specific instructional focus (connection steps, input→process→output, cursor, completion check) plus an unobtrusive per-scene progress line.

This branch contains the reusable **10-genre motion contract**, seven tests and CI. The full local Pillow/OpenCV/FFmpeg renderer, inherited voice track, AI-derived art and Japanese MP4 are packaged separately for human review, **not uploaded to GitHub** because inherited audio and image provenance remain unresolved. CI only generates a synthetic 1080×1920 MP4 with an electronic tone; it is not the user-ready Japanese video.

Local QA of the review MP4: 429 frames, 1080×1920 H.264/30fps, AAC/48kHz, bit-identical inherited audio elementary stream, complete decode, eight visually changed scenes, preserved subtitle region, 14/14 checks.

**Limits:** not verified against user reference video, not audited for Japanese pronunciation, no phone-device playback, no rights clearance. No auto-post, no merge, no paid service. Employee approval required before any manual posting.

Use `motion_contract.py` as the shared timing, color and attention coordinate source for a future independent renderer. The exact complete local renderer is in the cycle798 ZIP.
