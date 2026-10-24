# Cycle811 — subtitle safe-area revision (review only)

**Delta vs cycle810:** Previous subtitle box occupied y=1562..1708, overlapping the area normally used for TikTok's description and buttons. Cycle811 moves the three-stage Japanese captions to (x=70..866, y=1140..1500), reserving the right edge (x>=890) and bottom (y>=1540). Adds a slight three-phase photo push-in while preserving the previous Japanese audio bitstream.

- 10-genre portable contract and seven no-dependency CI tests are committed here.
- The **full local renderer, MP4, image assets, and QA JSON are supplied in the conversation ZIP**; they are not committed to GitHub and the CI does **not** render the MP4.
- Local verification: 1080x1920, H.264/30fps, 775 decoded frames, 25.833s, AAC/48kHz inherited Japanese voice; full decode PASS.
- New MP4 SHA-256: `96a71124d1b94b7b6b22ca533e7ab191804ba01278fa1dfe4011b41ebf15d818`
- Estimated caption timing, **not** ASR/forced alignment.
- Photo crops reuse prior ChatGPT-generated material. Photo/source and voice-model rights, real phone playback, and employee approval remain unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No auto-post, no merge, no paid services.
