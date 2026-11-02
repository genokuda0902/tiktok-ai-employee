# cycle1235 — result focus cue (HUMAN REVIEW ONLY)

This cycle follows cycle1233 dark-slide compression (PR #568). Distinct change:
an animated, fade-in/out teal focus ring around the **verified 44 result**
in chapter 3 (6.25–8.05s, rect 510,970,180,80). The overlay never touches
the Japanese narration card, subtitle/footer, or audio.

The offline renderer uses Pillow + FFmpeg, supports 10 named genre palettes,
requires an explicitly reviewed ROI/time interval, and rejects coordinates
overlapping subtitle/footer. This is a visual attention cue, not ASR.

Local real MP4: 22.237s, 1080x1920, 30fps, 667 frames, 8 chapters;
H264/AAC, original AAC ADTS hash identical, full decode PASS.
10 unit tests and 45-frame synthetic smoke PASS. The full real MP4 remains
local; GitHub CI uses synthetic media only.

**Unverified:** independent Japanese ASR, semantic/timing match of burned-in
subtitles, v33 reference video direct comparison, smartphone playback, asset
rights, employee approval, GitHub Actions billing. 10 genres are implemented
but only the AI-work sample was actually rendered.

No paid service, no auto-post, no merge, no public upload of private media.
PUBLICATION_NOT_APPROVED.
