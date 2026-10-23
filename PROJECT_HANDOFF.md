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


## Review-only checkpoint: cycle797 (2026-10-24 JST, stacked Draft PR #90)
- Based on cycle796 Draft PR #87; **main remains unchanged**. Branch: quality/cycle797-crop-safe-hook-20261024.
- Fixed visible 0–3.2s opening card Japanese footer clipping: recreated readable BEFORE/AFTER cards, synthetic 4-month table summing to 650,000円, and separate caption/disclaimer safe lanes.
- Actual local review-only MP4: H.264/AAC 1080×1920, 30fps, 714 frames, 23.848s, SHA-256 b01d16cce051fb27ab37ab6f61c67609a657bbaa0ffa08ae67fd56c2cef7d091. AAC packets unchanged from cycle796, full decode PASS, 11 local tests PASS.
- CI: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40000599194 SUCCESS. CI uses synthetic image proof only, not user footage, voice or completed Japanese MP4.
- User 16-panel storyboard visually inspected. Full TikTok市場分析/TikTok動画研究 transcripts and v33 original MP4 not available for direct comparison.
- Inherited video/photo/voice rights, Japanese speech/caption semantic match, phone playback and human publication approval are NOT verified. REVIEW ONLY, DO NOT MERGE OR POST.
- Next: narration semantic QA, approved-asset reproducible CI and actual v33 visual comparison. This renderer is **not** original recovered v33 code.

## cycle798 QA checkpoint — 2026-10-24 JST (review only)
- Based on unmerged cycle797 Draft PR #90 (head 33dc2504b753cca91967a58fe0b6c123406b2e2f). Main unchanged at 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Reimplemented an original, synthetic animated copy→paste step in frames 348–419 (11.6–14.0s). Unlike cycle797 opening-crop repair, this adds an explicit progression from AI result rows to spreadsheet rows. Only AI/仕事効率化 was rendered; 10-genre config/geometry is shared.
- Local inherited Japanese-audio review MP4 (not committed/uploaded): cycle798_COPY_PASTE_DEMO_REVIEW_ONLY.mp4, SHA256 36e06562806644a0eb26296c73b931357733e9f089d361240c506a4595fb5588, H.264 1080×1920 30fps 714 frames, container 23.848s, AAC 48kHz copied bit-identically from cycle797. Full A/V decode PASS. 11 local tests PASS. MAE changed region 12.7s=57.0463, unchanged 8.0s=0.3524 and 15.0s=0.498.
- CI workflow cycle798-review.yml renders ONLY original 2.4s synthetic segment with a 440Hz tone; not a full Japanese narration artifact. CI status must be checked separately; do not infer success from local tests.
- Prior research: TikTok市場分析/TikTok動画研究 summaries used, full transcripts inaccessible; 16-panel user storyboard inspected, v33 original MP4 not available in this run. Speech/caption semantic sync, mobile device, rights, v33 parity and employee approval NOT verified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid service or auto-post.

## cycle799 QA checkpoint — 2026-10-24 JST (review only)
- Stacked on cycle798 Draft PR #91; main unchanged. Replaced 14.0–17.2s redundant manual/formula proof scene with 96 original frames and a staged, legible arithmetic → =SUM(B2:B5) → 650,000円 agreement. Fictional data, 10-genre reusable layout; one AI efficiency review demo.
- Local inherited Japanese-narrated MP4 is for private human review only and is not committed. Original v33 MP4 and TikTok research transcripts unavailable for direct inspection; consult prior summaries only.
- CI: 14 tests plus original 3.2s synthetic-tone video only; no rights-unverified video/audio uploaded. Full narration semantic matching, mobile playback, rights and publication approval remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge or auto-post.

## 2026-10-24 cycle802 review-only checkpoint (unmerged)
- Stacked Draft PR #100: https://github.com/genokuda0902/tiktok-ai-employee/pull/100 (base is unmerged PR #97 branch). Main is unchanged.
- Implemented configurable scene-window optical centering: only 0–3.2s and 20.8–23.85s shift +136px; middle scenes stay unchanged to avoid right-edge UI clipping. 10-genre validation, fail-closed rights and publication checks.
- Implementation and CI fix commit: 8e8a8df516fda61ff8b9b449c1cc7fd6b5cf5a0e.
- 13 unit tests on GitHub PASS, push CI SUCCESS: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40037793350 ; PR CI SUCCESS: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40037799801 .
- CI artifact 12537518362 was downloaded and verified: 2.000s H.264/AAC 1080x1920, **synthetic 440Hz tone, NOT Japanese voice**. Real user media never uploaded.
- Local review-only Japanese-voice MP4: 23.848s, 714 frames 30fps, H.264/AAC 1080x1920; SHA256 ebd6bb1d1961d01b2253c6015700bff03ce2ed06cdc1d7fd07c9efa588b123fa. Inherited AAC packet hash matches cycle801. Full A/V decode PASS. Not committed or posted.
- Prior TikTok市場分析/TikTok動画研究 summaries and Library 16-panel storyboard inspected; full original task transcripts and v33 original MP4 unavailable for direct comparison. Japanese speech/subtitle semantic sync, phone playback, rights and employee approval remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
