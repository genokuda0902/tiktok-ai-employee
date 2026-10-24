# cycle828 — recommendation to action (REVIEW ONLY)

## Verified improvement
Starting from the cycle827 Japanese AI-work review video, replace **16.150–19.383 seconds (97 frames)**: instead of a static before/after correction card, a fictional laptop shows an AI recommendation, then a pointer and three checkmarks progressively convert it into work actions, followed by a readiness confirmation. No real service UI, customer data, performance claim, private assets, or externally licensed image is used. This is a deterministic PIL compositor with ten genre palettes. Only the AI-work genre's full MP4 was rendered.

## Reproduce locally
```bash
python -m unittest discover -s quality/cycle828 -p 'test_*.py' -v
python quality/cycle828/apply828.py --source cycle827_AI_WORK_SOURCE_PROOF_JAPANESE_REVIEW_ONLY.mp4 --output cycle828_AI_WORK_APPLY_ACTIONS_JAPANESE_REVIEW_ONLY.mp4 --genre ai_work --report qa828.json
ffmpeg -v error -xerror -i cycle828_AI_WORK_APPLY_ACTIONS_JAPANESE_REVIEW_ONLY.mp4 -f null -
```

CI regenerates the entire 8-scene source with original fictional assets, offline Open JTalk narration, and the same 24 Japanese caption states. It runs cycle827 tests and cycle828 tests, checks script-to-subtitle parity, produces a complete 1080×1920 H.264/AAC MP4 and uploads a **7-day review-only artifact**. The source video itself is not committed. The overlay code is identical between local and CI, but upstream video bytes can differ.

## Sources and non-approval
Consulted prior `TikTok市場分析` and `TikTok動画研究` summaries; complete task/chat text unavailable. User's 16-panel AI時短ラボ storyboard located in Library and consulted. Original v33 MP4 and original generation code unavailable; direct visual comparison not performed. Main at inspection: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`. Base is unmerged Draft PR #145, parallel #146 not merged.

Technical checks cover full AV decode, frame count, audio bitstream identity, 10 palettes, and animation phase difference. **Not** independently verified: audible Japanese speech semantics, naturalness, word-level caption sync, smartphone playback, reference equivalence, rights for public release, or employee approval. Do not publish or merge. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No payment or automatic posting.

## Next cycle
Prioritize independent Japanese audio-content and caption-timing inspection, then cinematic image-first visuals with confirmed release-safe assets and smartphone playback. Preserve evidence and avoid reworking the same static scenes.
