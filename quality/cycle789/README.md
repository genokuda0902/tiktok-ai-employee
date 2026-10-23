# cycle789 — photo-panel Ken Burns motion + fast CI (HUMAN_REVIEW)

**Previous cycle788:** 23.843 s, 1080×1920 H.264/AAC, 714 frames; 0–1.5 s Before/After opening. PR #71 CI run 39929277187 was CANCELLED after ~19 minutes: apt-get download of FFmpeg/OpenJTalk packages exceeded the 18-minute job timeout. No artifact was produced.

**This cycle:** animate only two photo regions (3.15–5.35 s), zoom <= 7% with a 22px feather at the panel edges, leaving all subtitles, numeric data, UI and audio untouched. This is a genre-neutral transform, but full MP4 was verified only for AI productivity. No new third-party images or services.

Local input: cycle788 review-only MP4 (not in GitHub; source rights not cleared).
```bash
python -m pip install Pillow opencv-python-headless numpy
python quality/cycle789/portrait_motion.py --input cycle788.mp4 --output cycle789.mp4 --config quality/cycle789/config.json --report cycle789_report.json
python -m unittest discover -s quality/cycle789 -p 'test_*.py' -v
```

**Local measured:** full MP4 23.843s, 714 frames, 1080×1920 30fps H.264/AAC; 11 tests PASS; AAC packet and PCM hashes match input; full decode PASS. At 4.25 s, changed photo-region mean absolute pixel difference is measurable; outside area only re-encode noise. See chat ZIP for actual source MP4, complete QA and comparison images.

**Fast CI recovery:** no apt-get; use pip wheels (Pillow + imageio-ffmpeg), run contract tests, render and decode a 3-second **synthetic test-tone** H.264/AAC artifact. It is NOT Japanese speech and NOT the full 23.843-second review MP4. This deliberate limitation avoids committing unapproved inherited voice/video.

**Reference:** User-provided 16-panel AI/Excel storyboard and AI JITAN quality brief: image-first scenes, short hook, safe area, subtle camera motion, one message, manual posting. Original v33 MP4 and full TikTok市場分析/TikTok動画研究 chat transcripts were not available. No claim of reference parity.

**Not approved:** source rights, Japanese narration transcription/naturalness, semantic subtitle alignment, mobile-device playback, employee approval, ten-genre full renders. No merge, purchase, upload to TikTok or automated posting. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Stacked on unmerged PR #71.
