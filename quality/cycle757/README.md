# cycle757 — review only (2026-10-22 JST)

## Change from cycle756
Cycle756 enlarged the opening 0–3.2s. Cycle757 instead replaces frames 493–603 (16.433–20.133s) with a 10-genre reusable **BEFORE/AFTER evidence comparison**: authentic screenshot of *synthetic* Calc cells beside an animated chart of March ¥200,000 and April ¥180,000. These values agree with inherited Japanese SRT cue 6. It is an illustration, not proof of live AI operation or claimed time savings.

## Files and local reproduction
- `src/comparison_story.py`: full Python renderer, ten genre palettes, safe bounds, data consistency.
- `tests/test_comparison_story.py`: 17 local tests passed.
- The private QA ZIP (shared in ChatGPT) contains the approved local input MP4, synthetic screenshot, output MP4, subtitle SRT, comparison contact sheet and decode logs.
- Run `python -m pytest -q quality/cycle757/tests/test_comparison_story.py`.
- Render with `python quality/cycle757/src/comparison_story.py --source <cycle756.mp4> --screenshot <synthetic_calc.png> --output <cycle757.mp4>`.

## Verification and exclusions
- MP4 SHA-256: `8d28704ec1ba4364e10f2b120208164f2eadf8f5a35efe49b6e8ed00c63804b3`.
- Baseline SHA-256: `195f76f80f5d28507d2c7d551fd8791ec36417364863c77b3e98b66df153f7fb`.
- H.264 1080x1920 / 30fps / 819 frames / 27.343s, AAC audio inherited unchanged; full video/audio decode PASS.
- Local 17 tests PASS; ten genre palettes tested.
- User 16-panel storyboard inspected; v33 reference MP4 unavailable this run.
- TikTok市場分析 and TikTok動画研究 task settings inspected; full research reports unavailable.
- Speech naturalness, strict audio/subtitle alignment, phone playback, rights and employee approval unverified.
- GitHub CI workflow creation and Draft PR creation were blocked by connector safety checks. No CI run, merge or posting.
- Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; manual posting only after employee approval.
