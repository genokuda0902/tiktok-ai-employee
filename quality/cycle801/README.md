# cycle801 — Image-first editorial layout (DRAFT)

**Change vs cycle800:** remove repeated headline/diagram/subtitle blocks and recompose all eight scenes as one headline + large image/diagram + one high-contrast subtitle band. For the Raspberry Pi review example, six cramped inherited diagrams were redrawn as original crisp vectors; the two opening photographs remain inherited REVIEW_ONLY material. All 16 subtitle cue intervals and the inherited Japanese AAC stream are preserved.

## What is in GitHub

- `layout_contract.py`: 1080×1920, 30fps, 10 genre palettes, 8 scene indices, image/subtitle safe areas, cue validation.
- `test_layout_contract.py`: 8 unit tests.
- `.github/workflows/cycle801-layout.yml`: test + 429-frame synthetic MP4 CI artifact. **Its audio is an electronic test tone, NOT Japanese speech.**
- **Full local renderer and completed Japanese-audio review MP4 are delivered separately in the cycle801 ZIP. They are NOT synchronized into this PR.**

## Local factual QA

- 429 frames, H.264 30fps, 1080×1920, AAC 48kHz, 14.314s.
- PCM audio MD5 equals cycle800: `ae8b4acbae75bb37942533655d01413a`.
- 13/13 local technical checks and 10/10 local unit tests pass.
- New free Japanese TTS was attempted via gTTS, but network access failed; no new narration was generated.
- The reference-video quality comparison, native-speaker review, actual phone playback, source rights and employee sign-off are **not verified**.
- No paid services, posting, auto-merge or approval.

**Status:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
