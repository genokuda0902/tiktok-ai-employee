# cycle581 — TikTok-safe Japanese captions (HUMAN_REVIEW)

Input: cycle580 MP4 (provided separately; inherited media rights not cleared). Output: 1080×1920 H.264/AAC MP4, 15.6 s, 30 fps. Change: move existing Japanese captions from the lower UI-obscured band into a conservative central safe area (x=80–900, y≤1436), enlarge Japanese type, increase contrast, fade out noisy old lower-third. Nine cue boundaries are derived from prior **visible caption changes**, not speech recognition. Audio AAC packets are copied unchanged. 10 genre palettes are supported.

Rebuild: `python quality/cycle581/build_cycle581.py --source /path/to/cycle580.mp4` (requires FFmpeg, Pillow, Noto Sans CJK). Test: `python -m unittest discover -s quality/cycle581/tests -v`. Video input is intentionally not committed. No automatic posting, no paid services, no merge. Language/naturalness, semantic subtitle sync, source rights, phone playback, and in-app placement still require human review.

Status: `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`.