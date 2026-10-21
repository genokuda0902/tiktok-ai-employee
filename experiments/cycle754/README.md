# cycle754 — scene cut motion smoothing (review only)

- Baseline: cycle753 local MP4; prior GitHub branch: `quality/cycle753-prompt-focus-20261022`.
- Change: five abrupt hard cuts at 3.2/6.5/9.8/12.8/24.3s become 0.20s left-slide transitions with frozen edge frames. Duration stays 27.343s, video 819 frames at 1080x1920/30fps, original AAC audio stream copied bit-for-bit, inherited burned-in Japanese captions preserved outside transitions.
- Reusable for 10 genre names, with configurable cut positions/transition/total timeline. No assets or original voice are uploaded to GitHub.
- Source media rights, narration pronunciation, caption-semantic alignment, smartphone playback and employee approval remain UNVERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- Run local: `python3 experiments/cycle754/src/smooth_scene_cuts.py --source /path/to/approved_baseline.mp4 --output /tmp/cycle754.mp4 --genre ai_work`.
- Run isolated CI tests: `python3 -m pytest -q experiments/cycle754/tests`. The synthetic E2E test uses ffmpeg-generated color and sine audio; it does NOT access user video.
- Baseline jump vs cycle754 at cuts, mean absolute RGB difference (270x480 proxy): 3.2s 58.582→38.041, 6.5s 36.476→28.476, 9.8s 57.978→30.624, 12.8s 44.529→35.797, 24.3s 64.758→28.608. This measures cut-frame discontinuity, NOT audience retention.
- The actual MP4 and reproducible local ZIP are delivered in the ChatGPT conversation, not in GitHub.
- No auto posting, merge, external asset downloads or paid service. This is a reimplementation, not recovered v33 source.
