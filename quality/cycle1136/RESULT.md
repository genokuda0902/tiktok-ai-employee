# cycle1136 verified local QA — 2026-11-02 JST

- Previous cycle1134 source SHA256 `8f409be877ff1bd145a01edc2e8c268f6683e4f0df2f7df7351d4caabdf76d15`; new review-only MP4 SHA256 `fea134e081c44363eb1bf3f8aecac57c4da4ed074efaffaee317eefcec379687`.
- Distinct from previous proportional proof bars: **seven left-to-right 8-frame (0.267s) content-only scene wipes** at frames [87, 174, 256, 342, 429, 520, 608]; 32px moving feather. Full-image dissolves were prototyped but rejected after visual inspection due to double text ghosting; spatial wipes are the final output.
- Local MP4 H264 1080x1920/30fps, 691 frames, 23.033s; AAC jpn 48kHz stream copied; full A/V decode PASS; no soft subtitle stream.
- Source/output AAC ADTS SHA256 identical `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`; Japanese speech content and caption semantic match **not** independently checked.
- Cut contrast MAE per cut [85.46, 105.458, 93.726, 106.861, 97.325, 73.05, 102.148] (160px ROI proxy, not aesthetic rating). Sampled 30 frames across boundaries; subtitle area max mean pixel difference 0.749/255; top header max 1.122/255. Video re-encoded so small differences expected.
- Nine local tests PASS; synthetic render/decode PASS; 10 genre safety configurations checked, only AI/Excel actual MP4 generated. CI separately tests synthetic media only.
- User's 16-panel storyboard directly inspected in Library. Accessible past TikTok market/research summaries consulted; original research chat full text and v33 original MP4 inaccessible. Storyboard 16/36s vs current 8/23s, no claim of parity.
- Commercial source rights, smartphone real playback, Japanese independent ASR/word alignment, human/employee approval, GitHub Actions billing NOT VERIFIED. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No paid service, merge, auto-post, or private media commit.
