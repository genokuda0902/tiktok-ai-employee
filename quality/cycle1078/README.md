# cycle1078 — genuine LibreOffice Calc operation recording (REVIEW ONLY)

Scene 03 (5.800–8.533 seconds) replaces a **static, clipped Calc screenshot** with a 2.733-second **actual Xvfb/x11grab screen recording of LibreOffice Calc**. The real operation selects SUM cells B5 and C5, then enters =B5+C5 to show 75 from fictional example data (46 + 29). It is **not** AI operating Calc or a real customer's business result. No PII; locally generated sample data only. Visible label: LIVE CALC RECORDING / FICTIONAL DATA.

Different from cycle1076's Writer gutter checks. The other seven scenes, all eight burned-in Japanese subtitle intervals, and inherited Japanese AAC narration are preserved in content (video re-encoded). This code provides 10 genre accents; only ai_work has been rendered as a complete private MP4. No private video/capture is committed.

Local command (input hashes required, fail closed):

```bash
python -m quality.cycle1078.real_calc_capture \
  --source /private/cycle1076.mp4 --source-sha EXACT_SHA256 \
  --capture /private/calc_live_recording.mp4 --capture-sha EXACT_SHA256 \
  --out /private/cycle1078.mp4 --genre ai_work
```

CI uses only a synthetic 9-second 1080×1920 video and 1440×900 simulated capture to test the compositing mechanics, not the real 23-second MP4. Local 12 tests and synthetic smoke passed. Real video decoded fully and inherited AAC ADTS stream was byte-identical. Protected subtitle region max mean pixel difference 0.4667/255 across 691 frames.

**Publication remains prohibited**: no independent Japanese ASR or semantic subtitle match, no smartphone playback, no publication rights/employee approval, and actual Actions billing unverified. No merge, no auto-post, no paid service.
