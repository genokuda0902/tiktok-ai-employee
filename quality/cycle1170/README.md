# cycle1170 — proportional fictional-data proof chart (REVIEW ONLY)

This is a reimplementation, not recovered original v33 source. No auto-post, merge, paid API, public private-media upload, or publication approval.

## Change vs cycle1168
- Previous scene 06 had three numeric cards (A46, B29, total75) but no proportional bar chart.
- Reviewed scene 14.50–16.90s, ROI x54/y806/w940/h240: new original animated A/B comparison, data A=12+16+18=46 and B=8+9+12=29, total75. Fictional numbers only.
- Source screenshot, original Japanese AAC and burned-in chapter subtitles retained.
- 10-genre palette support, but only AI-work output was rendered. Other genres require separately reviewed ROI/timing/rights.

## Commands
- python -m unittest discover -s quality/cycle1170/tests -p 'test_*.py' -v
- python quality/cycle1170/tests/ci_smoke.py
- python quality/cycle1170/proof_chart.py --source /private/cycle1168_REVIEW_ONLY.mp4 --output /private/cycle1170_REVIEW_ONLY.mp4 --manifest /private/manifest.review.json --report /private/qa1170.json

Private manifest must include review-only policy, asset_approval, manual_post_only, roi_reviewed, source_sha256, genre, roi, time, fictional_data. Never commit private media, frames, audio or manifests.

## Local verification
- Source SHA256: 4f663f774b0154a366625cd27ff122008c0a023dd74c59fed661264b1b8805d4
- 23.033333 seconds, H.264 1080x1920, 30fps, 691 frames, AAC 48kHz stereo (jpn tag).
- Full A/V decode PASS, AAC ADTS bit-identical, 11/11 local unit tests, 3-second synthetic smoke PASS.
- 691-frame comparison: chart ROI 73 changed frames, mean MAE 35.257/255 during effect, 0.478 outside; caption ROI max MAE 0.619/255; 8/8 chapter caption visual samples.
- Independent Japanese ASR, speech-caption meaning/timing, smartphone playback, original v33 video, rights, employee approval and actual Actions billing NOT VERIFIED.

## Research/reference
Consulted accessible past TikTok市場分析/TikTok動画研究 summaries: first-1.5s hook, real demonstration, Before/After, evidence, readable captions, manual employee posting. Full original chats unavailable. Directly viewed user's 16-panel ChatGPT×Excel時短術 storyboard (~36 seconds). Original v33 MP4 unavailable. Current 8-scene/23s output still lacks cinematic character footage and 16-scene variety.

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. CI tests synthetic media only.