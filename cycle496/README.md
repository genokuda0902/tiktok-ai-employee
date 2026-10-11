# Cycle496 — review only (zero additional cost)
**Topic:** Convert vague work requests into purpose / deadline / deliverable.
**Difference from cycle495:** original cream editorial BEFORE→AFTER graphics, three-step brief cards, high-contrast 12-beat captions; matches all 10 genres from the existing user pilot.
**Preview:** locally generated 1080×1920, H.264/AAC, 19.2 seconds, 576 frames. The local full renderer and original PNGs are in the separately supplied cycle496 ZIP; this branch stores the reusable scene data and approval tests.
**BLOCKER:** no native Japanese TTS on the local runner. gTTS network request fails DNS; Kokoro and Open JTalk voice packages are unavailable. MP4 is an SFX-only preview; it is NOT ready to post. No voice/caption alignment or human listening QA has passed.
Run contract tests: `cd cycle496 && python -m unittest -v test_scene_config.py`.
Next recovery: run existing workflow_dispatch Kokoro test with authorized GitHub Actions runner; review WAV pronunciation, then re-time subtitles and render a new MP4. Do not treat TTS presence as voice approval.
**Release:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No automatic posting, no merge, no paid service, no personal data.
