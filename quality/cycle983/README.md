# cycle983 — shadow-detail recovery (review only)

Base: cycle981 Draft PR #382, private local video SHA256 `c3cbec8278acde8e362f80153ef82006ec3e2050592cd440a965c5acb09f2319`. Parallel cycle982 PR #383 introduces Calc GUI footage and is not repeated or merged.

**Distinct change:** local luminance-only shadow recovery in upper artwork y=150..1180 using a bounded YUV luma LUT. Protect white UI cards/highlights, all caption pixels below y=1180 from intentional edits, and copy the AAC elementary stream without re-encoding. No sharpening, new wipes, or scene timing changes. All eight scenes use one shared renderer. 10 genre IDs are defined; unreviewed real-video layouts fail closed. Only `ai_work` has a checked real MP4.

Local QA of 23.033s, 1080x1920, 30fps, 691-frame output: full A/V decode PASS; AAC ADTS SHA256 identical; dark source artwork pixels Y 25..90 mean Y **51.08 → 67.10** (+16.02/255, technical luminance only); highlight mean absolute Y difference 0.389/255; protected caption ROI (y>=1230, all 691 frames, downsampled) maximum MAE 0.479/255 from re-encoding. 12 unit tests pass. No human perception quality percentage is claimed.

Only local review MP4 and images are available through the ChatGPT conversation, **not committed to public GitHub**. CI runs a synthetic 1080x1920 H264/AAC render and decode. Prior research accessible in summaries emphasizes immediate visual hooks, concise purposeful scene changes, Japanese narration and subtitle readability. User-provided v33 original is unavailable; a 16-frame storyboard summary was previously referenced but original was not recovered.

Unverified: independent Japanese ASR and semantic subtitle timing; original v33 comparison; footage/commercial usage rights; smartphone playback; employee approval; GitHub Actions billing. Zero-cost intent does not prove actual Actions charges are zero.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, posting, auto-posting, source-media upload, purchases, or external contracts.
