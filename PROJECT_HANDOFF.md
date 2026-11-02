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


## 2026-11-02 cycle1136 checkpoint (draft; not merged)
- Source: cycle1134 private MP4 SHA256 `8f409be877ff1bd145a01edc2e8c268f6683e4f0df2f7df7351d4caabdf76d15`. Output: private review-only MP4 SHA256 `fea134e081c44363eb1bf3f8aecac57c4da4ed074efaffaee317eefcec379687`.
- Distinct improvement: seven 8-frame left-to-right content-only wipes at audited scene boundaries. Initial full-image dissolve prototype rejected because of doubled Japanese UI text. Existing proof bars and original AAC jpn audio preserved.
- Local QA: H264 1080x1920/30fps, 691 frames/23.033s, full A/V decode PASS, AAC elementary stream bit-identical; 30 sampled caption frames max MAE 0.749/255. Nine unit tests PASS including synthetic AV render. CI checks synthetic media only.
- Source/tests/CI/QA record: quality/cycle1136/ and .github/workflows/quality-cycle1136.yml. Ten genre safety configurations checked; only AI/Excel video rendered. Private media/manifest NOT committed.
- User's 16-panel storyboard directly inspected; accessible research summaries consulted, full task transcripts and original v33 MP4 unavailable. Current 8/23s vs reference 16/36s, cinematic gap remains.
- Independent Japanese ASR, source rights, real-phone playback, employee approval and actual CI billing NOT VERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid API, merge, auto-post or publication.


## 2026-11-02 cycle1138 checkpoint (draft, NOT MERGED)
- Based on cycle1136 review-only MP4 SHA256 `fea134e081c44363eb1bf3f8aecac57c4da4ed074efaffaee317eefcec379687`; produced private MP4 SHA256 `4a881fc32e9bd03117801c6c82f9c4e96795b2a172d71be9541d4d5b5eef3f45`. Private MP4/manifest are not in GitHub.
- New, distinct improvement: 29-frame (0.967s) soft cyan directional key-light sweep on audited opening robot ROI x110..779/y475..974. Frame 4..32, peak alpha 0.16. No text overlay, Japanese caption and header regions protected; cinematic reference quality NOT claimed.
- Local verification: H264 1080x1920 30fps, 691 frames/23.033s, full A/V decode PASS, AAC jpn 48kHz elementary bit-identical (ADTS SHA256 `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`); 12 local tests PASS including synthetic render. Source/test/workflow in `quality/cycle1138/` and `.github/workflows/quality-cycle1138.yml`.
- User storyboard directly inspected (16 panels/~36s); accessible research summaries consulted. Full research chats and original v33 MP4 unavailable. Current output still 8 scenes/23s. Independent Japanese ASR, meaning/timing alignment, source rights, smartphone playback, employee approval and actual CI billing NOT VERIFIED.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, auto-post, paid API, or private media commit.

## Verified cycle1140 review-only checkpoint (2026-11-02 JST)
- Based on unmerged cycle1138 PR #539, adds subject-local 56-frame eased 1.08x camera push/pull with mandatory 90px title guard, 10-genre safety checks, 12 local unit tests and 75-frame synthetic smoke. See `quality/cycle1140/RESULT.md`.
- Private full video SHA256 `20e3fb916ef5654c4d333863c907c35f348f4daab1fbcc7caa5a7fe6f1fcd775`; 1080x1920 30fps 691 frames/23.033s, AAC 48kHz Japanese-tagged stream bit-identical; full decode passed. Video and private manifest NOT committed.
- Independent Japanese speech transcription, subtitle meaning/timing, original v33 comparison, rights approval, phone playback, employee signoff, and actual CI billing remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No auto-post, merge or paid services.


## cycle1142 review-only checkpoint (2026-11-02 JST)
- Stacked on cycle1140 PR #541, NOT merged. New spreadsheet evidence improvement: B5 formula/label mismatch repaired in frames 182–206, with arithmetic provenance cues for B=46 and C=29 in frames 182–217. Not the previous robot zoom or original v33 engine.
- Private review MP4 SHA256 \`c3227077c8284a4d7d35e2dd4b0745f4a6e3d6615b509ce1a36db8c41d2b4053\`, H264 1080x1920 30fps 691 frames/23.033s; AAC jpn 48kHz ADTS bit-identical to cycle1140; full decode PASS; 13 local tests PASS including synthetic AV.
- All 691 caption frames compared: max downsampled caption MAE 0.4956/255. Exact renderer, QA comparison and tests stored as content-addressed tar.xz in quality/cycle1142; CI extracts and tests synthetic media only.
- User 16-panel storyboard directly inspected, research summaries consulted; full chats/v33 MP4 inaccessible. Independent Japanese ASR/caption semantic timing, rights, real phone, employee approval and billing remain unverified. HUMAN_REVIEW/PUBLICATION_NOT_APPROVED. No auto-post, merge, private-media commit or paid API.


## cycle1144 review-only checkpoint (2026-11-02 JST)
- Stacked on unmerged cycle1142 PR #544; draft PR #545. Distinct visual change: 90-frame original vector cursor guiding B5=46, C5=29, and total=75 at 14.3–17.3s. This is an illustrative cursor, not actual recorded interaction.
- Source/test Git blob `28602a651a59b6e122bc9b25e90dd39e0aa9648a` at `quality/cycle1144/source_tests.tar.xz`, SHA256 `fa081a17938d55800f7ea27ff55f56539520722efbc2f188ad0f768d506c0116`; local 11/11 unittest PASS including synthetic 2-second A/V. GitHub CI is synthetic only.
- Private MP4 SHA256 `18c7da2395524fb490f0d427e190fcbfccd2f40062482c864c389060d4bcde15`: H264 1080×1920/30fps 691 frames/23.033s, AAC jpn 48kHz bit-identical to cycle1142 ADTS; full decode PASS; 691 caption frames max MAE 0.5264/255. Full private video and manifest NOT committed.
- 16-panel/~36s user storyboard directly inspected; research summaries consulted; full original research transcripts and original v33 MP4 inaccessible. Independent Japanese ASR/caption meaning/timing, rights, phone, employee approval and Actions billing NOT verified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, auto-post, private media commit or paid services.


## cycle1146 review-only checkpoint (2026-11-02 JST)
- Draft branch `quality/cycle1146-readable-takeaway` based on unmerged PR #545, separate from concurrent PR #546. Previous cycle1144 added a vector cursor; this cycle makes the small scene02 takeaway "まずは1つ選んで試す" legible with a timed original banner at 3.10–5.65s, strictly x50–900/y1095–1227, outside Japanese caption ROI y>=1500.
- Full private MP4 SHA256 `acf8d9fac8139f08bfa4a71e7fe4900e2c2e6a0b8e44d3923c1dcdf6bdaafbb8`; 1080x1920 H264 30fps 691 frames/23.033s; AAC jpn 48kHz ADTS SHA256 unchanged `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`; full A/V decode PASS. Sampled caption max MAE 0.7092/255, effect ROI mean 42.374/255. Nine local unit tests and synthetic 60-frame render/decode PASS; GitHub CI synthetic only.
- The user 16-panel/~36s storyboard directly inspected. Accessible TikTok market/video research summaries consulted; full research chats and original v33 MP4 inaccessible. The new banner improves readability, not cinematic realism or reference parity. Independent Japanese ASR/caption semantic timing, rights, smartphone playback, employee approval and Actions billing NOT VERIFIED.
- No merge, automatic TikTok posting, confidential media upload, or paid services. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## cycle1148 review-only checkpoint (2026-11-02 JST)
- Stacked on unmerged cycle1146 PR #547, separate from concurrent cycle1217 PR #549. New improvement: fix duplicate/ghosted CTA labels in final 3-step cards, not scene02 takeaway. 3 focus states at 20.55/20.95/21.55s in audited x84..996 y970..1086; captions y>=1280 untouched intentionally.
- Local private output MP4 SHA256 e0015a1bf632a9676cef3af8073f939edc766ea92841c14d6df30af23134356e; source acf8d9fac8139f08bfa4a71e7fe4900e2c2e6a0b8e44d3923c1dcdf6bdaafbb8. H264 1080x1920 30fps 691 frames/23.033s; AAC jpn 48kHz elementary ADTS bit-identical SHA256 27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65. Full A/V decode PASS. CTA ROI MAE at 21.8s 35.1538/255; caption ROI max 0.6177/255 in four samples.
- Local seven tests PASS, 10 genre configs PASS, synthetic 23.1s A/V smoke 693 frames PASS. GitHub CI uses synthetic media only, no private MP4 upload. 16-panel storyboard and research summaries reviewed; original v33 MP4 and full research transcripts unavailable. Japanese independent ASR/caption semantics, rights, phone, staff approval and Actions billing unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; no merge, paid service or auto-post.

## cycle1150 review-only checkpoint (2026-11-02 JST)
- Stacked on unmerged PR #550 (cycle1148), separate from concurrent PR #549 (cycle1217). New improvement is a proof-first result badge during 0.12–1.50s, not another CTA/text deghosting or audio mastering change. Displays a fictional and checked `46 + 29 = 75` in audited opening-panel ROI x52..896 y1305..1387, below the robot and above captions y>=1480.
- Local private review MP4 SHA256 `7a29934c65dc0768ce97130e17321f3e0cc61204dcf7c63982974e59e66cb4c8`; source `e0015a1bf632a9676cef3af8073f939edc766ea92841c14d6df30af23134356e`. H264 1080x1920 30fps 691 frames/23.033333s, Japanese AAC 48kHz elementary ADTS bit-identical SHA256 `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`. Full A/V decode PASS; 40 changed hook frames, none after 1.6s; all-frame sampled caption ROI max MAE 0.7611/255.
- Local 10 tests and synthetic 2-second/60-frame A/V render/decode PASS. GitHub CI uses synthetic media only. 10-genre configurable accent/proof, source hash pin, arithmetic, manual posting, review-only and caption-region checks. User 16-panel storyboard directly inspected; accessible research summaries consulted, original v33 MP4/full research transcripts unavailable.
- Independent Japanese ASR/caption meaning/timing, rights, smartphone playback, employee approval, reference quality parity and actual Actions billing unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, automatic posting, paid service or private MP4 commit.


## cycle1152 review-only checkpoint (2026-11-02 JST)
- Stacked on unmerged cycle1150 PR #552, not main; parallel cycle1219 PR #551 untouched. Added simultaneous BEFORE/AFTER clarity cards at 8.75–10.85s, distinct from cycle1150 proof-first hook and cycle1219 silence-tail pacing. Initial overlapping legacy panel corrected with opaque footer; protected captions y>=1280.
- Private source cycle1150 SHA256 `7a29934c65dc0768ce97130e17321f3e0cc61204dcf7c63982974e59e66cb4c8`; local review output SHA256 `e97b3ca09192cf8d7b80c0c55590b1a51b0b547867e0e8630ab9cedaae480b6c`. H264 1080x1920 30fps 691 frames 23.033s, AAC48kHz ADTS SHA256 identical `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`. Full A/V decode PASS; 62 changed frames, all-frame sampled caption max MAE 0.865/255; 8 chapters nonzero audio RMS, NOT semantic ASR proof.
- Local 11 tests and 2s synthetic full A/V smoke PASS. CI tests synthetic data only; real MP4 remains in private ChatGPT attachment. Ten genre palettes tested, only AI full MP4 generated. Research summaries and original user 16-panel storyboard inspected; full research chats/original v33 MP4 inaccessible. No verified rights, phone playback, staff approval, ASR or Actions billing. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; no merge, paid services or posting.


## Cycle1156 review-only checkpoint (2026-11-02)
- Unmerged branch `quality/cycle1156-source-proof` stacks on `quality/cycle1154-problem-visual`; not a recovered v33 engine.
- Adds `quality/cycle1156/proof_story.py`, 10-genre/rights fail-closed unit tests, and synthetic A/V workflow. Scene 05's 11.55–14.35s shows fictional source→formula→result; arithmetic 46+29=75.
- Local private MP4 SHA256 `855509adc699189b8b5b7391b2b323a5624e9eedec94ac33ab7f092f7a016f91`; 23.033333s/691 frames H264/AAC; full decode PASS; audio packets bit-identical to cycle1154; local 11 tests and synthetic smoke PASS. Public repo contains NO source or output MP4.
- Independent Japanese ASR/subtitle semantics, rights, original v33 MP4, smartphone playback, employee approval, and actual Actions billing remain unverified. HUMAN_REVIEW/PUBLICATION_NOT_APPROVED; no merge or posting.

## cycle1162 review-only efficient encode (2026-11-03 JST)
- Stacked on unmerged PR #561 (cycle1160), parallel PRs untouched. Main verified 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Local real MP4: 1080x1920 H264 30fps 691 frames / 23.033s; 9,281,386 → 4,489,912 bytes (51.62% smaller); full SSIM 0.997425, caption ROI SSIM 0.997679, AAC ADTS bit-identical, full A/V decode PASS.
- Output SHA256 83895018e312dbb1e01b6b8c3ad603f0160aebeff46d515d3dfe656f4d19d614; source SHA256 9fbae3325136e0da41e7b8fe55c1f5c816d296c3dd9b2d781d4b06271e762026. Private MP4 only in ChatGPT, NOT in GitHub.
- New quality/cycle1162/efficient_encode.py and tests; local 8 unit tests and 2s synthetic A/V smoke PASS. GitHub Actions synthetic-only, not the private MP4. See quality/cycle1162/README.md for reproduction/limits.
- Directly inspected 16-panel storyboard, research summaries consulted; original v33 MP4/full research chats unavailable. Spoken Japanese semantic sync, rights, employee approval, smartphone playback and actual billing unverified. HUMAN_REVIEW/PUBLICATION_NOT_APPROVED; no merge, paid services, or posting.
