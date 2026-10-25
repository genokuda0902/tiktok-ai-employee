# cycle841 — image-region focus motion / review only (2026-10-25 JST)

## Actual outcome and prior difference
- Previous cycle840: 691 frames / 23.033s / 1080×1920, H.264/AAC 48kHz, seven retained dissolves and seven audio-pause trims.
- This cycle: applies **smooth 0→4.4%→0 image-only push-in** to three static image scenes (2, 6, 8). Existing real PC operations, title and burned Japanese caption regions are protected; no new footage is fabricated. The 10-genre config shares the same motion engine; only `ai_work` was rendered.
- Local private source SHA256 `2d54f2c419af9451969a3d448625fa2c750e5227ee8c3d17e9a7cc81e139ddf4`.
- Local review output SHA256 `2f29c252048b10123e36a3a86aaf621355dbbefbfe75c11f5c9837b8ea2b8942`.
- Output: 691 frames, 23.033s, H.264 1080×1920 30fps, AAC 48kHz. Full A/V decode PASS; decoded audio PCM MD5 equal before/after `813f69e5c926b70c927e46e27704e267`.
- Representative image-region MAE at 4.2/15.6/21.0s: 35.592/36.336/33.960; protected top+bottom MAE: 0.550/0.490/0.511. Unchanged scenes at 1.3/9.5s image MAE: 1.220/0.508.
- No new voice, speech transcript, or subtitle timing was independently validated. Do not confuse PCM equality with Japanese semantic correctness.

## Source, rights and references
- TikTok市場分析 and TikTok動画研究 full chats unavailable; previous accessible summaries prefer hook in 1.5s, actual demonstration, Before/After, readable subtitles, human approval.
- User's 16-frame ChatGPT×Excel storyboard inspected; original v33 MP4 unavailable in this runtime, so no direct parity claim.
- Main authoritative PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md inspected; original v33 source unrecovered. This is a reimplementation.
- Source is fictional review-only media from prior private ChatGPT run, not a publication-approved asset. NEVER upload it to GitHub. GitHub CI uses only synthetic test patterns.

## Reproduction (local authorized media only)
```
PYTHONPATH=. python3 cycle841/motion_review.py --source cycle840_REVIEW.mp4 --output cycle841_REVIEW.mp4 --manifest local_manifest.json --genre ai_work
PYTHONPATH=. python3 -m unittest discover -s cycle841 -p 'test_*.py' -v
bash cycle841/ci_synthetic.sh
```

## Open gates
- Verify Japanese narration semantics and subtitle timing independently; phone playback, source rights, employee approval and original v33 comparison remain unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, posting, paid services, external media uploads or employee delivery.
