# Cycle1158 — Writer reading-order focus (review only)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Independent reimplementation, not original v33 source.

## Source and change
- Builds on unmerged cycle1156 PR #557. Source private MP4 SHA256: `855509adc699189b8b5b7391b2b323a5624e9eedec94ac33ab7f092f7a016f91`.
- Window 17.65–20.15 seconds: transparent three-stage highlight of **目的 → 条件 → 形式** in the existing Writer screenshot, 75 overlay frames. Does not rewrite the Japanese narration or subtitles. First local attempt 17.10–19.60 overlapped the prior Excel-to-Writer transition and was discarded; timing was corrected.
- Renderer supports ten color palettes, but each new genre/layout requires manually checked `layout_id` and approved source media. Only the AI work sample was rendered.
- The source screenshot and audio are inherited, rights and public distribution **unverified**. No real user data or new third-party images were added.

## Reproduction (private media only)
```bash
python quality/cycle1158/reading_focus.py --source /private/cycle1156.mp4 --output /private/cycle1158.mp4 --manifest /private/review_manifest.json --workdir /private/tmp
PYTHONPATH=quality/cycle1158 python -m unittest discover -s quality/cycle1158/tests -p 'test_*.py' -v
PYTHONPATH=quality/cycle1158 python quality/cycle1158/tests/ci_smoke.py
python quality/cycle1158/audio_chapter_audit.py /private/cycle1158.mp4
```
Private manifest: `{"policy":"HUMAN_REVIEW/PUBLICATION_NOT_APPROVED","asset_approval":"review_only_no_publication","manual_post_only":true,"source_sha256":"855509adc699189b8b5b7391b2b323a5624e9eedec94ac33ab7f092f7a016f91","genre":"ai","layout_id":"writer_three_rows_v1","window":[17.65,20.15]}`.

## Local QA
- New review MP4 SHA256: `b0b508b13d812130d2b088d8d0aff54e91db2edee9d3700e6f3ccb97a38996b7`.
- H264 1080×1920 30fps, 691 frames / 23.033s, AAC 48kHz, full A/V decode PASS.
- Original and new AAC elementary ADTS SHA256 both `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`.
- Mean changed focus-region pixels: 5.448/255 in window, 1.147/255 outside (re-encode noise). Caption y1490–1840 max per-frame mean difference 0.716/255.
- Local 10 unit tests PASS, synthetic 5s/150-frame A/V smoke PASS, all eight chapters have nonzero audio signal by RMS. **RMS does not verify Japanese transcription, pronunciation or subtitle semantic alignment.**
- User's 16-panel/~36s reference storyboard was inspected; full original research chats and original v33 MP4 remain unavailable. Current video has 8 scenes/23s and does not match reference cinematic human/robot scenes or scene variety.

## Gates
No independent Japanese ASR, rights approval, phone playback, employee approval or actual GitHub billing verification. CI uses **synthetic** A/V, not private real MP4. Do not merge, upload private media to public GitHub, auto-post, or pay for services.
