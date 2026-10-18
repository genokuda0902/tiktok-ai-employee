# Cycle 666 — Illustrated hook (draft / not approved)

Compared with cycle665, the first 2.1 seconds were redesigned into an original 1080x1920 high-contrast illustrated mini-computer vs monitor question hook. The source video, 8 scene assets, inherited Japanese AAC, full MP4 renderer, QA, and reproduction test are delivered separately as a ZIP in the ChatGPT run. This branch stores a small genre-neutral contract and unit tests, **not** the complete renderer or media.

- Ten genres configured; science is the only rendered/tested genre.
- New Japanese TTS: not generated. Existing workflow `.github/workflows/raspberry-pi5-voice.yml` is manual-dispatch only.
- Audio: inherited AAC; mean -19.1 dBFS, peak -2.4 dBFS; actual speech-to-subtitle transcript match not verified.
- New opening visual pixel change: 45.55% of the central opening region differs >30 intensity levels from cycle665.
- 1080x1920 H.264/AAC, 30fps, 468 frames, 15.6 sec; full local decode PASS.
- Rights, mobile-device playback, reference parity and human approval: pending.
- No auto posting, paid services or merge. Human review before manual publication.

CI is not considered successful until an actual workflow result is verified.
