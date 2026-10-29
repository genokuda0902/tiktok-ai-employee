# cycle960 — UI-safe caption reflow (review only)

## Difference from cycle959
Cycle959 enlarged all eight Japanese subtitles. Cycle960 reflows the **same exact text** into an assumed mobile UI safe region, reserving right-side actions and bottom controls. Prior source caption bounds reached x1048 / y1720. New panel ends at x883 / y1618, with glyphs x<=858 / y<=1640. 10 color presets are unit-tested; real rendering is SHA-locked to the reviewed AI-work source.

## Local real-media QA
Source cycle959 SHA256: `37d9333effd1fd7702581be447c0820a9e44a7f5dedd1f19ce4fef4f316d51e9`.
Local cycle960 MP4: 23.033333s, 691 frames, H.264 1080x1920 30fps, AAC 48kHz mono Japanese tag. Full audio+video decode PASS; AAC ADTS SHA unchanged `0045ddfb9eb47f798aa6ae3a465f885409dab58ce27ad0fa1479901becddc57d`. 8 scene samples changed only lower region, outside-region mean absolute RGB difference 1.13–1.28 due to re-encoding. 7/7 local unit tests PASS. Real MP4 remains a private ChatGPT artifact, not pushed to public GitHub.

## QA limitations
The safe area is a conservative assumption, not official TikTok UI geometry or a real-phone test. No independent Japanese ASR, subtitle-semantic/timing verification, original v33 reference comparison, commercial source-rights verification, employee approval, or Actions billing verification. Research/16-cut storyboard referenced only from available summaries. CI uses synthetic geometry/text tests, **not real video**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, paid service, or release.
