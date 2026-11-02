# cycle1134 — proportional evidence bars, private review

2026-11-02 JST. Independent cycle based on cycle1132 (original non-musical SFX). The new 14.30–17.30s scene06 animation fills three micro-bars inside existing proof cards, without obscuring values or subtitles. Evidence: 12+16+18=46, 8+9+12=29, 46+29=75. All bars share denominator 75; sequencing 0.15–2.10s into scene.

## Source research and access
- Read accessible prior summaries of TikTok市場分析/TikTok動画研究: strong hook, short scenes, real proof, Before/After, readable Japanese captions, manual posting after human approval. Full task/chat transcripts inaccessible.
- Directly viewed user-supplied ChatGPT×Excel時短術16コマ絵コンテ.png in file Library: robot/person, ChatGPT/Excel demos, charts, Before/After and CTA across 16 cuts/~36s. Original v33 MP4 unavailable.
- Verified latest main 18e084c38db0dc55db7dfc0532b9451b1167f2aa; read PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, existing cycle1132 code and prior PR #533. Other open PRs (including parallel cycle1201) left untouched.

## Real MP4 local QA (not in repository)
- Input private MP4 SHA256: 6b72e8ebbec527848b3a85315a23bfa4b0cf4809193ffae8e85af78443189126
- Output private MP4 SHA256: 8f409be877ff1bd145a01edc2e8c268f6683e4f0df2f7df7351d4caabdf76d15
- 1080×1920, 30fps, H.264/AAC Japanese 48kHz, 691 frames, 23.033s; full audio/video decode PASS, zero soft-subtitle streams.
- Original AAC ADTS stream SHA256 identical before and after: 27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65.
- Frame 16.4s: changed bar ROI mean absolute RGB difference 17.391/255; lower caption ROI difference 0.484/255 (codec noise); frame 10.0s unchanged-content ROI difference 0.489/255. Visual compare inspected; bars inside cards.
- Local unit tests 9/9 PASS, ten-genre manifest contract PASS, synthetic 3s H264/AAC render PASS. CI uses synthetic media only; real MP4 locally tested.
- Audio speech meaning vs subtitles not verified by independent Japanese ASR. Phone playback, rights, employee approval and actual Actions billing unverified.

## Remaining difference and next
Reference 16 scenes/~36s vs current 8 scenes/23.033s. Bars improve quantitative comprehension, not cinematic footage, natural character motion, new-topic generation or scene diversity. Next: independent Japanese speech-to-caption semantic/timing QA if a zero-cost offline model is available, plus authorized image-first visual diversity. No public posting, merge, private media commit, external upload or paid API.

Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
