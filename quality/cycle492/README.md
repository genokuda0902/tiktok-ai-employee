# cycle492: Phrase-synced caption timing (review-only)
- Prior cycle491: 6 static scene-level captions, phonetic eSpeak speech proxy.
- cycle492: 12 individually timed Japanese subtitle states across 6 scenes, 12 separate speech clips, exact start/end boundary assertions.
- A new original AI verification theme: numbers, sources, context, human review. 1080x1920 / 30 fps / 19.2 s.
- Local artifact, full Pillow/OpenCV renderer, QA JSON and tests are in the cycle492 ZIP delivered in ChatGPT, NOT in this repository.
- This repository contains the reusable 10-genre phrase-timing module and its independent tests. Run: `python -m unittest quality.cycle492.test_phrase_timing -v`.
- Speech proxy is eSpeak Italian reading romaji, **NOT native/natural Japanese TTS**. Native voice, user-device playback, reference parity, human approval and publication are **NOT VERIFIED**.
- Rights: original synthetic graphics; no personal data. No payment, merge, external upload or TikTok posting.
- Next: approved runner Kokoro or Open JTalk native Japanese TTS; replace voice and verify phonetics and subtitle sync before review.
