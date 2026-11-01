# cycle1145 — Japanese title ghost removal (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merging, paid services, auto-posting, or private media upload.

## Difference from cycle1143

cycle1143 lifted illustration midtones in y370–1220. cycle1145 instead repairs a pre-existing double-exposed Japanese headline in the hook-to-step transition. Replace **frames 38–49** (1.267–1.633s) with clean typography plates from source frames 36 and 50, hard cut at frame 42, 40px feather at y1130–1170. Lower Japanese narration card (y>=1170) remains untouched except re-encoding.

The reusable compositor accepts **10 genre IDs**, but only one AI-workflow finished MP4 was produced. It fails closed unless the source SHA256 matches an explicitly provided value. No new voices, data, external footage or rights-unapproved media.

## Actual private MP4 validation

22.5s, 675 frames, H264 1080×1920 30fps, AAC 48kHz mono, full A/V decode PASS. Source SHA256 `a3c3c344505baec5fec603f74569f602747429a4eef55bb6c59a8ad8af0d815a`; output SHA256 `bd9e99ff7ab70998508c7a56e8b6d557693dd211cb8521fad16961ea89611569`. AAC ADTS SHA256 identical `da601fdd17eae3cc1c0fe9a0d93843f6c07e1321d33f84f92474819c477d8b18`.

Measured title ROI ghosting vs clean reference: frame40 **13.29→1.34/255**, frame42 **13.85→1.45/255**. Narration card across all 675 frames: maximum per-frame mean absolute pixel delta **1.17/255**. Local 12 tests PASS, 75-frame synthetic H264/AAC full-decode PASS. GitHub CI runs only synthetic media and tests, never the private full MP4.

## Prior research / limits

Accessible `TikTok市場分析` and `TikTok動画研究` summaries: fast hook, purposeful visual cuts, real UI proof, legible Japanese captions, employee-approved manual publishing. Prior cycle1143 report documents the user's 16-panel / ~36s `ChatGPT×Excel時短術16コマ絵コンテ.png`; the original reference v33 MP4 remains unavailable. No parity claim.

Independent Japanese ASR, subtitle meaning/timing, inherited voice commercial rights, phone playback, employee approval, retention, and actual GitHub Actions billing **NOT VERIFIED**. AAC preservation is not semantic verification. Publication remains prohibited until human review.

## Run

```bash
python -m unittest discover -s quality/cycle1145/tests -v
python quality/cycle1145/code/ci_synthetic.py
python quality/cycle1145/code/typography_cut.py /private/source.mp4 /private/review.mp4 --expected-sha256 <SHA256>
```
