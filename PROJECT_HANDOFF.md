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

## 2026-10-24 — cycle814 review-only checkpoint (unmerged)
- Stacked Draft PR #122 on unmerged #120: https://github.com/genokuda0902/tiktok-ai-employee/pull/122
- Saved shared 10-genre focus renderer and 13 tests; actual sanitized Calc scene zooms 1.52x and pans from B2 target to D2 computed gap, with callouts delayed until visible in source pixels.
- Local private review MP4 SHA256 `66ebd1f7fd81dcdfef2ce1fba09106f91f28fd36140d68cfcc799402fb8feda2`; 1080x1920, 30fps, 718 frames, 23.933s, H.264/AAC 48kHz, full decode PASS, inherited AAC bitstream identical to cycle813.
- 13 local tests PASS; synthetic-only CI SUCCESS https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40084621421, artifact 12556363201 downloaded and decoded. CI artifact is NOT the private Japanese-narrated MP4.
- Research task full transcripts and v33 original MP4 unavailable; user's 16-panel storyboard inspected. No direct quality parity claim.
- Independent ASR/caption semantics, asset rights, smartphone playback, employee approval pending. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, billing or automatic TikTok post.
- Full reproducible delta: `quality/cycle813/CYCLE814_DELTA.md`.

## 2026-10-24 — cycle815 review-only checkpoint (unmerged)
- Stacked Draft PR #123 on #122: https://github.com/genokuda0902/tiktok-ai-employee/pull/123
- Added 10-genre reusable fictional KPI 3-beat animated panel (6–9s) and 12 tests. Local private Japanese-narrated MP4 SHA256 `c90c94e40af64aeb2932ab70c9b5acf57cae09d9baff8bb157da80a674f91402`; 1080x1920, 30fps, 718 frames, 23.933s, inherited AAC bitstream unchanged, full decode PASS.
- Synthetic-only GitHub Actions PASS: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40088325725, artifact 12557159419 downloaded, ZIP integrity and full A/V decode verified. CI synthetic tone is NOT the private Japanese narration.
- User-provided 16-panel storyboard directly inspected; full TikTok市場分析/TikTok動画研究 transcripts and original v33 MP4 inaccessible. No v33 quality equivalence claim.
- Independent ASR/caption meaning, asset/voice rights, phone playback, employee approval pending. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, billing or automatic posting.
- Details: `quality/cycle815/CYCLE815_DELTA.md`.
