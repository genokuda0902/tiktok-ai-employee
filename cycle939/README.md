# cycle939 — weekly task close-up (HUMAN_REVIEW)

## Distinct change from cycle937
cycle937 applied Japanese narration clarity EQ without changing video frames. cycle939 instead replaces the small, hard-to-read three-column cards in **scene02 (2.9–5.8 s; frames 87–173)** with a crisp, native-resolution editorial close-up: week 1 → week 2 → week 3, one readable weekly-report card at a time. This is a fictional illustrative example, **not a recorded real workflow**. Existing Japanese narration and burned captions are retained. 10 genre text/color profiles are configured; only the AI-productivity example was rendered to a real MP4.

## Actual private MP4 verification
- Private review file: `cycle939_WEEKLY_CLOSEUP_JP_HUMAN_REVIEW.mp4`, SHA256 `eeeb533effdb15620aceebca5b1be450065fceafa68ce1af95cabd2dc121eabd`.
- Source: cycle937 review MP4 SHA256 `b46dc50d7dacfe44ad7c3649c6467ea6687e989071c9e17d477e85f384e9f663`.
- 1080×1920 H.264 / 30 fps / 691 frames / 23.033 s nominal / AAC 48 kHz mono.
- Full video/audio decode PASS. Original and output AAC elementary-stream SHA256 identical: `523a9d360ff3b3cdcc98730610aec21a74b97952dd469dd0a8fbd19af4042357`.
- 87 edited frames; 1/8-resolution scene ROI mean absolute delta 60.545. Max outside-scene delta 1.684 and max subtitle-region delta 1.486 (8x-downsampled pixel values, due to re-encoding).
- Audio RMS in the three edited beats: 0.07346 / 0.18006 / 0.12404. **This is audio presence only, not Japanese ASR or word sync**.
- 14/14 local unit tests PASS. CI runs Python synthetic tests only; the private MP4 is NOT uploaded to GitHub.

## Reproduce (free local tools)
Requires Python 3, OpenCV, NumPy, Pillow, FFmpeg, and a locally installed Noto Sans CJK Japanese font. Source MP4 must be a user-approved private review file.

```sh
python cycle939/src/weekly_zoom.py --source PRIVATE_REVIEW.mp4 --output REVIEW_ONLY.mp4 --genre ai_productivity
python -m unittest discover -s cycle939/tests -v
```

## Research and remaining limitations
Prior accessible TikTok市場分析 / TikTok動画研究 summaries emphasize early hooks, purposeful scene changes, readable Japanese text, real demonstrations, and manual employee review. User's 16-panel ChatGPT×Excel storyboard was located in the Library; original v33 MP4 could not be accessed directly in this run. No claim of matching the reference.

**Not verified:** independent Japanese ASR or caption semantic/timing match, inherited source media commercial rights, subjective readability or voice quality, phone hardware playback, employee approval, actual Actions billing.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No auto-post, no merge, no paid service contract, no public upload of the private video. Employee approval and manual TikTok posting only.
