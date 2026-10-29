# cycle963 — original, synchronized UI cues (PRIVATE REVIEW ONLY)

Independent reimplementation, **not original v33**. This change adds five quiet original sound cues to an existing 23-second Japanese-narrated review MP4, at evidence/step/action beats. No third-party sound files or new visuals. 10 separate genre cue policies, only `ai_work` review-enabled; the other 9 fail closed. The existing H.264 elementary stream and burned Japanese subtitles are preserved exactly.

## Local private rendering

```
python -m pip install numpy pytest
python cycle963/sound_cue_engine.py --source /private/cycle961_MOBILE_PROOF_REVEAL_JP_REVIEW_ONLY.mp4 --output /private/cycle963_ORIGINAL_SYNC_CUES_JP_REVIEW_ONLY.mp4 --qa /private/render_qa963.json
python cycle963/verify_output.py --source /private/cycle961_MOBILE_PROOF_REVEAL_JP_REVIEW_ONLY.mp4 --output /private/cycle963_ORIGINAL_SYNC_CUES_JP_REVIEW_ONLY.mp4 --qa /private/qa963_full.json
python -m pytest -q cycle963/test_sound_cue_engine.py
```

Source SHA256 must be `4257fccc11a1e8880eb208a5a50f53a9fb815c35f53069048409da021084344d`. Requires local `ffmpeg`, `ffprobe`, `numpy`. Original sounds are computed from math, with per-cue peak <= -23 dBFS; no commercial sample libraries. CI tests code/synthetic sound only; **private full MP4 is not uploaded to GitHub**.

Japanese voice remains present, but independent Japanese speech recognition and semantic/time match to captions are not verified. Employee approval, original media rights, phone playback, public release are not verified. No automated TikTok posting.
