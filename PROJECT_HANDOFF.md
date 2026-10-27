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


## cycle883 checkpoint (2026-10-27 JST; review-only branch)
- Branch: `automation/cycle883-kinetic-wipes-20261027`, stacked on open Draft PR #246; no merge. Latest verified main remains `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- New `video_engine/cycle883`: seven 9-frame diagonal kinetic wipes, reusable across ten genres; 10 local tests and synthetic 90-frame H264/AAC smoke PASS. Source media is the accessible private cycle881 video, not the unavailable cycle882 video. **Do not infer cycle883 outperforms cycle882**.
- Private preview MP4 SHA256 `595d365549373f0de96ae6e8868725bea038be903bb194a00983b432c0c7b1fc`, 1080x1920/30fps/691f/23.033s/AAC48k, full decode PASS; source AAC elementary stream unchanged. Caption-safe region checked across all 691 frames (max sampled delta 1.1074).
- Private MP4 and inherited audio remain outside GitHub. CI tests only synthetic code/media, not private final MP4. Original v33 source/video not recovered here; reference storyboard directly inspected, research full chats inaccessible. Independent Japanese transcription, semantic subtitle sync, phone playback, rights and employee approval are still outstanding.
- Status **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid service or automatic TikTok posting.


## cycle884 checkpoint (2026-10-27 JST; review-only branch)
- Branch `automation/cycle884-row-focus-20261027`, stacked on open Draft PR #248; **not merged**. Latest verified main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- New `video_engine/cycle884`: four timed focus outlines in first 2.967s of **accessible cycle883**; distinct from cycle883's seven wipes and parallel PR #247's Chromium zoom. Ten-genre geometry, safe-zone and rights/source-hash gates; 12 local tests + 45-frame synthetic H264/AAC smoke PASS.
- Private MP4 SHA256 `1a57acc1d8151c52f53d5b104f7f913a685d07fbaee2bcc5a4cd6a0314680afb`, H264 1080×1920/30fps/691f/23.033s, AAC48k; full decode PASS. Source AAC bitstream identical. All 691 frames sampled, max subtitle-band mean difference 1.0177. This **does not prove semantic subtitle sync**.
- Only `ai_productivity` rendered. The 16-panel storyboard was directly inspected; full research chats, original v33 MP4 and cycle882 MP4 inaccessible for direct comparison. Original v33 source not recovered. Independent ASR, phone playback, source rights and employee approval still missing.
- Final MP4 remains in private ChatGPT sandbox, not GitHub. CI checks only synthetic media; no merge, paid service or auto posting. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.


## 2026-10-27 JST — cycle885 review checkpoint (unmerged branch)
- Branch: automation/cycle885-kinetic-task-cards-20261027, based on cycle884 row-focus PR #249; parallel PR #250 untouched. Main unchanged at 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Distinct from cycle884's first-scene four row outlines: second scene (frames 89–169) now shows three staggered task cards and a concrete single-task CTA. Ten-genre shared renderer/test gates, fictional demonstration only.
- Private review MP4 generated locally, SHA256 5f92fc4a175b762dd0c8188170f725e1fa3175f6542fcafa2306fbcd14c02465; 1080x1920/30fps/691f/23.033s, H264/AAC48kHz. All 691 frames compared; 80/81 target frames substantially changed; AAC elementary SHA identical; full A/V decode PASS. Local 15 unit tests and synthetic 1-second A/V smoke PASS.
- No private media, inherited voice, screenshot, manifest or generated PNG committed. GitHub CI is synthetic/code-only, not completed Japanese MP4. Source voice rights, independent Japanese ASR/caption semantic sync, phone playback, employee approval and original v33 parity UNVERIFIED.
- See video_engine/cycle885/README.md for reproduction and measured deltas. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid service, external upload or automatic posting.

## 2026-10-27 JST — cycle886 local browser save proof (unmerged)
- Branch `automation/cycle886-offline-save-proof-20261027`, based on cycle885 Draft PR #251 (head `19802dbcb24ed8f3e3bb8d05a03889d336b2fd57`). Latest checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`. No merge.
- Distinct change: scene07 frames 510–587 (17.000–19.600s) replaced by three **genuine local Chromium DOM action screenshots** (fill -> verify computed fictional 46/29 -> save), with stage markers. Original offline HTML, not ChatGPT or Excel and not a continuous screen recording. Ten-genre text/geometry/privacy validation.
- Private review MP4: SHA256 `090e9ebe87a2aa8e05beba75b3b4f628f1bbcbf069807e64d2720773c7465d10`; source cycle885 SHA256 `5f92fc4a175b762dd0c8188170f725e1fa3175f6542fcafa2306fbcd14c02465`. H264 1080x1920/30fps/691 frames/23.033s, AAC48k stereo, full A/V decode PASS. All 78 target frames changed substantially; outside scene max sampled delta 1.264; subtitle band max sampled delta 1.157. Audio ADTS SHA identical.
- Local 12 unit tests PASS (including browser); CI tests synthetic H264/AAC and pure code only, browser tests explicitly skipped unless provisioned. Finished inherited Japanese MP4 is private sandbox media, NOT in GitHub.
- User 16-panel storyboard inspected; full TikTok research chat bodies and original v33 MP4 inaccessible. Independent Japanese ASR/semantic subtitle sync, voice/media public-use rights, phone playback, employee approval and actual Actions billing UNVERIFIED.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No auto posting, paid services, external private-media upload or merge. See `video_engine/cycle886/README.md`.


## 2026-10-27 JST — cycle889 arithmetic correction animation (unmerged)
- Based on open cycle886 Draft PR #253 (head a7e21c51298482e7bb6d54e4d6b00c22acda369f), main independently checked at 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Parallel unmerged #254 (narration-reactive header) and #255 (focus highlights) were inspected and not merged. This cycle is distinct: source-grounded correction scene06 frames 422–509, not scene07 browser states or focus corners.
- Source local cycle886 MP4 SHA256 090e9ebe87a2aa8e05beba75b3b4f628f1bbcbf069807e64d2720773c7465d10; output local cycle889 MP4 SHA256 0edfc3bd34ba6b1beccfd9a7016219178dc709d276dee40fa0454ec9dce2d99c. 1080x1920 H264 30fps 691f 23.033s, inherited AAC 48k stereo bitstream SHA unchanged (2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9). All 88 target frames changed, all 691 caption and header bands sampled, full A/V decode PASS. Local 15/15 unit tests PASS. Fictional correction: 6月営業A 17 -> 18, total 45 -> 46.
- Code: video_engine/cycle889/; CI workflow: .github/workflows/cycle889-qa.yml. CI is **synthetic media and code only**; actual Japanese review MP4 is private in ChatGPT sandbox, NOT uploaded to GitHub.
- TikTok市場分析/TikTok動画研究 prior accessible summaries consulted; original full chats inaccessible. User 16-panel storyboard known from prior inspection, but original v33 MP4 not retrieved this run. No reference parity or public-release quality claim.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**: independent Japanese ASR/semantic caption sync, inherited media/voice rights, phone playback, employee approval, TikTok retention and actual Actions billing unverified. No merge, paid service, private-media upload or auto-post.

## 2026-10-27 JST — cycle890 Japanese prompt entry motion (unmerged)
- Based on open Draft PR #256 (cycle889 head `11f5d824999459498e07f7d164ba5772a61f526f`). Independently checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`. Other open PRs #254/#255 were not merged.
- Distinct from cycle889 arithmetic scene06: scene04 frames **251–335** now progressively type the exact three-line Japanese offline demo prompt with cursor and final verification emphasis. Ten-genre shared renderer, source SHA/rights fail-closed gate, 18 local tests.
- Input local cycle889 SHA256 `0edfc3bd34ba6b1beccfd9a7016219178dc709d276dee40fa0454ec9dce2d99c`; output local cycle890 SHA256 `a255c93f861897f07ea48debaa1a293177fab94bda008b0a1219345dd9ce3c08`. H264 1080×1920 30fps 691 frames 23.033s; AAC48k stereo elementary bitstream identical. All 85 target frames changed; full 691-frame region comparison, complete A/V decode PASS.
- GitHub workflow `.github/workflows/cycle890-qa.yml` verifies code and **synthetic** composited A/V only; private completed Japanese MP4 is shared in ChatGPT sandbox, not GitHub.
- User 16-panel ChatGPT×Excel storyboard inspected this cycle; full research chats and original v33 MP4 unavailable. No independent Japanese ASR, pronunciation or semantic subtitle match; rights, phone playback, employee approval, TikTok metrics and actual Actions billing unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-posting, paid service, or inherited media upload. Next priority: independent offline Japanese ASR or an auditable manual transcription gate; richer genuine UI/person visuals.

## Isolated review checkpoint — cycle892 (2026-10-27 JST)
- Draft PR #261 (base unmerged PR #260); this checkpoint is **not on main** and **not merged**.
- Scene02's previously sparse/repeated-task area now uses an original, explicitly fictional 3-step offline spreadsheet-style UI, not actual Excel footage. Frames 89–169 modified. Shared module: `video_engine/cycle892/repeated_task_ui.py`.
- Local review MP4 SHA256: `2577cc9bf686a956b35e543002826d13031eb5e7be7cbc35439772b0bcff75af`. H264 1080x1920 30fps 691 frames/23.033333s, AAC 48kHz stereo. Full decode PASS; AAC stream unchanged; caption-band max MAE 0.9914; 81/81 scene frames changed; 19 local tests PASS. Completed MP4 is **private sandbox only**, not a GitHub artifact.
- Original v33 MP4 and full research chat text were unavailable; prior research summaries consulted. Original user 16-panel storyboard image was directly opened from the file Library (human frustration, AI/Excel operation, robot, Before/After and CTA panels). Independent Japanese ASR and semantic caption matching, rights, phone playback, employee approval and actual Actions billing remain **unverified**.
- No auto-post, merge, public-media upload, or paid service. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
- Next: independent offline Japanese ASR/transcript QA, real approved operation footage, v33 direct quality comparison if available.

## 2026-10-27 cycle894 — review-only Before/After comparison (unmerged)
- Proposed in Draft PR #263 (`automation/cycle894-before-after-proof-20261027`, based on unmerged cycle892 PR #261). Renderer commit `3ad2b5ec6da4a679c6fab6809071e60ef87595d1`, 12 local tests PASS; synthetic-only CI workflow. Do not treat this as mainline production.
- Local private completed MP4 SHA256 `7e423364d2865d22fa0499aa8e716af35732459f142967913e36d5b085f1e0f7`, H264 1080×1920 30fps/691 frames/23.033s AAC48k, full decode PASS, source audio bitstream unchanged, caption region comparison PASS. Media not committed to GitHub.
- Before/After is a fictional workflow illustration, **not** measured time saved or genuine ChatGPT/Excel screen recording. Ten genre IDs supported; only AI productivity video rendered.
- Original v33 MP4, independent Japanese ASR and subtitle meaning sync, inherited rights, phone playback, employee approval, actual Actions billing remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; no merge, automatic post or paid service.

## 2026-10-27 cycle896 — offline evidence magnifier (unmerged)
- Branch `automation/cycle896-proof-magnifier-20261027`, based on unmerged cycle894 PR #263; distinct from parallel cycle895 PR #264. Code: `quality/cycle896/`; review-only local MP4 was NOT uploaded to GitHub.
- Locally generated actual 23.033s H264 1080x1920 30fps / AAC 48kHz video from cycle894 SHA256 `7e423364d2865d22fa0499aa8e716af35732459f142967913e36d5b085f1e0f7`. New SHA256 `8be7da9de4ad858563713342f47a6c7083810a9d98db6034083aa60c5a8b2946`.
- Changed scene07 frames 510–587: zoomed original **synthetic offline UI** verification area and overlaid native-size Japanese step titles. 78/78 target frames changed, minimum pixel MAE 52.609. Original AAC bitstream preserved; all 691 subtitle-region frames compared (max MAE 1.125); full A/V decode PASS. 13 local tests PASS.
- Past TikTok market/video research summaries and original user 16-panel storyboard directly consulted. Full research chats and original v33 MP4 unavailable; no equivalence claim. No independent Japanese ASR, semantic subtitle alignment, phone playback, rights or employee approval.
- Ten genre identifiers share the renderer and safety policy, but only one AI-productivity MP4 was rendered. No merge, auto-post, private-media upload, paid contract or billing action. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
- Next priority: independent Japanese transcription and timed subtitle comparison; acquire reference v33 and rights-approved footage; verify actual CI status and phone playback.
