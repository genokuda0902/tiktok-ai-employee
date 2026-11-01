# cycle1114 — scene-header chapter-number consistency repair

**Observed defect:** In cycle1112 at 4.5 seconds, the second scene's top-left header reads `STEP 01 / 08`, but its lower narration-caption counter reads `02 / 08`. The source video was visually inspected, not OCR-guessed. This cycle changes only the incorrect top-left two-digit `01` to `02` for 2.9–5.8 seconds. It does not claim to verify every header in all eight scenes.

Unlike cycle1112's row verification cut, this fixes a misleading on-screen chapter number. A small RGBA patch (x182–230, y99–139) preserves the other text, picture and lower subtitles. Ten genre palette choices share one strict renderer; only the AI-work private MP4 was produced.

Local reproduction:

```sh
python -m unittest discover -s quality/cycle1114 -p 'test_*.py' -v
python quality/cycle1114/chapter_number_fix.py --source /private/cycle1112_ROW_VERIFICATION_CUT_JP_REVIEW_ONLY.mp4 --source-sha aff73f105774cb6fbfad6ccc8b656e3626365d144c0feffc044002767dd31b1c --out /private/cycle1114_CHAPTER_HEADER_FIX_JP_REVIEW_ONLY.mp4 --report /private/report.json
```

Local result: 1080x1920, H264 30fps, 691 frames, 23.033333s, AAC 48kHz, full decode PASS; AAC elementary bitstream unchanged; 5/5 tests PASS; all-frame caption-region mean pixel delta <=0.2672/255, outside time interval <=0.2459/255 (re-encode noise). Output SHA256 b5bd9843ef0306ce5df291bfbba242267462985616e00f64d33933947f70549d. This is not a perceptual quality score.

Python3 + Pillow + FFmpeg/ffprobe + DejaVu Sans font. GitHub CI tests **synthetic** one-second media, not the private completed MP4. Do not commit source MP4, audio, confidential materials or reference video. Inherited rights, independent Japanese ASR, speech-caption semantic timing, phone playback and employee approval remain unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, posting, paid service or confidential-media upload.
