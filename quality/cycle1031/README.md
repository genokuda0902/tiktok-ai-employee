# cycle1031 — Clean CJK scene headlines (review-only)

Previous cycle1029 emphasized the final three-step CTA. This cycle fixes a different, visible quality defect: multiple/cropped headings competing in scenes 2–8. One opaque, high-contrast Japanese title band replaces the upper headline region, while leaving the main UI demonstration and bottom burned subtitles in place. Scene 1 is intentionally unchanged.

## Local actual-MP4 QA (22.5 s, 1080×1920, 30 fps)
- Source: cycle1029 review-only MP4, inherited 8 chapters and Japanese AAC
- 675 video frames; H.264; AAC 48 kHz; full video/audio decode PASS
- AAC ADTS bitstream SHA-256 identical before/after
- 8 scene samples: caption-safe ROI maximum MAE **0.736 / 255**
- Header ROI changed in scenes 2–8: minimum MAE **34.914 / 255**
- First-scene header ROI MAE **0.398 / 255**
- Local unit tests **11/11 PASS**
- Actual review MP4 is delivered separately in the conversation, not committed to GitHub. GitHub Actions tests **synthetic material only**.

## Shared engine
Ten genre color presets: ai_work, trivia, cooking, beauty, money, health, travel, product, story, work_skills. Scene timing/title strings are template-specific; other genres require new validated scene metadata. Header overlay explicitly refuses other resolutions and protects the caption area.

## Limitations and gates
Original v33 reference video unavailable. Prior TikTok market/video research was consulted via accessible summaries, not original complete source. Independent Japanese ASR, spoken-text/caption semantic sync, original media commercial rights, phone playback, employee approval, retention impact, and actual Actions billing are **NOT VERIFIED**. Existing media is review-only and not cleared for posting.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, paid services, auto-post, or public release. Employee review followed by manual posting only.

## Local command
python quality/cycle1031/code/clean_headers.py input.mp4 output.mp4 --genre ai_work
