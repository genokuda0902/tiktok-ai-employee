# cycle775 — brighter results, review only

Date: 2026-10-23 JST. Additional cost: 0 yen.

Source: cycle774 27.343-second local review MP4 (not committed; media rights unverified).
Reimplementation, not recovered original v33 engine. Original v33 MP4 unavailable in this run.
Reviewed user-supplied 16-panel ChatGPT x Excel storyboard, earlier v33 comparison still, and summaries of TikTok market/video research. Full research task transcripts unavailable.

## Change from cycle774
- Replace 10.0–12.8 seconds (84 frames) with a high-contrast bright chart and animated monthly bars.
- Verify synthetic data: 120000 + 150000 + 200000 + 180000 = 650000 yen.
- Use directional scene wipes to prevent ghosted overlaid Japanese text.
- Add ten-genre palette, fail-closed claims/rights/posting validation, and renderer tests.

## Evidence
- Local video: 1080x1920 H.264 30fps, 819 frames, 27.343 seconds, AAC audio inherited unchanged.
- Local output SHA256: d292efd6ddcf48dd26961c169c1cdafd14d46c8f998808a84585146c88ae05ce
- Local unit tests: 22 PASS. Full video/audio decode PASS. PCM audio unchanged.
- RGB difference at 11.8s: 87.27; outside changed scene at 7.5s: 0.171.
- GitHub CI workflow uses synthetic test-tone audio and creates a separate smoke artifact. CI is NOT a test of Japanese voice or rights.
- Full local renderer is src/result_reveal.py; source blob matches the local git hash-object SHA.
- Source baseline and final review MP4 shared outside GitHub with the user; not committed.

## Approval and limitations
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
Inherited audio rights, exact Japanese speech-caption sync, smartphone playback, and reference v33 equivalence are unverified.
No auto-posting, paid subscriptions, or merging. Employee approval and manual posting only.
