# Cycle1169 — First-second hook underline (human review)

**Previous cycle1167:** Scene-elapsed-time rail across eight scenes. **This cycle:** A new 1.4-second animated amber underline directly below the opening question. It draws in, holds briefly and fades without covering title or narration. This is a distinct intro-hook improvement, not a repeat of scene progress.

- Reusable effect: `code/hook_underline.py` — 10 genre palettes, portrait safe-strip validation, 42 transparent frames, H.264 video render and AAC bitstream copy.
- Unit tests: `tests/test_hook_underline.py` — 23 local tests passed.
- GitHub Actions: `.github/workflows/quality-cycle1169.yml` — synthetic-only 22.5-second A/V generation, full decode, resolution and exact AAC copy.
- Local actual MP4: 22.5 s, 1080×1920, 30 fps, H.264/AAC 48kHz, 675 frames; local full decode and exact audio bitstream verification passed. Actual MP4 and QA stay in conversation files, not public GitHub.
- Actual source and output audio AAC ADTS SHA-256: `8f67ed7ae02482d581c375401329004c9e06c6cc282fa03d34c93ec6f200c928`.
- Frame 28 hook ROI mean pixel difference 19.838/255; subtitles remain within 2/255 of re-encoding noise on sampled frames; effect absent after scene 1.
- **Not verified:** independent Japanese ASR and word-level subtitle sync, reference v33 parity, rights, mobile real-device playback, retention impact, employee approval and GitHub Actions billing.
- No private source uploaded, no paid contract, no merge and no automatic posting. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
