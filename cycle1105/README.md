# cycle1105 — scene-safe dip + Japanese caption label (HUMAN REVIEW ONLY)

## Delta from cycle1103
- Replace the seven abrupt chapter cuts with a four-frame, **fade-through-dark** of the upper UI (relative frames -2/-1/0/+1 with brightness 0.72/0.30/0.30/0.72). The subtitle and learning-rail safe areas are never faded.
- Replace the English production/debug caption header with Japanese **今日のポイント** in all eight scenes.
- Do **not** use a cross-dissolve between different screenshots: the first local trial visibly doubled text/UI and was rejected.
- Ten configurable genre accent colors; only the AI-work video has been rendered and verified.

## Local actual-MP4 verification (not in GitHub)
- Source: cycle1103 22.5 s 1080x1920 30fps, 675 frames, 8 chapters.
- Output: cycle1105 22.5 s 1080x1920 30fps, 675 frames, H.264, original AAC 48kHz audio stream-copied.
- Mean immediate chapter-cut pixel-change reduction: 71.32% over seven cuts; this is a transition smoothness proxy, **not** proof of higher watch time.
- Full audio/video decode PASS, original/output ADTS audio payload SHA-256 identical; lower learning rail sampled max MAE 1.277/255.
- Local tests 9/9 PASS. Synthetic GitHub CI is **not** the actual 22.5-second video.
- Actual output SHA-256: 0441c69da1a0edf299b305c822c15515d5ffcb2894a5b5eb9a66c8dfe9be0926 (superseded by verified final output if updated).

## Reproduction
`python cycle1105/scene_safe_dip.py --source <private_source.mp4> --dest <private_output.mp4> --expected-sha <source_sha256> --genre ai_work`

Private MP4, reference stills, source media and voice are **never** uploaded to this public repository. Code and synthetic test only.

## Unverified
Independent Japanese speech transcription, subtitle semantic/timing match, original reference v33 parity, rights to all inherited media, real-phone playback, employee approval and actual Actions billing. No publishing, merging, paid contracts or auto-posting.
