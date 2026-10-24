# cycle809 — simulated goal UI (REVIEW ONLY)

2026-10-24 JST. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. This is a reimplementation, NOT original v33 source. No merging, publishing, posting, billing or private data.

## Research, reference and repo provenance
- Current main SHA: 18e084c38db0dc55db7dfc0532b9451b1167f2aa. Read PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md. Reviewed unmerged PR #110 and parallel #109/#107.
- TikTok市場分析 and TikTok動画研究: consulted available prior research summaries (first 1.5s hook, short scenes, one idea/video, real demos and Before/After, safe Japanese captions). Full task/chat transcripts unavailable.
- User's 16-panel AI時短ラボ storyboard: previous accessible summaries show office/Excel demonstration and cinematic tech visuals; original v33 MP4 not accessible during this run. No reference-parity claim.
- Local source cycle808 MP4 SHA256: c3ed27226338159ec6a537bbdab4740a79087d50be71f3a8000117561bb5ec2a.

## Change vs cycle808
Scene 2, frames 90–178 (3.000–5.967s): static goal card becomes simulated goal-entry UI with typing, cursor motion and save feedback. UI visibly labeled 架空UI / 架空データ・操作イメージ. Fictional example 月間成約 20件; no actual application, company metrics, logo or PII. Preserves inherited caption and original AAC elementary audio bit-for-bit. Ten-genre scenario contract, one sales_business MP4 rendered.

## Reproduce
Install Pillow==11.3.0, ffmpeg, ffprobe and Noto CJK Bold font (override CYCLE809_FONT).
Run: python -m unittest discover -s quality/cycle809 -p 'test_*.py' -v
Run: python quality/cycle809/goal_ui_demo.py --source cycle808_ACTION_BEATS_REVIEW_ONLY.mp4 --output review_output/cycle809_GOAL_UI_REVIEW_ONLY.mp4
Run: ffmpeg -v error -xerror -i review_output/cycle809_GOAL_UI_REVIEW_ONLY.mp4 -f null -
Do NOT commit source or local output MP4 to public repo without rights review.

## Verified local QA
12/12 tests PASS; 1080x1920, 30fps, 718 frames, 23.933333s, H.264 + AAC 48kHz, full A/V decode PASS.
Output MP4 SHA256: 48c6bd1b0b3770311e00cec62293dd3e570431bdd0ea44b2c89bb71e29bbac73
Preserved AAC ADTS SHA256: d9f3e2c986b32eda17ee64c3c89fc2ec2d428121715076c6d686edde85cd9093
Speech content, naturalness, caption semantic alignment, voice/asset rights, original v33 direct comparison, smartphone playback and employee approval remain UNVERIFIED.
CI only uses synthetic sine-tone media, NOT the rights-unapproved Japanese review video.
Next: independent Japanese ASR/caption QA; licensed image-first visuals and real sanitized operation demo; reference v33 direct comparison. Manual employee-approved posting only.
