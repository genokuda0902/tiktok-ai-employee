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

## 2026-10-29 cycle951 independent review-only checkpoint (PR #348)
- This is an unmerged review branch stacked on PR #345, separate from concurrent PR #347 deghost and PR #346 chapter badge; latest main remains `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- Verified local code: `cycle951/src/evidence_consistency.py` blob `d33a89fc45b9d764503ac59942d75a61277f757a`; 27 pytest tests PASS; source arithmetic ledger 12+16+18=46 and 8+9+12=29.
- Local private review MP4 SHA256 `950b8d4d336cdb5f4ba4a774348e19c4f0dfc8bff98046e2eeeed2a9d2976c2d`; H.264 1080x1920 30fps 691 frames, AAC 48kHz ADTS unchanged, full decode PASS; no private MP4 in public GitHub.
- Reference storyboard 16 panels directly inspected; original v33 MP4, full research chat transcripts and independent Japanese ASR unavailable. Caption meaning, phone playback, rights and employee approval UNVERIFIED; PUBLICATION_NOT_APPROVED. No merge, paid service or posting.
- Draft PR: https://github.com/genokuda0902/tiktok-ai-employee/pull/348 ; CI tests source, not full private MP4.

## 2026-10-29 cycle961 review-only checkpoint (Draft PR #361)
- Unmerged independent review branch stacked on cycle960 PR #360; main was 18e084c38db0dc55db7dfc0532b9451b1167f2aa at inspection.
- Previous cycle960 410x310 proof card -> 770x630 two-beat source-backed fictional Calc proof, 0.35-2.34s, verified A=46/B=29. No fabricated real Excel UI.
- Local private MP4 SHA256 4257fccc11a1e8880eb208a5a50f53a9fb815c35f53069048409da021084344d; 1080x1920 30fps 691 frames, 23.033333s, H.264/AAC 48kHz stereo. Full A/V decode PASS; original AAC ADTS bitstream identical; caption area sampled max mean delta 0.4861/255.
- 21 local synthetic tests PASS; CI checks code/safety only, not full private media. Private MP4 shared in ChatGPT, NOT committed to public GitHub.
- Source provenance: accessible market/video research summaries and prior 16-panel storyboard description; full research chats, original storyboard image this run, original v33 MP4 not directly available.
- Outstanding: independent Japanese ASR and subtitle meaning/timing alignment, source publication rights, phone playback, employee approval, actual Actions billing. Ten genre policies, only ai_work verified; other nine fail closed. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- Draft PR: https://github.com/genokuda0902/tiktok-ai-employee/pull/361 . No merge, auto-post, private media upload or paid contract.

## 2026-10-29 cycle963 private review-only checkpoint
- Distinct from cycle961 mobile proof zoom and parallel cycle962 loudness normalization: add five quiet **original synthesized UI sound cues** at 1.39, 8.02, 11.05, 16.25, 21.15 seconds, synchronized to existing evidence, report, prompt, verification and closing beats.
- Source: cycle961 private review MP4 SHA256 `4257fccc11a1e8880eb208a5a50f53a9fb815c35f53069048409da021084344d`. Output SHA256 `5df3b08c7ec6d18d3de52616939bc5b36fd1d1f3d790b5caf0e50d5c8cf54c6f`. MP4 remains in ChatGPT private attachment, **not in public GitHub**.
- H.264 video stream SHA256 unchanged `d3bdf1fa0448fcdf99f3e04df24620a828b57edcacae900ab3aa8daf5297dc72`; burned captions identical. 1080x1920, 30fps, 691 frames, 23.033333s, AAC stereo 48kHz Japanese-tagged. Full A/V decode PASS, source/output PCM correlation 0.998844, peak <0.9; all five cue windows have measurable extra audio versus non-cue window. 19/19 local synthetic tests PASS.
- Directly inspected user Library image `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels, ~36s) and prior research summaries. Full original research chats and original v33 MP4 inaccessible this run. Current video remains 8 scenes and 23s, **not reference-equivalent**.
- Ten genre cue policies, only ai_work approved for private test; nine other genres fail closed. Independent Japanese ASR, caption semantic/timing match, phone playback, source rights, employee approval, and Actions actual billing remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- No auto-post, paid service, private media upload, or merge. Branch: `automation/cycle963-original-ui-sound-cues-20261029`.


## 2026-10-29 cycle964 arithmetic-continuity private review checkpoint
- Distinct from cycle963 original UI sound cues: replace only scene05 11.60–14.50s with three-step source row check. Fictional rows Apr (12,8), May (16,9), Jun (18,12) yield totals 46/29; explicitly not an actual app recording.
- Source private cycle963 MP4 SHA256 5df3b08c7ec6d18d3de52616939bc5b36fd1d1f3d790b5caf0e50d5c8cf54c6f. Output private cycle964 MP4 SHA256 cb8d504b95c7e06f1b3acb216a7f283e83a2b6276b22e83fb82f5b73e2e557cc. Neither is committed.
- H264 1080x1920 30fps 691 frames / 23.033s, AAC 48kHz stereo. Full A/V decode PASS; audio ADTS stream identical ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e. Subtitle ROI sampled maximum mean delta 0.5236/255; 14 local synthetic tests PASS.
- Consulted accessible TikTok market/video-study summaries and directly inspected user's 16-panel storyboard. Full original research chats and original v33 reference MP4 unavailable. Still 8 scenes, 23s, not reference-equivalent.
- Ten genre rules, only ai_work review-rendered. Independent Japanese ASR, caption semantic/timing match, source rights, phone playback, employee approval and actual Actions billing unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- No merge, auto-post, paid service, or private media uploaded. Work branch automation/cycle964-arithmetic-continuity-20261029-2053.


## 2026-10-29 cycle966 real Calc-backed finished-sample review
- Distinct from cycle964's source-check drawing and parallel PR #366 save CTA: scene03 (5.80–8.70s, frames 174–260) now displays an **actual LibreOffice Calc SUM-calculated CSV export**. The PDF table is real Calc output; accompanying monthly comparison bars are an illustration from the same fictional source. It is **not** an Excel/ChatGPT live operation capture.
- Private source cycle964 SHA256 cb8d504b95c7e06f1b3acb216a7f283e83a2b6276b22e83fb82f5b73e2e557cc; private output cycle966 SHA256 afa207d9b22dc40ab4ba24c765e7b675bb7246332011cc2d91a827713931eb3c. No private media committed.
- Real LibreOffice formula PDF text independently confirmed totals 46 and 29. MP4 1080x1920 H264 30fps 691 frames / 23.033s; AAC 48kHz stereo ADTS bitstream unchanged; full A/V decode PASS. Caption protected region max sampled mean delta 0.6694/255; outside-scene max 1.0532/255. Local synthetic tests 9/9 PASS.
- Accessible TikTok market/video research summaries and user's 16-panel storyboard original inspected; full original research chats and v33 original MP4 unavailable. Still 8 scenes vs reference 16, 23s vs ~36s.
- Ten genre policies, only ai_work reviewed. Independent Japanese ASR/semantic subtitle timing, rights, smartphone playback, employee approval, and Actions actual billing unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, auto-post, paid service or private upload.
- Work branch automation/cycle966-real-calc-proof-20261029-2153; CI synthetic only.

## Review-only cycle968 checkpoint (2026-10-29 JST)
- Based on unmerged cycle966 PR #367 (head `5c12bc71b1d9bab302f93b0f80742af43cf59403`); parallel cycle967 PR #368 unchanged. The review-only renderer/test/CI files are in `cycle968/` and do not touch the production pipeline.
- Private output MP4 SHA256 `a777828ff5db82ba1df8e74c4c1f1419b4c893512707435cd3e6c17922567bd4`, 1080x1920 H264 30fps 691 frames, 23.033s, inherited Japanese AAC ADTS SHA identical. Scene04 frames 261–347 replaced with readable purpose/conditions/output instruction cards. 8 local unit tests and full A/V decode passed; see `cycle968/README.md`.
- The private MP4 is not committed. CI tests synthetic media only. Original v33 MP4, full prior research chats, independent Japanese ASR/semantic subtitle timing, smartphone playback, commercial rights, employee approval and actual Actions billing are unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Do not merge or auto-post without review. The ten genre palettes are not ten validated outputs.

## Review-only cycle970 checkpoint (2026-10-29 JST)
- Base is unmerged cycle968 PR #369; parallel cycle969 PR #370 is untouched. New cycle970 animated Japanese prompt entry replaces scene04 upper panel only (frames 261–347). Explicitly simulated, NOT a live ChatGPT recording.
- Private local MP4 source cycle968 SHA256 `a777828ff5db82ba1df8e74c4c1f1419b4c893512707435cd3e6c17922567bd4`; output cycle970 SHA256 `ebee379a95b4b46ce8f10606262cd6b019e28aad1e8a96b18d73bd1fb563c824`. H264 1080x1920 30fps 691 frames 23.033s; AAC 48kHz stereo ADTS SHA identical `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`. Full A/V decode PASS, changed scene 87 frames avg pixel difference 80.297/255, subtitle protected region max mean delta 0.905/255, outside-scene max 1.618/255. Local 10/10 unit tests PASS. CI is synthetic only.
- Accessible TikTok market/video research summaries and user 16-panel storyboard directly inspected. Original v33 MP4 and full original research chats unavailable. Still 8 scenes / 23s vs storyboard 16 / ~36s.
- Audio energy diagnostic is NOT ASR; Japanese speech meaning and subtitle semantic timing remain unverified. Source commercial rights, real smartphone playback, employee approval and actual Actions billing remain unverified. 10 genre palettes, only ai_work rendered; other nine fail closed.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, paid service or public private-MP4 upload.

- cycle972 (2026-10-30 JST, Draft PR #373): 11.60–14.50s scene05 replaced with animated grouped 4–6月 chart using fictional A=(12,16,18), B=(8,9,12), exact totals 46/29. Private review MP4 SHA256 `ae8ba688c6808ca13df8bd353d16d74ab00b2f98ab87f0a741e48a661cdb9648`; 1080×1920 H264/AAC 23.033s, 9 local unit tests PASS, full decode PASS, AAC elementary-stream identical, sampled caption ROI mean pixel difference <=1.115/255. CI synthetic only. Japanese ASR, subtitle semantic timing, rights, smartphone playback and employee approval UNVERIFIED; do not publish. Separate from PR #372. Source and tests: `cycle972/`. No merge.
