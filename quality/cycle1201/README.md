# cycle1201 — scene-aware progress rail (HUMAN_REVIEW)

Previous cycle1199: feathered central-panel slow zoom. This cycle: a **different** improvement, an eight-step progress rail in the unused top safe area, synchronized with editorial scene starts (frames 42,96,171,252,333,414,501,579). Completed chapters turn teal, the current chapter white. The intro remains inactive. All 10 genre accent configurations use the same code; only AI-work-efficiency has been rendered and reviewed.

## Reproduce locally

```bash
python quality/cycle1201/code/chapter_progress.py previous.mp4 cycle1201.mp4 --genre ai --starts 42,96,171,252,333,414,501,579
python -m unittest discover -s quality/cycle1201/tests -p 'test_*.py' -v
python quality/cycle1201/tests/ci_smoke.py
```

No paid dependencies. Requires FFmpeg and Python 3.11. The existing 1080x1920, 30fps H.264/AAC source is **not committed**. AAC is copied byte-for-byte, and the burned-in Japanese captions are preserved apart from ordinary re-encoding differences.

## Actual 22.5-second review MP4 (local, not committed)

- Filename: cycle1201_CHAPTER_PROGRESS_HUMAN_REVIEW.mp4
- SHA256: 80fe16fcc61b2f975fea397eabaa08671f85926f32a0a1c966ed2a3acdebaf09
- 8,504,988 bytes, 675 frames, 1080x1920, 30fps, H.264/AAC 48kHz.
- Full video and audio decode: PASS.
- AAC ADTS SHA256: 76bcb9897c914d5ecebe97650cae6fc317b168fffcf19d2891ce4135627babfe, identical to previous.
- Protected image regions (outside rail): max mean absolute pixel difference 0.391/255 across 10 sampled frames.
- Unit tests: 10/10 PASS. Local 30-frame synthetic smoke: PASS.
- CI scope: synthetic 30-frame video and tests only, **not** the actual review MP4.

## Source/reference limitations

Prior TikTok market/video research summaries and reference storyboard notes were consulted: 1.5s hook, short purposeful cuts, concrete UI proof, Before/After, readable Japanese captions. Original v33 reference (previously reported 31.55s/512x910) and original 16-panel storyboard were not available for direct inspection this cycle. Independent Japanese speech-to-text and subtitle semantic/timing verification remain **NOT VERIFIED** (no offline ASR model available). Actual phone playback, commercial rights, employee approval and reference-quality parity remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, paid service, auto posting or upload of user media.
