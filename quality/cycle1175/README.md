# cycle1175 — BEFORE → AFTER comparison focus

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**

This is a distinct improvement from cycle1173 caption sharpening. Scene06 now
uses two sequential soft glows on the existing BEFORE and AFTER cards, with
alpha fade-in/out. No overlay fill covers the card text. The original subtitle
region begins below y=1320 and is never intentionally overlaid.

Shared Python renderer supports 10 palette presets. Only AI genre full MP4
was produced. Local 12/12 tests PASS; synthetic 4-second 1080×1920/30fps
H264+AAC end-to-end generation and full decode PASS. Actual private 22.5-second
675-frame MP4 was generated and verified locally, **not uploaded to GitHub**.
Audio AAC ADTS SHA256 unchanged from cycle1173:
8f67ed7ae02482d581c375401329004c9e06c6cc282fa03d34c93ec6f200c928.

Unverified: independent Japanese ASR, semantic subtitle sync, original
reference-v33 direct comparison, commercial asset rights, smartphone playback,
employee approval, and actual Actions billing. No merge, auto-post, or paid service.
