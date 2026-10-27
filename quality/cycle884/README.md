# cycle884 — scene-only eased dissolves (review only)

- Improvement vs cycle883: seven hard scene cuts become six-frame (0.20s) smoothstep dissolves. Internal UI state changes remain sharp; Japanese ASS subtitles are composited after the transitions, so text does not ghost.
- 10 genres share the same frame-exact planning, source provenance gates, and reserved caption band. The total remains 691 frames at 30fps (23.033s).
- Local MP4: `cycle884_SCENE_EASE_DISSOLVE_JP_HUMAN_REVIEW.mp4` generated outside GitHub, using prior-cycle 22 locally authored 1080×1920 images, 42 blended frames, and inherited Japanese AAC narration.
- Technical QA (local): 22/22 checks; 16/16 core tests; 7 scene boundaries' peak per-frame jump decreased by 77.87% on average versus cycle883. Video/audio decode, 1080×1920, H.264/AAC, 24 captions, and packet-identical narration confirmed.
- This CI workflow tests core code only. It does NOT render or validate the MP4 in GitHub Actions.
- No public posting or merge. Narration reuse rights, Japanese pronunciation and semantic ASR alignment, original user reference video comparison, mobile device playback, and employee approval remain unverified.
- Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid service, no external media upload, no automatic TikTok posting.
