# cycle875 — source-verified before/after, 10-genre shared renderer

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is a reimplementation, **not** recovered v33 source. No auto-post, merge, paid API, public media upload or publication approval.

## Improvement vs cycle874

The inherited scene 06 had a numeric `17 → 18` card but did not show the corresponding input and recalculation clearly, and its lower visual layers were crowded. Replaced **frames 422–509** (14.067–17.000s), 88 frames, with a three-beat sequence: detect one mismatched input → correct to the source value → recompute and verify. Fictional `ai_work` data is `営業A: 4月12, 5月16, 6月18 = 46`, `営業B: 4月8, 5月9, 6月12 = 29`; before 6月営業A=17, corrected to 18. All values derive from `cycle874.chart_truth.GENRES`, not separate hard-coded totals. Layout uses the same 10 genre configurations. Only `ai_work` was exported as a full review MP4. Existing Japanese audio and burned-in subtitle region are preserved, not rewritten.

## Local review-only reproduction

```bash
PYTHONPATH=.:cycle875 python -m unittest discover -s cycle875 -p 'test_*.py' -v
python cycle875/verified_delta.py --source /PRIVATE/cycle874_REVIEW_ONLY.mp4 --output /PRIVATE/cycle875_REVIEW_ONLY.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/render_report.json
python cycle875/verify_review.py --old /PRIVATE/cycle874_REVIEW_ONLY.mp4 --new /PRIVATE/cycle875_REVIEW_ONLY.mp4 --report /PRIVATE/verification.json
```

Manifest must equal `POLICY` plus `source_sha256`; do **not** commit manifest, source video, completed video, audio, extracted frames, personal information or source rights evidence. CI runs 10 tests and a synthetic 1-second MP4 smoke test; it does **not** test the private Japanese video.

## Research / provenance

Accessible summaries of `TikTok市場分析` / `TikTok動画研究` were consulted (strong hook, meaningful quick cuts, demonstrative UI, readable Japanese captions, manual human approval). Full original task/chat text unavailable. Directly inspected the user's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` (36s) and its before/after panel 9. Original reference v33 MP4 not accessible; no direct comparison. Read latest main, open PRs, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py`, and previous cycle874 code. v33 original generation source is still unrecovered; main's daily code is not a proven v33 pipeline.

## Remaining gates

No independent Japanese speech transcription/pronunciation or semantic speech-to-caption alignment; inherited source rights and publication approval not verified. No smartphone hardware test, employee approval, original v33 video comparison or actual GitHub Actions billing verification. Do not claim reference-equivalent or publication-ready quality. The user's requested human-approved manual TikTok posting remains mandatory.