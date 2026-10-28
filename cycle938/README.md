# cycle938 — three-beat evidence comparison (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Stacked on unmerged Draft PR #325; not merged into main.

## Distinct change vs cycle937
- cycle937 enlarged a small template and moved the unapproved outro forward to match Japanese captions.
- cycle938 changes **scene06, 14.50–17.40 seconds (frames 435–521)** from a static 17-vs-18 card into three sequential beats: inspect fictional AI draft 17 → inspect fictional source 18 → identify difference 1 and require human judgment.
- "Fictional demo" and "not automatically corrected" labels remain visible. Other scenes and the Japanese caption/audio track are inherited.
- Generic 10-genre presets and tests; **only AI-work rendered to a full MP4**. Other genres require separately approved visual sources.

## Reproduction with authorized local media only
Private source: cycle937_TEMPLATE_MICROCUT_JP_REVIEW_ONLY.mp4, expected SHA256:
9c98d96d8b5596b80b099da98fbc266b2d2b76409a32cfe7dcd9939644a876a0

    python cycle938/src/evidence_progression.py --source /private/cycle937_TEMPLATE_MICROCUT_JP_REVIEW_ONLY.mp4 --output /private/cycle938_EVIDENCE_THREE_BEATS_REVIEW_ONLY.mp4 --tmp /private/cycle938_tmp --genre ai_work --expected-source-sha 9c98d96d8b5596b80b099da98fbc266b2d2b76409a32cfe7dcd9939644a876a0

Requires Python, Pillow, ffmpeg, and free Noto CJK fonts. Fail closed on source SHA mismatch.

## Verified private output (NOT uploaded to public GitHub)
- MP4 SHA256: 189d3869b1326c8743e0cd7c5904da2e217b2c4d8db8a0b0e283de12e5d17a29
- H.264 1080x1920, 30fps, 691 frames / 23.033333 seconds; AAC 48kHz.
- 87/87 edited frames changed; downscaled minimum mean absolute pixel delta 19.862.
- Outside edit max delta 0.422; subtitle band max delta 0.411.
- AAC ADTS bitstream identical; full A/V decode PASS.
- Local renderer tests 14 passed. GitHub CI validates synthetic imagery/code only, not the private finished MP4.
- Independent Japanese ASR/semantic/timing sync, original v33 direct comparison, commercial rights, mobile playback, employee approval, and actual Actions billing are NOT verified.

## Research and safety
Consulted accessible summaries of TikTok市場分析 and TikTok動画研究. Directly inspected user's 16-panel ChatGPT×Excel storyboard in Library. Original v33 MP4 and full research chats inaccessible. Cinematic human/robot scenes and 16-cut story remain unmatched.

No private media, extracted audio, personal data, or secrets committed. No automatic TikTok posting, paid service, contract, or merge. Employee approval must precede manual posting.
