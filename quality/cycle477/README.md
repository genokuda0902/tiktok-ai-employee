# Cycle 477 — review-only quality experiment (2026-10-11 JST)

Original synthetic 18-second MP4 with six scenes and 36 half-second visual states. The result was checked with ffprobe (1080x1920, H.264, AAC, 30 fps, 540 frames), full FFmpeg decode, and 12 local unit tests.

MP4 SHA-256: `9f57fc5085f99eb73343d5708d2b34bde937a93b0877c1f7d5d1e0e4e1b7d1bc`.

**BLOCKED:** No Japanese narration was generated; AAC carries nonverbal sound effects only. Japanese SRT captions are script-timed, not synchronized to measured speech. Human quality approval is missing. Publication remains NOT_APPROVED.

The full renderer, tests and review MP4 are retained in the ChatGPT cycle477 source/QA ZIP, not this branch. Executable code and test writes were rejected by connector safety checks. No CI workflow ran; draft PR creation was rejected. Do not merge or publish.

Next: restore free Japanese narration and measured speech timing; restore reproducible source and CI in GitHub.
