# cycle1163 — scene05 status-strip text repair

**Review only. Publication not approved.** No automatic posting, paid services, merge, or private MP4 upload.

## Distinct change
Cycle1161 animated three repeated-task cards in scene02 (frames 116–164).
This cycle fixes **double-rendered Japanese characters** in scene05 status strip (frames 282–329, 9.4–10.967s). The text remains "目的 → 条件 → 形式 | 架空の入力例"; it is not a new factual claim.

The repair uses a protected-area patch at x90–989, y1255–1293, below the infographic and above the narration card. The main narration captions (y1490–1840) remain untouched. Ten genre color presets share the same implementation; only the AI-work MP4 was rendered.

## Local real-MP4 QA
- Source: cycle1161 actual 22.5-second Japanese review MP4.
- Output: cycle1163_STATUS_TEXT_REPAIR_HUMAN_REVIEW.mp4 (private review attachment, not committed).
- H264, 1080×1920, 30fps, 675 frames, 22.5s: PASS.
- AAC 48kHz, language tag jpn; source/output ADTS payload SHA256 identical: 8f67ed7ae02482d581c375401329004c9e06c6cc282fa03d34c93ec6f200c928.
- Full A/V decode PASS.
- 675-frame caption-region max mean delta: 0.7861/255; outside-scene sampled max 1.3561/255 (re-encoding).
- Status-strip mean difference at modified frames: 25.00–25.51/255; first unmodified frame 330: 1.052/255.
- Local unit tests: 8/8 PASS.

## CI scope
CI uses synthetic H264/AAC test input and checks unit tests, 1080×1920, frame count and full decode. It **does not** verify the private full MP4 or Japanese narration semantics.

## Research and reference
Accessible prior market-analysis/video-research summaries emphasize hook, legible Japanese text, live UI and Before/After. The user's 16-panel ChatGPT×Excel storyboard was inspected; original v33 MP4 was not accessible. This 8-scene video is still below the storyboard's photographic/robot/real-UI variety.

## Open risks
Independent Japanese ASR, subtitle meaning and timing, source commercial rights, real-phone playback, employee approval, and actual GitHub Actions billing are not verified. Human review required before manual posting.
