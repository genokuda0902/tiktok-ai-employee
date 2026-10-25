# cycle832 — full-width image-first layout (review only)

## Actual change from cycle831 editorial branch (#153)
- Increase the main image from 684×910 = 622,440 pixels to 972×1030 = 1,001,160 pixels (**+60.8% area**).
- Remove the narrow STEP/CHECK sidebar; the image now occupies the full horizontal content area.
- Keep the Japanese hook, 8 scene structure, 775 frames, mastered offline narration and 24 timed caption states.
- Place a short per-scene action chip *inside* the image and reserve y=1450–1808 for subtitles.
- Run 10-genre geometry and pixel-level regression checks. New CI should render an actual MP4 and upload it.

## Sources and limitations
- Prior TikTok市場分析 / TikTok動画研究 summaries: 1.5-second hook, image-first, action proof, Before/After, short captions, safe zone. Full original transcripts inaccessible.
- User's ChatGPT×Excel 16-panel storyboard inspected; original v33 MP4 unavailable this run.
- This branch is stacked on unmerged #153 (itself stacked on #150). **Not merged into main**.
- CI uses original procedural fallback art, not the uncommitted local AI photo collage from #153.
- Therefore this is a **layout/composition** improvement, not verified photographic realism or v33 parity.

## Verification and safety
Run `python -m unittest discover -s quality/cycle832 -v` and the GitHub Actions workflow `cycle832-photo-first-japanese.yml`.
The resulting MP4 is **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No paid APIs, posting, auto-merge, customer data, or unapproved assets.
Actual speech recognition, pronunciation, mobile device testing, public-use rights, employee approval, and reference parity remain open.
