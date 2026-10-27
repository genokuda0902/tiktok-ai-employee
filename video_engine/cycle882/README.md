# cycle882 — Chromium-rendered DOM proof (HUMAN REVIEW ONLY)

Distinct from cycle879's Pillow-simulated UI states and cycle881's source-proof QA: this cycle captures **13 genuine Chromium-rendered screenshots after actual DOM input/check/click actions** in a locally authored, in-memory HTML demo (no navigation, accounts, external requests, or real AI service). Scenes 4, 5, 7 are reconstructed into a frame-exact 691-frame video. **This is NOT continuous screen recording and NOT a real third-party AI app.**

## Reusable core and tests
- `browser_proof_core.py`: ten genre identifiers, safe screenshot placement above Japanese caption area, 22 frame-exact visual states across eight scenes, 13 local-browser states, fail-closed source checks.
- `test_browser_proof_core.py`: 13 test methods with ten genre subtests.
- Run `PYTHONPATH=video_engine/cycle882 python3 -m unittest discover -s video_engine/cycle882 -p 'test_*.py' -v`.
- CI tests only this stdlib core and verifies no private media is committed. CI does **not** render or verify the actual final MP4.
- **CI recovery:** first run failed because runner lacked `ffmpeg` (exit 127), though 13 unit tests passed. Removed the nonessential synthetic FFmpeg smoke step and replaced it with private-media exclusion check.

## Actual media and limitations
The ChatGPT review ZIP contains local HTML, Playwright capture script, actual 13 screenshot PNGs, renderer, Japanese caption ASS, inherited audio, final MP4, and QA report. Local technical QA: 1080x1920, 30fps, 691 frames, 23.033s, H264/AAC 48kHz, 24 Japanese caption events, all video/audio decode, 3 browser scene changes. Inherited audio bytes match cycle879; no independent pronunciation or speech-text alignment test.

An attempt to record continuous WebM using Playwright failed (missing compatible bundled FFmpeg and 0-byte output); direct file:// and localhost navigation were blocked by administrator. The successful route used `page.set_content`, actual DOM actions, screenshots, and FFmpeg reconstruction. Do not claim genuine continuous recording.

Original reference-video full playback comparison, inherited voice rights, employee review, smartphone playback, and TikTok performance remain unverified. No paid services, automatic posting, or merge. **PUBLICATION_NOT_APPROVED**.
