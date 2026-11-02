# Cycle1176 result — 2026-11-03 JST

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No posting, merge, paid API, or confidential media upload.

## Delta from cycle1175
- cycle1175 magnified real spreadsheet source regions at 6.16–8.73s.
- cycle1176 repairs the low-contrast/ghosted red review-only disclosure in scene 5 (14.45–17.45s) with a crisp, source-independent high-contrast label: **未承認｜社員確認後に手動投稿**.
- First attempt mistakenly placed a second label above the original (y=1122), creating duplicate warnings; rejected. Corrected panel to y=1290..1432 over the original, with subtitle region y>=1480 protected.
- This is a reusable ten-genre overlay and approval gate, not proof of ten rendered genres.

## Local MP4 QA
- Input: cycle1175_SOURCE_TRUE_UI_LENS_JP_REVIEW_ONLY.mp4 SHA256 9144673657b90a9f732dd0b2ea463e83473a0ea3a2c21a98007592e11e26092c.
- Output: cycle1176_READABLE_APPROVAL_DISCLOSURE_JP_REVIEW_ONLY.mp4 SHA256 4b0ac54f7bf72465d58527c73defc220771d545df9498087c59f426b29585a74.
- H264 1080×1920 / 30fps / 691 frames / 23.033333s / 3,260,116 bytes.
- AAC 48kHz jpn-tagged: ADTS payload bit-identical to source; 8/8 equal-duration audio intervals non-silent. Japanese speech correctness and alignment NOT independently checked.
- Full audio/video decode PASS; unit tests 6/6 PASS; 90 warning-region frames materially changed.
- White-on-dark contrast: 18.19:1 (calculated palette ratio; not a device/visual accessibility certification).
- All 691 frames compared at 1/4 scale for subtitle/footer region y>=1480: mean pixel MAE 0.721/255; maximum frame mean 0.767/255. Difference from re-encoding remains, so pixels are not bit-identical.
- Smartphone playback, original v33 direct comparison, rights and employee approval NOT verified.

## Research and next priority
- Accessible research summaries: hook 0–1.5s, 15–25s, scene purpose, readable Japanese captions, sanitized real UI, Before/After, human review/manual posting.
- User-provided 16-frame / ~36s storyboard was previously inspected; not directly available in this execution. v33 reference MP4 and full market-analysis/video-research conversations not directly available.
- Current review video: 8 scenes / 23.03s, still lacks cinematic people/robot visuals and real-operation scene diversity.
- Next: licensed/offline Japanese ASR and subtitle semantic/timing audit; fail closed until human QA. Never publish or merge without review.
