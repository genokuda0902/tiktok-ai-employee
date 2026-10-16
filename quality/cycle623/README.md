# Cycle 623 — full-screen synthetic spreadsheet proof (review only)

Baseline: cycle622 MP4. Changed video region: 10.5–16.5 s.
Improvement: replace tiny screenshots and overlay cards with a large synthetic
spreadsheet sequence: highlighted B2:B5 range → typed =SUM(B2:B5) →
computed 720 → four-bar chart (120,150,200,250). This is NOT an actual Excel
recording, not a recovered v33 renderer, and does not show real AI execution.

Local reproducible renderer, full MP4, side-by-side comparison, tests and
technical QA are provided in the accompanying conversation ZIP. The GitHub
module here verifies shared 10-genre arithmetic, safety bounds and approval
gates; the full rendering implementation is NOT yet in this repository.

Technical QA: 1080x1920, H.264 30fps 605 frames, AAC 44.1kHz stereo,
20.166s; complete ffmpeg decode succeeded. Local renderer unit tests: 10/10.
New Japanese speech: ABSENT. Voice/caption alignment: NOT VERIFIED.
Rights: synthetic segment only; inherited base-video assets not approved.
Publication: NOT_APPROVED; manual posting only after human approval.

Sources reviewed: PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md,
user storyboard, v33 reference video (local comparison), prior cycle622.
Do not merge automatically or publish.
