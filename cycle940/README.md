# cycle940 — legible finished-example focus (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, auto-post, paid API or public private-media upload.

## Actual distinct change
Compared with local cycle938 private review MP4, scene03 (frames 174–260, 5.8–8.7 s) replaces a small static sample report with a native-resolution 3-step finished-example demonstration: (1) finished layout; (2) required column labels; (3) human verification. Soft background bloom and sequential focus emphasize the result without moving Japanese glyphs. This is a **fictional illustration**, not recorded Excel or ChatGPT.

Parallel PR #328 cycle939 changes scene02 from a different source branch; it is not merged or assumed integrated. This PR is stacked on Draft PR #327, not main.

## Verified local private media
- Input: cycle938_EVIDENCE_THREE_BEATS_REVIEW_ONLY.mp4, SHA256 189d3869b1326c8743e0cd7c5904da2e217b2c4d8db8a0b0e283de12e5d17a29
- Output: cycle940_FINISHED_EXAMPLE_FOCUS_REVIEW_ONLY.mp4, SHA256 4169c540bb354992a19705fb60fe4cb6da14fc4f857cb8c7d976b9667161c4de
- H.264 1080×1920, 30 fps, 691 frames / 23.033s; AAC 48 kHz stereo. Full video/audio decode PASS.
- AAC ADTS SHA256 preserved exactly: 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9.
- Edited frames: 87/87; 1/8 downsampled MAE min 42.299, mean 44.364. Outside edited frames max 0.260; subtitle area max 0.410 (reencode noise).
- 13/13 local pytest tests PASS. GitHub CI tests only code/synthetic images, **not** private actual MP4.
- 10 genre configurations tested; only AI-work was rendered as full MP4.
- Private review MP4 shared via ChatGPT, not GitHub.

## Reproduce with authorized private source
Requires Python 3, Pillow, FFmpeg and free Noto Sans CJK fonts.

    python cycle940/src/finished_example_focus.py --source /private/cycle938_EVIDENCE_THREE_BEATS_REVIEW_ONLY.mp4 --output /private/cycle940_FINISHED_EXAMPLE_FOCUS_REVIEW_ONLY.mp4 --tmp /private/cycle940_tmp --genre ai_work --expected-source-sha 189d3869b1326c8743e0cd7c5904da2e217b2c4d8db8a0b0e283de12e5d17a29
    python -m pytest -q cycle940/tests/test_finished_example_focus.py

## Research and remaining gates
Accessible summaries of TikTok市場分析/TikTok動画研究 and user's 16-panel ChatGPT×Excel storyboard consulted. Original v33 reference MP4 and complete original research chats unavailable; no claim of reference-equivalent cinematic quality. Independent Japanese ASR/meaning/word sync, commercial rights, smartphone playback, employee approval and actual GitHub Actions billing NOT VERIFIED. Employee approval and manual posting only.
