## cycle1130 (2026-11-02 JST, REVIEW ONLY)
- Corrected a previously overlooked contradiction in scene03: overlay =SUM(B2:B4) vs selected C5 and visible =SUM(C2:C4). Fictional B total 46, C total 29; corrected frames 180–217.
- Source cycle1128 private MP4 SHA256 8200e485fca3042424b7d6f78d43bbd8b7ec7b3893197a6bee61418d1348ded0; output cycle1130 private MP4 SHA256 f20bcd0ca234cc68fa7eec82d6d07aa23775f4c44210a8aa7dcb333b8450b91e.
- Local 10 unit tests PASS; 691-frame H264/AAC full decode PASS, audio ADTS identical, captions protected. GitHub workflow synthetic media only; private MP4 not committed.
- Code/tests/CI: quality/cycle1130/ and .github/workflows/quality-cycle1130.yml. Formula/selected-cell/data-total gate supports 10 genres; specific geometry requires per-video review.
- User 16-panel storyboard directly viewed; full TikTok research chats and original v33 MP4 inaccessible. Independent Japanese ASR, phone playback, rights, staff approval, Actions billing and reference parity NOT VERIFIED. Do not merge/post/auto-publish.

## cycle1128 (2026-11-02 JST, REVIEW ONLY)
- Corrected scene04 factual month-count mismatch (4月–6月 = 3か月, not 4か月) with a tiny 69-frame digit replacement; preserved AAC and burned-in captions.
- Source private MP4 SHA256 `68d13d172353e06fa6913a176de347a7eae1e592791fdd460ce760418007fc2e`; output private MP4 SHA256 `8200e485fca3042424b7d6f78d43bbd8b7ec7b3893197a6bee61418d1348ded0`; full A/V decode PASS, 691 frames 1080x1920/30fps, 10 local tests PASS.
- Code/tests: `quality/cycle1128/`; CI synthetic only. Original v33, independent Japanese ASR, rights, smartphone and employee approval remain unverified. Never merge/publish without human review.

# TikTok AI社員システム — authoritative handoff

## cycle1132 (2026-11-02 JST, REVIEW ONLY)
- Distinct from cycle1130 formula correction: added three original non-musical quiet UI proof/reuse cues at 6.2s, 16.2s, 21.25s. No third-party music or recordings. Exact H264 video stream unchanged; original Japanese AAC narration re-encoded to mix SFX (not bit-identical).
- Private source SHA256 f20bcd0ca234cc68fa7eec82d6d07aa23775f4c44210a8aa7dcb333b8450b91e; private output SHA256 6b72e8ebbec527848b3a85315a23bfa4b0cf4809193ffae8e85af78443189126. Full 691-frame 1080x1920 30fps 23.033s H264/AAC 48kHz decode PASS; video elementary stream identical; final audio peak -3.3 dBFS; local 6 tests PASS.
- Code/tests/CI: quality/cycle1132/ and .github/workflows/quality-cycle1132.yml. Ten genre safety contract, synthetic-only CI, fail-closed on missing private-review approval or source hash mismatch. Real MP4 and private manifest never committed.
- Directly inspected user's 16-panel storyboard via file Library. TikTok research summaries accessed; original full task chats and v33 MP4 inaccessible. Still 8 scenes/23s vs 16/36s, cinematic visual gap remains.
- Independent Japanese ASR, pronunciation, subtitle semantics, real-phone playback, rights, employee approval, reference parity and Actions actual billing NOT VERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; no merge, paid service, or auto-post.


## Latest review-only checkpoint — cycle1126 (2026-11-02 JST)
- Branch `quality/cycle1126-completion-reuse-cue` (based on open PR #525). Local private output MP4 SHA256 `68d13d172353e06fa6913a176de347a7eae1e592791fdd460ce760418007fc2e`, H.264 1080x1920/30fps/23.033s with unchanged AAC 48kHz and burned Japanese subtitles; full local A/V decode PASS.
- Distinct change: animated closing 02 Save → 03 Reuse focus during 20.8–22.8s, ten-genre safe-area/PII/approval gates and synthetic A/V tests. Code and tests in `quality/cycle1126/`; CI in `.github/workflows/quality-cycle1126.yml`.
- Original 16-panel user storyboard inspected; original v33 MP4 and full market research chats not accessible. No semantic Japanese ASR, phone test, media rights or publication approval. Do not merge/post. See `quality/cycle1126/README.md`.
- This checkpoint describes a review-only reimplementation; it does not supersede the product/security decisions below.

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


## 2026-11-02 cycle1134 checkpoint (draft; not merged)
- Prior cycle1132 audio SFX retained; new quality/cycle1134/proof_share_bars.py adds offline proportional numeric bars inside existing scene06 evidence cards, based on independently verified fictional rows A=46, B=29, total=75.
- Local review MP4: 1080x1920, 30fps, 691 frames/23.033s, full decode PASS, original AAC bitstream SHA256 unchanged; 9 local unit tests PASS. Private video and manifest are NOT committed. See quality/cycle1134/RESULT.md for source/output SHA256 and measured ROI differences.
- Reference storyboard directly inspected; full research transcripts and original v33 MP4 not accessible. 8-scene output still below 16-panel storyboard cinematic diversity. Japanese ASR semantics, smartphone playback, rights, staff approval and billing remain unverified.
- No merge, auto-post, external distribution or paid API. PUBLICATION_NOT_APPROVED. Changes in draft PR on quality/cycle1134-proportional-proof-bars.
