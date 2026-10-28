# cycle942 — caption-safe 3-shot cinematic CTA (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** New, distinct from cycle941's template reuse scene: replace final 82 frames (609–690, 20.3–23.033 s) with three visually distinct CTA beats: choose one action → check results manually → save for later. Retain the original burned Japanese subtitles in y=1400..1920 and the original AAC audio. A persistent unapproved/manual-posting warning remains in the upper visual area. The “save” wording is illustrative, not an implemented button or an action.

## Private reproducibility
The source is the PRIVATE cycle941 review MP4 with SHA256 `57c493d748d9930834101343b0c5a28f1ed75b6b8412df77854fe311012474d7`. This source and the new MP4 must NOT be committed to public GitHub. Local build with FFmpeg, Pillow, numpy, free Noto CJK fonts:

```bash
python cycle942/src/closing_cta.py --source /private/cycle941_REUSE_STORY_JP_REVIEW_ONLY.mp4 --output /private/cycle942_CINEMATIC_CTA_JP_REVIEW_ONLY.mp4 --tmp /private/cycle942_tmp --genre ai_work --expected-source-sha 57c493d748d9930834101343b0c5a28f1ed75b6b8412df77854fe311012474d7
python -m pytest -q cycle942/tests/test_closing_cta.py
```

10 genre-specific examples configured; only ai_work has a full MP4 rendered. The full source assets are not approved for publication. This is a reimplementation, not recovered original v33. No merge, auto-post, private media upload, paid API or release.

Research: accessible summaries of 「TikTok市場分析」「TikTok動画研究」 and user-supplied 16-panel storyboard were reviewed. Original v33 MP4 and complete original research chats were not available in this run. Reference has cinematic people/robot, 16 scenes, ChatGPT/Excel demo, bold typography and a final CTA. Current output still uses 8 mainly synthetic scenes and is not reference-equivalent.

Unverified: independent Japanese ASR, semantic narration-caption alignment, mobile device playback, source rights, employee approval, GitHub Actions actual billing. CI checks code and synthetic images, NOT private finished MP4.
