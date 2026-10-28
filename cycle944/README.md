# cycle944 — Japanese voice-active caption visibility guard

Different from cycle943's 3-step review-item focus scan: detect short caption fade/dimming gaps during Japanese voice activity and restore the already-existing caption from an adjacent legible frame. No words are generated. Existing 1080x1920 video was locally re-encoded; AAC audio was copied bit-for-bit.

Private source cycle943 SHA256: 100b913c4a59748f511587d33873d6cd2a4bc9199bae556fca2d09f20b3764ab
Private output cycle944 SHA256: 1ce2fe9e1a0c65230b50dcc69c3bc6bf2fd3962ca3210ef95d47db99c4c3ebae

Local QA: full A/V decode PASS; H264 1080x1920 30fps 691 frames / 23.033s; AAC mono 48kHz bitstream identical; 16 caption frames improved, mean bright-text pixel fraction 0.0001 to 0.0964 on changed frames; max measured header MAE 1.426 due to video re-encode; 11 local tests PASS. 10 genre presets are configured and unit-tested, but only AI productivity was rendered as a complete MP4.

Research basis: accessible previous-cycle summaries of TikTok market/video research and the user's prior 16-panel storyboard description. Original v33 MP4 and complete research transcripts were not accessible for direct comparison.

Unverified: independent Japanese ASR, caption semantics, subjective listening/reading quality, commercial rights of inherited material, smartphone playback, employee approval, actual Actions billing. GitHub CI tests source and synthetic frames only, not private MP4.

No automatic posting, private-media upload, paid service, merge, or publication. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Employee approval before manual posting.

Local tests: python -m unittest discover -s cycle944/tests -v
Local render: python cycle944/src/caption_voice_guard.py --source SOURCE.mp4 --output OUT.mp4 --report report.json
