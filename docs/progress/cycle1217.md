# cycle1217 — 2026-11-05 JST
- Difference from cycle1216: adds a high-contrast focus card during seconds 12–16; previous cycle added an end-of-video action summary.
- Review-only reimplementation; does not reproduce original v33.
- Local artifact: cycle1217_FOCUS_CARD_REVIEW_ONLY.mp4, SHA256 d10e0374f3e9e74d4631d16debd77a1900f134ae27a80b775496c950b891566d, 1080x1920, source cycle1216 local MP4.
- FFmpeg full decode and frame 13 extraction passed locally. Japanese spoken content, caption synchronization, phone playback and licensing remain unverified.
- Original v33 MP4 and full TikTok research chats not accessed. Confidential prototype prohibited. No posting/merge.
- Reproduction: python -m src.review_focus_card SOURCE.mp4 OUTPUT.mp4
- CI status: to be checked. Human review required.
