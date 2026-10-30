# cycle1027 — shadow-detail lift, review only

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**

## Distinct from cycle1025
cycle1025 increased visual beats from 8 to 14 with six UI close-ups.
cycle1027 instead applies highlight-preserving shadow lift to the central UI
(y=150..1389) while leaving the top status area and burned subtitle area
unprocessed. No new image, external asset, or new voice is introduced.

## Local finished MP4 (not uploaded to public GitHub)
- 22.500s, H.264 1080x1920 30fps, 675 frames, 8 chapters
- Japanese-tagged AAC 48kHz: source/output payload SHA256 identical
- Full audio/video decode: PASS
- 14 sampled timestamps: central dark pixels lifted +14.919 gray levels on average;
  bright pixels average absolute change 2.533 levels; protected caption region
  maximum mean absolute difference 0.416/255 (codec drift)
- 5 unit tests: PASS. The GitHub CI renders **synthetic** 2s media only.
- Actual finished MP4 and contact sheet are shared as conversation files.

## References and limitations
Accessible earlier research summary: first 1–1.5s hook, ~15–25s, readable
Japanese captions, UI demonstrations, Before/After and employee review.
User's 16-panel ChatGPT×Excel storyboard and prior cycle1025 are used as
design context. Original reference v33 MP4 not directly accessible.
Only ai_work is tested on the finished 22.5s video; all ten genre presets
have unit tests. Independent Japanese ASR, semantic caption sync, commercial
rights of inherited media, smartphone playback, employee approval and
GitHub Actions billing are not verified.

No paid service, new contract, unapproved merge or automatic publication.
Only employee-approved manual posting is permitted.
