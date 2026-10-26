# cycle862 — verified local QA (2026-10-26 JST)

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

- Baseline cycle861 MP4 SHA256: `bfc5b31ab0a53eb69a57b5b90915254a409a670d6ba2445262517c52365780e3`.
- New cycle862 MP4 SHA256: `82e9f547fb28e79ea71c5021576328e91301635d6a656e7c924d033fdcb708d2`.
- Frame range: **631–690** (60 frames, 21.033–23.033s). New actionable three-step outro with genuine old fictional Calc/Writer footage inset. No new recordings.
- Video: 1080×1920 H264 30fps **691 frames**, 23.033s. Audio: inherited AAC 48kHz; original/new ADTS SHA256 both `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- **12/12 local tests PASS**, **8/8 media QA checks PASS**, full A/V decode PASS.
- Edited region sampled mean pixel differences: **68.485 / 67.491 / 74.422**; subtitle region (y1490–1840) **0.254 / 0.366 / 0.357**; outside scene **0.525** (minor encoding differences).
- CI scope: synthetic-only tests, **not** private video. Completed MP4 is attached to the private ChatGPT review conversation, not GitHub.
- Open items: original v33 MP4 unavailable, research chats full text unavailable, independent Japanese ASR/naturalness and semantic caption timing, source publication rights, mobile playback, employee approval, audience retention and GitHub Actions billing unverified.