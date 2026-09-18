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
