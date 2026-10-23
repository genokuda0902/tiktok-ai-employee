# cycle790 — opaque transition wipe (review only)

Previous cycle789: 23.843s / 1080×1920 / H.264 + inherited AAC, photo-panel Ken Burns motion; Draft PR #73 and successful synthetic CI (run 39936184619). **New defect found:** around 13.73–14.20s, three scene transitions briefly double-expose Japanese headlines, tables and numbers. This interval was not repaired in cycle785 (which covered 10.8 and 17s).

This cycle replaces frames **411–428 (13.70–14.27s)** with a configurable *opaque* left-to-right wipe between clean frames at 13.60s and 14.36s. Unlike alpha crossfades, opaque wipes never blend letters from two scenes. This deliberately removes unreadable <0.2s flash scenes. The same transition contract can be used across 10 genres, but only the AI productivity full video was tested.

Full local command (requires the **unapproved local** cycle789 MP4):

```sh
python quality/cycle790/repair_wipe.py --input cycle789.mp4 --output cycle790.mp4 --config quality/cycle790/config.json --report cycle790_report.json
python -m unittest discover -s quality/cycle790 -p 'test_*.py' -v
```

Local verified: 23.843s, 714 frames, 1080×1920 30fps H.264/AAC, source AAC packets and decoded PCM identical, full decode PASS, 7/7 unit tests PASS. Visual changes concentrated at 13.7–14.3s. Complete review-only MP4 and QA comparison supplied in conversation sandbox, **not committed to GitHub** (source rights/employee approval unverified).

CI on GitHub creates only a separate **3-second synthetic-tone fixture**. It does NOT reproduce the complete Japanese video and is NOT publication-ready. Japanese narration transcription/naturalness and semantic subtitle synchronization, reference v33 original, smartphone playback, source rights and employee approval remain unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No auto-posting, merge or paid services. Stacked on PR #73.
