# TikTok AI社員システム — authoritative handoff
Updated: 2026-09-18 JST. This document is an index, NOT proof of end-to-end completion. At the start of each chat, read this file and `recovery/v33/RECOVERY_STATUS.md`, then verify actual code and artifacts. Update this file with verified commit SHAs and test results whenever changing implementation.

## Binding decisions (latest wins)
- Preserve v33 quality; do not substitute v20, v19, or a simplistic slideshow and call it v33.
- **Image-first**: high-quality, approved/public-safe images with zoom/pan/cuts, optionally simple approved video (sanitized Excel operations, work scenes), new Japanese narration, synchronized readable captions. Natural animated robot / ComfyUI / Wan 2.2 **cancelled / out of scope**. Earlier Wan instructions are obsolete.
- Initial 6 employees, scale to 100 after verification. Google Forms registration/approval -> employee-specific planning/script/media/audio/render -> real QA -> Drive original -> LINE WORKS private notice -> employee review/revision -> employee manually posts to TikTok -> metrics collection. No automatic TikTok posting.
- Never use private or confidential images without explicit publication approval. Never publish, distribute, upload, or commit confidential images/video/audio, secrets, or the unsafe prototype. Do not buy GPU or enable production delivery without approval.
- Never claim quality equivalence, virality, QA completion, or deployment from merely generating a technically valid MP4.

## Verified source artifact and security
- Original `AI_Jitan_v33_REAL_SPREADSHEET(1).mp4` exists in session sandbox; SHA256 `b190414f6e3e191cea184d80e28ca7a3404d37a3f212eb94964f95b7674ea712`, duration 31.553333 s. It is NOT stored in this repository. Original v33 generation code and prompts have NOT been found.
- Session-created `v33_engine/render.py` is an unapproved simplistic prototype, **not original v33 source**, and its demo used confidential `IMG_5805.png`–`IMG_5812.png`, `IMG_5814.png`. Demo is DO NOT PUBLISH. Neither these images nor demo have been committed.
- Recovery checkpoint committed at `recovery/v33/RECOVERY_STATUS.md`, commit `4af9a936f5878d57558db839cbd814ff58c11215`.

## Repo state previously checked
- `main` workflow `.github/workflows/ai_jitan_complete_video.yml`: v19 reference studio, not proof of v33 reproduction.
- `main` `.github/workflows/daily-v2.yml` runs `src/build_daily.py`; not verified as v33, historically silent `-an` output.
- PR #5 `feature/employee-qa-real-metrics`: draft/open/unmerged on 2026-09-18; do not merge as proof of quality.
- v20 isolated run `35241003875` is v20 evidence only.
- Forms/GAS authorization and deployment, Drive and LINE WORKS production connectivity, and end-to-end 6-person run are not verified.

## Next concrete actions
1. Search original v33 source code, prompts and scene plan; save found originals with provenance and commit. If missing, explicitly label subsequent work a reimplementation.
2. Implement approval-allowlisted assets (fail closed), new-topic image-first generation with original narration and Japanese timed subtitles; commit source and reproducible manifest, dependencies, QA tests and exact command.
3. Validate new-topic video visually and for privacy, sound, caption alignment, pacing, and quality against v33. User quality approval is not yet obtained.
4. Then connect employee workflows and test all six. Update this handoff with immutable SHA, artifacts and measured test outcomes. Never ask user to rerun v20.

Repo: https://github.com/genokuda0902/tiktok-ai-employee
Checkpoint: https://github.com/genokuda0902/tiktok-ai-employee/blob/main/recovery/v33/RECOVERY_STATUS.md
PR #5: https://github.com/genokuda0902/tiktok-ai-employee/pull/5


## cycle818 checkpoint — 2026-10-24 JST (review only)
- Draft PR #129: https://github.com/genokuda0902/tiktok-ai-employee/pull/129 (head quality/cycle818-japanese-editorial-20261024, base parallel unmerged PR #128). main still 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- New 10-genre Japanese editorial overlay localizes eight scene headings and English review/debug footer; it does not change main narration, primary scene content or inherited AAC bitstream.
- Local 8/8 tests PASS; private review MP4 1080x1920/30fps/718 frames/23.933s, full decode PASS, AAC packet MD5 unchanged, SHA256 e74d3ebac022725f5709603aa1a3392160e00f7994cacb8be1016831ae0681a5. CI uses synthetic tone only. Exact details: quality/cycle818/CYCLE818_DELTA.md.
- Full TikTok市場分析/TikTok動画研究 transcripts and v33 original MP4 inaccessible in this run. 16-panel user storyboard found. No cinematic quality equivalence or publication approval.
- Priority: independently verify Japanese narration/semantic caption sync, approved source stills for clean-source renderer, rights, phone playback and reference comparison. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, charge or auto-post.


## cycle819 checkpoint — 2026-10-25 JST (REVIEW ONLY)
- Stacked Draft PR #132: https://github.com/genokuda0902/tiktok-ai-employee/pull/132 (base unmerged PR #129; parallel PR #130 unmerged). main remains 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Replaces only 18–21s (90 frames) of cycle818 private review video: original procedural desk/paper chart, 1.5% push-in, ten-genre colors. No reference/stock assets or personal data included. Local 9/9 tests PASS; 23.933s H.264/AAC 1080×1920 full decode PASS, AAC MD5 unchanged (8d0baabf50866471846346e7159046e2). Local SHA256 f77c61ec3b31be160084f0546f27fa4934b66b84efdaad85ecd919a0f229cfb0.
- Synthetic CI generates a tone, not Japanese speech; its status/artifact must be checked at latest PR head before claiming success. Private MP4 and inherited voice are NOT committed.
- User storyboard inspected; research full transcripts and v33 original MP4 inaccessible. Voice/caption semantic verification, inherited rights, smartphone playback, and employee approval still pending. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Next: semantic audio/subtitle verification and approved image-first footage, not further flat chart animation.


## cycle820 checkpoint — 2026-10-25 JST (REVIEW ONLY)
- Stacked Draft PR #134: https://github.com/genokuda0902/tiktok-ai-employee/pull/134 (base unmerged PR #132; no main merge). main at check 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Original animated completed action-plan card replaces only 15–18s (90 frames) of cycle819 private review MP4. Clear 担当 / 行動 / 期限, deadline 今日の稼働終了まで. Ten genre colors and fail-closed missing-field tests.
- Local 11 tests PASS; 23.933333s 1080x1920/30fps H.264/AAC; full A/V decode PASS; inherited AAC bitstream MD5 identical 8d0baabf50866471846346e7159046e2; local MP4 SHA256 9208ae3689d9c10d1f2f95f4f4dfd2fbbf00922b032a612933e16339f92d247c.
- CI at commit 188c51cdfa208e4e635719ee3ff9ff58d377c023: push SUCCESS https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40109976201 ; PR SUCCESS https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40109991759 ; synthetic artifact 12566370866 downloaded, ZIP tested and H.264/AAC full decoded. CI audio is synthetic tone, NOT Japanese speech.
- User storyboard inspected; full research task transcripts and original v33 MP4 inaccessible. Japanese speech/caption semantic match, inherited rights, smartphone playback and employee approval remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, charge or auto-post.
- Next: independently verify Japanese voice and subtitle semantic alignment, acquire approved high-quality image-first media, and compare original v33 if accessible.
