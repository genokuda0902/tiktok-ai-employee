# cycle961 — source-backed mobile proof reveal (REVIEW ONLY)

2026-10-29 JST. Based on unmerged Draft PR #360 / cycle960, **not** the original v33 generator. No merge, auto-posting or paid service.

## Change vs cycle960
The old 410×310 proof card at x490/y620 was too small in a 9:16 phone preview. This cycle uses a 770×630 card at x155/y520, two timed beats (0.35–1.41s and 1.26–2.34s), a larger crop from the same fictional LibreOffice Calc screen recording at 13.8s, and 48–82px proof numerals. The source shows A=12+16+18=46 and B=8+9+12=29. Do not describe the Calc screen as Excel UI.

The lower Japanese caption/audio-wave area y>=1490 is protected. The original Japanese AAC bitstream is copied unchanged. This is a readability/pacing improvement, not an independent transcription or claim of v33 equivalence.

## Local reproduction (private media never committed)
Input: cycle960 private MP4, SHA256:
5b56fc8b72b984f5fc81397738d06900adaedbe35620de99b3b15f2a25bfcc07

Run with Python 3.11+, Pillow, ffmpeg/ffprobe, Noto CJK fonts:
- python -m pytest -q cycle961/test_mobile_proof_reveal.py
- python cycle961/mobile_proof_reveal.py --source /private/cycle960.mp4 --output /private/cycle961.mp4 --qa /private/render_qa961.json

Local full-media QA additionally used OpenCV and numpy, tested complete video/audio decoding and compared caption pixels. That verifier and detailed QA are in the private ChatGPT review package; CI runs synthetic tests only.

## Measured local result
- MP4 SHA256: 4257fccc11a1e8880eb208a5a50f53a9fb815c35f53069048409da021084344d
- 1080×1920, H.264 30fps, 691 frames, 23.033333s; AAC 48kHz stereo.
- Full A/V decode PASS; source/output ADTS SHA256 equal: 37df7a17744c68dc6952f0778e57ef4ad94c977057a470cd12ea951e8bcb1e27.
- Proof ROI mean pixel changes 91.064 and 87.884/255 at 0.8/1.8s.
- Protected caption region max mean sampled pixel delta 0.486/255; outside edit window max mean sampled delta 1.274/255.
- 21 local synthetic tests PASS. Smartphone playback and human readability preference not independently validated.

## Provenance and gates
Consulted accessible summaries of TikTok市場分析/TikTok動画研究 (strong 0–2s hook, short meaningful cuts, real UI, readable Japanese subtitles, manual review), previous 16-panel ChatGPT×Excel storyboard description, GitHub handoff and v33 recovery notes. Original research chats, 16-panel storyboard image in this run, and original v33 MP4 are not directly accessible. Reference remains 16 panels vs current 8 scenes; cinematic person/robot variety and direct ChatGPT/Excel interaction are still missing.

10 distinct genre policies exist, but only ai_work has reviewed evidence and geometry; nine other genres fail closed. Commercial material rights, independent Japanese ASR/transcript-to-caption semantic/timing alignment, real phone playback, employee approval and actual Actions billing are NOT verified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Private MP4 shared only as ChatGPT review attachment, never committed to public GitHub.
