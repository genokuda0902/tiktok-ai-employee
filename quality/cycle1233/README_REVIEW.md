# cycle1233 — Quality-gated dark-slide bitrate optimization

- Previous cycle1231: 1.8% chapter-reset microzoom increased video size 18.39%.
- New change: offline H.264 CRF21 / preset medium / adaptive quantization mode 3 for dark backgrounds, with **two independent FFmpeg SSIM gates** (full frame >= 0.996; central image panel >= 0.992).
- Narration AAC bitstream is copied byte-for-byte; burned-in Japanese narration card, caption line, chapters, and 1080x1920 30fps geometry retained.
- Shared pipeline accepts ten genre identifiers; only AI workflow genre rendered as a complete review MP4.
- CI tests use synthetic media only. User MP4 remains local and is not uploaded to public GitHub.
- No independent Japanese ASR; subtitle semantic/timing verification, v33 reference original comparison, source rights, smartphone device playback and employee approval remain NOT VERIFIED.
- No paid API, no auto-post, no merge. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
