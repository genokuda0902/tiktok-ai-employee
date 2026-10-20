# Cycle721 QA (2026-10-20 JST)

- Base: cycle720 Japanese-narrated image-first render.
- New local output: cycle721_NATIVE_CINEMATIC_NARRATED_REVIEW_ONLY.mp4 (27.343s, 1080x1920, H264/AAC, 819 frames).
- MP4 SHA256: 05b773bb3e24296e01420f1f96bd12f836434eb0a7807e074cae14ecf0155b94
- Visual change: native 1080x1920 scene cards rather than cycle720's 540x960 upscaled source; new self-drawn robot, gradient and safe caption panel.
- Eight local tests passed; ffmpeg full decode succeeded.
- Japanese narration is **reused** from cycle720. Decoded audio SHA256 matches the previous MP4; no fresh TTS generated.
- Subtitle timing is scene-level, not word-level. Phone playback, pronunciation, license and human approval remain unverified.
- Full local renderer, tests, MP4 and QA images are attached to the ChatGPT run, **not** committed to GitHub. Code/test writes were blocked by the GitHub connector safety checks.
- CI not run for cycle721. No PR created, no merge, no publication.
- Research task settings checked, but historical findings inaccessible. Reference storyboard consulted; v33 original MP4 inaccessible this run.
- Publication status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
