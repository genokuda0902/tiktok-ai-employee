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

## 2026-10-31 cycle1064 review-only checkpoint (unmerged Draft PR #465)
- Base: open Draft PR #464 (cycle1062); latest main checked 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Branch: quality/cycle1064-cinematic-ui-20261031. PR: https://github.com/genokuda0902/tiktok-ai-employee/pull/465
- Distinct improvement: static, sanitized fictional LibreOffice Calc screenshot gets an original eased 8.5% Ken Burns push-in, depth and three-step emphasis on 82 frames (5.800–8.533s). This is NOT live UI recording; original v33 engine NOT recovered.
- Actual local review MP4 SHA-256 87ea4a7995f726edcb12739a7b6a6ce08bc13ce3ef5ffe61cf7cd8ca01581bfd. 23.033s / 691 frames / H264 1080x1920 30fps / inherited Japanese AAC 48kHz. Full decode PASS, ADTS audio bitstream identical, protected caption ROI max mean pixel delta 0.5328/255, exactly 82 changed frames. Seven local unit tests and synthetic 0.5s smoke PASS. GitHub CI status must be checked on final head; CI does NOT verify private full MP4.
- Research: past accessible summaries of TikTok市場分析/TikTok動画研究 and original 16-panel user storyboard directly inspected; full research transcripts and v33 original MP4 unavailable this run. Reference still has richer cinematic human/robot and real UI operations.
- Still blocked for publication: independent spoken Japanese transcription/semantic subtitle sync (especially 20.300s), asset/voice release rights, phone playback, employee approval, actual Actions billing. No merge, no automatic posting, no paid services, no public upload of private media. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.


## Verified development checkpoint — cycle1074 (2026-11-01 JST, REVIEW ONLY)
- Stacked Draft PR: https://github.com/genokuda0902/tiktok-ai-employee/pull/475 (base: unmerged cycle1072 PR #473; **not main**).
- Added reusable 10-genre vector task-stack animation to scene 02, 2.900–5.800s, avoiding subtitle region. Code: quality/cycle1074/task_stack.py; 14 local unit tests PASS. Prior cycle1072 animated only the opening hook; concurrent PR #474 addresses caption zoom separately.
- Local **private** MP4 produced, 23.033333s/691 frames/H264 1080x1920 30fps/AAC 48kHz. Full decode PASS; original AAC ADTS bitstream identical. Max caption-region mean pixel difference 1.2623/255; target region 87-frame mean difference 17.63018/255. The actual MP4 and extracted audio are NOT uploaded to GitHub.
- GitHub Actions workflow tests a synthetic 6s H264/AAC video, not the actual private MP4. Check CI status in PR before asserting success.
- Original v33 reference MP4 and original generation source not available in this run. Available 16-panel storyboard directly inspected. Prior TikTok market/video research summaries consulted; full source chats unavailable. Independent Japanese ASR and semantic subtitle match, smartphone playback, release rights and employee approval remain **UNVERIFIED**.
- No merge, auto-post, public release, payment, or production deployment. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.


## cycle1076 review checkpoint (2026-11-01 JST; NOT PUBLICATION APPROVED)
- Independent stacked branch from unmerged cycle1074 PR #475; scene 07 only (frames 520–608, 17.333–20.300s). Original vector gutter checkmarks sequentially guide purpose / condition / output format on a **static** real Writer screenshot; not a recording of actual input.
- Reusable 10-genre palette code: `quality/cycle1076/writer_review.py`; 18 local unit tests PASS; original/private MP4 never committed. Source hash fail-closed; existing narration and burned-in subtitles intentionally unchanged.
- Private local MP4: 23.033333s / 691 frames / 1080x1920 30fps H.264 / AAC 48kHz stereo. Source SHA256 `1625df39f27e63dbb5c40ceeeff09b3be7949ad485d6a4455bb2832db0ca24f8`; output SHA256 `baf49198026575d770ae43fb1952278fe2afac5e963920fcbbe146536187ccee`. Full A/V decode PASS; ADTS audio bit-identical; subtitle protected region max mean pixel difference 1.2637/255; target region mean 10.0192/255.
- GitHub CI only tests **synthetic 21s** video, not actual 23s private MP4. Verify workflow run conclusion before calling CI successful.
- Research summaries available, full TikTok市場分析/TikTok動画研究 chats and original v33 reference MP4 not accessible. Reference 16-panel storyboard still materially richer than 8-scene current video. Independent Japanese ASR/semantic subtitle check, publication rights, smartphone playback, employee approval, actual Actions billing remain UNVERIFIED. No merge, paid service, auto-post, or public media upload.


## cycle1078 verified review checkpoint (2026-11-01 JST; NOT APPROVED FOR POSTING)
- Stacked branch on unmerged cycle1076 PR #477; scene 03 (5.800–8.533s / 82 frames) now contains an actual sanitized LibreOffice Calc Xvfb/x11grab operation recording instead of a static screenshot. Formula selections B5/C5, then =B5+C5 yields fictional total 75. This is a genuine manually scripted UI capture, **not AI-controlled operation**.
- Private review MP4 SHA256 d9ffee665fbc233fb0ead5c501088f69a08ac931521a4490fb56b5ea26d65de1; 23.033333s / 691 frames / 1080x1920 30fps H264 / AAC 48kHz. Full A/V decode PASS; original AAC ADTS byte-identical. All 691 frames protected caption ROI max mean difference 0.4667/255; changed scene 03 ROI mean 47.127–48.006/255 at three checkpoints.
- Reusable ten-genre capture compositing module and twelve local tests PASS; synthetic nine-second smoke PASS. Actual MP4 and raw capture remain local, never committed. Source/capture SHA256 fail closed.
- Prior TikTok市場分析/TikTok動画研究 summaries consulted; 16-panel storyboard goal known, original v33 MP4 and full research transcripts unavailable. Current 8-scene/23s remains below reference 16-panel/~36s cinematic variety.
- Independent Japanese ASR and semantic subtitle match, phone playback, media/audio rights, employee review, and Actions billing remain UNVERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, no paid services, no auto-post.


## cycle1080 review-only checkpoint (2026-11-01 JST, NOT APPROVED)
- Source branch: stacked on open PR #480 (cycle1078), not main. Draft PR #482 https://github.com/genokuda0902/tiktok-ai-employee/pull/482 ; main checked at 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Concurrent PRs unchanged.
- Different improvement: scene 06 frames 429–519 (14.300–17.333s), replacing washed-out mock audit with animated 3-beat **fictional illustrative** B-only 46 → B+C 75 correction, including a locally extracted still of actual Calc demo in scene03. This is not a claim of actual AI error, true speedup, or recovered v33 engine. 10-genre palette and SHA256 fail-closed private input; no media committed.
- Local actual MP4 SHA256 ac53a00467f4a75297b80c2d32ccc310a11aa5fd0065e487e08b444ae1502436; source SHA256 d9ffee665fbc233fb0ead5c501088f69a08ac931521a4490fb56b5ea26d65de1. 23.033333s, 691 frames, 1080x1920 30fps H264 / AAC 48kHz. Full A/V decode PASS; AAC ADTS SHA256 identical (76801539a721f7d968b5a8bf725fd056ab00de5a74bd09caf50112993c4aa2f8). Exactly 91 changed frames (global mean >1.5/255); caption ROI max mean pixel difference 0.48145/255; target scene mean difference 71.4123/255; outside scene mean 0.2404/255. Twelve local tests and synthetic 18s smoke PASS.
- Research: directly inspected user's Library `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels/~36s) and accessible TikTok市場分析/TikTok動画研究 summaries; full original chats and v33 MP4 inaccessible. Current 8-scene/23s still lacks cinematic imagery, variety and full ChatGPT interaction.
- Unverified: independent Japanese ASR/meaning/timing alignment for eight subtitles (especially 20.300s+), smartphone playback, media/voice publication rights, employee approval, GitHub Actions actual billing. CI validates only synthetic video; check actual final workflow run conclusion separately. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid services, public private-media upload or auto-post.


## Cycle1092 review checkpoint (2026-11-01 JST; branch-only, unmerged)
- Branch: \`quality/cycle1092-stable-total-20261101\`, stacked on unmerged cycle1090 PR #492, **not** main. Do not merge automatically.
- Scene06 truth defect: 46 + 29 displayed transient wrong totals 13 at ~15.7s and 71 at ~16.0s. New \`quality/cycle1092/stable_total_guard.py\` masks the false intermediate totals, shows 確認中 then source-calculated 75. Ten genre presets and synthetic-only safety gate.
- Source review MP4 pinned SHA256 \`0a0a653ac06a96a5445b3af138ad5018642b913096ff12123f080d3b78b694e7\`; original source media is not committed.
- Local 6 unittest cases PASS, 3s synthetic full A/V smoke PASS. Completed local MP4 SHA256 \`8cd93dadba53243970d18265c404cd556af203385b3532c370935e150cb51306\`; full CI status and independent Japanese ASR not yet verified at this checkpoint.
- Research summaries and prior v33 inspection retained; full original research chats and reference MP4 original were not retrieved in this run. Publication rights, phone QA, subtitle semantic verification and employee approval remain unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**; manual posting only.

## 2026-11-01 — cycle1098 review checkpoint (stacked draft, not main)
- Parent open PR #497 (cycle1096), separate quality/cycle1098/writer spotlight patch. Real private MP4 SHA256 `71be71788fd58ffdf17862d61c4984c6ad5637ea44d4fe277b59748dd4f82cea`; source cycle1096 SHA256 `53bb7306b829054c0379d46cb6422f164f7be54153af67637d1b549331686831`.
- Three successive thin highlights on fictional Writer purpose/conditions/format rows at 17.5–19.9s. 10 local unit tests, full private 23.033s A/V decode PASS; inherited AAC bitstream unchanged; independent Japanese ASR NOT VERIFIED. Synthetic-only GitHub CI; final run status tracked in PR.
- Current 8-scene reimplementation is NOT v33 equivalent; rights, human review, phone playback, publication approval and billing unverified. No merge or auto-post. See `quality/cycle1098/README.md`.

## 2026-11-01 — cycle1100 review-only Calc formula focus (stacked on open PR #499)
- Source: cycle1098 local MP4 SHA256 `71be71788fd58ffdf17862d61c4984c6ad5637ea44d4fe277b59748dd4f82cea`. Local cycle1100 output SHA256 `739599eafb7b2150ade1aa79aeef1dbd4f0390990c6236c33a4cc7ebc8754f54` (private ChatGPT review artifact; NOT committed).
- Changed chapter03 frames 195–248, formula `=SUM(C2:C4)` then fictional 46/29 totals. 14 unit tests, full 23.033s 691-frame A/V decode, H264 1080x1920/30fps, AAC 48kHz ADTS bit-identical (spoken Japanese per prior review; stream metadata `und`; no independent ASR). All-frame quarter-resolution subtitle protection max delta 0.8928/255. Ten palettes tested; one genre rendered.
- Original 16-panel storyboard inspected; v33 original MP4 and full research chats inaccessible this run. Independent ASR/semantic subtitle sync, commercial rights, phone playback, employee approval, Actions charges NOT VERIFIED. GitHub CI tests synthetic 9-second A/V, not private MP4.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid services, confidential media upload, or automatic posting. See `quality/cycle1100/README.md`.

## 2026-11-01 cycle1110 review-only checkpoint
- Base PR #509; draft PR #512; no merge or publication.
- Exact source, test and manifest saved under quality/cycle1110; offline 11 unit tests, ten-genre overlay preset checks, synthetic CI.
- Local review-only MP4 SHA256 bcf5b872effca785199589caa45f825f6a38c96f68263388b0fe50b3f3f6aa3b, source SHA256 40ff844987eec893748b5ab75264e2b1f37ab0ab08b59a0e67ab46b29b4e77c2; 691 frames, H264 1080x1920 30fps AAC 48kHz, full decode and audio stream identity PASS. Private MP4 not committed.
- Difference: 8.85–10.95s scene4 fictional prompt Before/After cue, no productivity claim; caption y>=1280 preserved.
- User 16-panel storyboard directly inspected; full research transcripts and original v33 MP4 not accessed. No ASR semantic check, rights approval, device playback, or employee approval. PUBLICATION_NOT_APPROVED.
