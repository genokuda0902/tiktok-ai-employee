# cycle802 — optical centering, scene-safe (REVIEW ONLY)

The cycle801 MP4 is 1080x1920 but its opening and end-card information group was left-heavy (approx x=60..770, center=415 vs canvas center=540). This cycle shifts **only** 0.0–3.2s and 20.8–23.85s 136px right (new centre approx 551). Intermediate scenes are intentionally untouched: they have UI near the right edge and shifting would crop it. This was caught during local preview and fixed before the final render.

The left extension repeats the first two source pixel columns instead of adding a hard black seam. Important content remains <=906px, leaving >=174px for right-side TikTok UI. No aspect ratio stretch or new images, voices, captions, music or numbers. Same config validation for 10 genres; one AI-workflow video was rendered locally.

Local (do not commit inherited video): `python quality/cycle802/reframe.py --config quality/cycle802/config.json --source-video <LOCAL_REVIEW_MP4> --output <LOCAL_OUTPUT_MP4> --review-only`

CI creates only a 2-second synthetic video and sine tone, **not** the 23.8-second Japanese narrated completed video. User media and audio rights are unverified, so NEVER upload to GitHub, merge, publish, auto-post or deliver to employees. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Japanese speech meaning/naturalness, semantic subtitle sync, v33 original comparison and mobile playback remain unverified. This is a reimplementation, not recovered v33 source. Budget: 0 JPY.

## Verified CI and review outputs

## 2026-10-24 cycle802 review-only checkpoint (unmerged)
- Stacked Draft PR #100: https://github.com/genokuda0902/tiktok-ai-employee/pull/100 (base is unmerged PR #97 branch). Main is unchanged.
- Implemented configurable scene-window optical centering: only 0–3.2s and 20.8–23.85s shift +136px; middle scenes stay unchanged to avoid right-edge UI clipping. 10-genre validation, fail-closed rights and publication checks.
- Implementation and CI fix commit: 8e8a8df516fda61ff8b9b449c1cc7fd6b5cf5a0e.
- 13 unit tests on GitHub PASS, push CI SUCCESS: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40037793350 ; PR CI SUCCESS: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40037799801 .
- CI artifact 12537518362 was downloaded and verified: 2.000s H.264/AAC 1080x1920, **synthetic 440Hz tone, NOT Japanese voice**. Real user media never uploaded.
- Local review-only Japanese-voice MP4: 23.848s, 714 frames 30fps, H.264/AAC 1080x1920; SHA256 ebd6bb1d1961d01b2253c6015700bff03ce2ed06cdc1d7fd07c9efa588b123fa. Inherited AAC packet hash matches cycle801. Full A/V decode PASS. Not committed or posted.
- Prior TikTok市場分析/TikTok動画研究 summaries and Library 16-panel storyboard inspected; full original task transcripts and v33 original MP4 unavailable for direct comparison. Japanese speech/subtitle semantic sync, phone playback, rights and employee approval remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
