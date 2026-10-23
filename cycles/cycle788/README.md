# Cycle788 — clean slide rebuild (HUMAN_REVIEW)

**Previous:** cycle787 applied shadow/detail enhancement to inherited visuals, which still had duplicated text/ghosted panels.

**New:** all 8 science/technology scenes were rebuilt locally as original vector illustrations; Japanese subtitles are composited only once using 16 timed ASS cues. Japanese AAC narration from cycle787 was copied without re-encoding. Video output: H.264 1080×1920, 30 fps, 429 frames, ~14.314 s container duration. No third-party images or paid APIs used.

This branch includes the actual scene/cue/genre contract, tests, and CI. The full local Pillow+FFmpeg rendering implementation, input video, slide PNGs, QA report and finished MP4 are packaged in the conversation ZIP (not uploaded to GitHub because the connector only accepts UTF-8 text files and this run does not publish inherited media). **CI checks the scene contract, not the MP4.** Do not claim this branch alone can reproduce the full video.

Run CI tests: `python -m unittest discover -s cycles/cycle788/tests -v`.

Ten genre presets exist; only one science video was produced. Human voice naturalness, smartphone playback, rights for inherited narration, reference-video parity and employee approval are not verified. No merge, paid subscription or auto-posting. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
