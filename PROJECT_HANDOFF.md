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


## Cycle824 checkpoint — 2026-10-25 JST (Draft PR #140; not merged)
- Latest checked main: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`. Branch `quality/cycle824-sequential-focus-20261025` is stacked on cycle823 PR #139 (AI-work Japanese UI), while sales-business cycle822 PR #137 remains separate.
- Added `quality/cycle824/focus824.py`, six tests and isolated Japanese-MP4 GitHub Actions workflow. Sequentially highlights left and right action/Before-After regions above caption safe zone. All ten genre palettes supported, but only sales_business local review and ai_work CI video are exercised.
- Local cycle824 sales_business MP4 derived from cycle822: 23.933333 s, 1080x1920, 30fps, 718 frames, H.264/AAC 48kHz, full decode PASS, inherited AAC MD5 `8d0baabf50866471846346e7159046e2`, SHA256 `9bc59d9a36f6d6a8afb6fd09f1f28b711bf2f1b0c5741982acba368102c842a5`. Local video not committed; distributed only in conversation.
- The AI-work CI workflow generates its own Japanese Open JTalk narration, retains 24 Japanese caption states, and is designed to validate full decode/audio-bitstream equality; check actual Actions status before claiming CI success.
- TikTok市場分析/動画研究 full transcripts and original v33 MP4 unavailable; user-provided 16-panel storyboard accessible in file library. No v33 parity claim.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Speech naturalness, word-level caption sync, rights and smartphone testing, employee approval still pending. No auto-post, paid services, or merge.


## Cycle825 checkpoint — 2026-10-25 JST (Draft, not merged)
- Main checked at 18e084c38db0dc55db7dfc0532b9451b1167f2aa; new branch quality/cycle825-image-led-semantic-gate-20261025 stacked on cycle824 PR #140. No merge or production posting.
- Added quality/cycle825/image_scene825.py, audit825.py, eight unit tests and an isolated CI workflow. Ten genre IDs; provenance manifest fails closed on private or unapproved-for-review images. Script-to-caption equality gate compares all 8 TTS input sentences with 24 ASS states; DOES NOT verify actual spoken audio, pronunciation or word-level sync.
- Local sales_business cycle825 review MP4 changes 6.47–9.45s from a flat KPI card to a new previously generated generic laptop/desk photo. Output 23.933333s, 1080x1920, H.264/30fps/718 frames, AAC/48kHz; full A/V decode PASS; inherited audio MD5 unchanged 8d0baabf50866471846346e7159046e2; output SHA256 3cf5dd5a286ce3f896b3df40e62218ba2d90841167123fb9fc6ebf291f361ce5. Eight local tests PASS. The image and inherited audio are not committed or uploaded to public GitHub.
- CI builds separate ai_work Japanese Open JTalk review MP4 using original procedural art. Its actual status/artifact must be checked, not assumed.
- Research summaries accessed; full TikTok市場分析 and TikTok動画研究 transcripts unavailable. 16-panel user storyboard found. Original v33 reference MP4 unavailable this cycle.
- Remaining gates: original-v33 comparison, actual Japanese listening/transcription and word-level caption alignment, rights/publication approval, smartphone playback, employee approval. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.


## Cycle826 checkpoint — 2026-10-25 JST (Draft, NOT MERGED)
- Latest main confirmed: 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Based on open PR #141, no merge. Other open PR #142 is parallel and NOT incorporated.
- Improvement vs cycle825 AI-work MP4: replace scene 4 at 9.687–12.917s (97 frames) from static instruction-card to fictional animated typing → execute → result preview. Preserve existing Japanese AAC bitstream, 24 caption states and lower caption region. 10 genre palette variants share the same compositor; only AI-work finished MP4 tested.
- Local source: prior cycle825 CI artifact, 25.833333s 1080×1920 H264/30fps 775 frames AAC/48kHz. Local renderer 8 tests PASS; full A/V decode PASS; exact AAC packet MD5 unchanged; new MP4 SHA256 cf518c80313b2e1e1baa4602faf1293877f1fdfdc512a3044aed95f15e680b25. Artifact is in user conversation, NOT committed to public GitHub.
- Added quality/cycle826/interaction826.py, test_interaction826.py, and .github/workflows/cycle826-live-prompt-japanese-review.yml. CI generates a SEPARATE new offline Japanese Open JTalk MP4 with attribution, checks script/24 ASS captions and audio bitstream identity, uploads a 7-day review artifact. Confirm actual Actions outcome separately; code commit alone does not prove CI success.
- TikTok市場分析 and TikTok動画研究 full chat/task bodies unavailable; past research summaries consulted. User-provided 16-panel storyboard visually inspected; original v33 MP4 unavailable for direct comparison. Do not claim reference equivalence.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Actual speech recognition/naturalness, word-level caption sync, voice/image release rights, smartphone playback, employee approval remain pending. No paid API, auto-post or unauthorized merge.
