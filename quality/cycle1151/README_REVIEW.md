# cycle1151 — 0-yen animated proof chart (human review only)

- Source: cycle1149 completed private MP4, not stored in GitHub.
- New, non-repeated change: replace the static chart in chapter 03 with an animated three-bar, data-driven proof card showing **9 → 14 → 21** (explicitly synthetic). This is different from cycle1149's speech-onset caption accent.
- Code: `code/animated_proof_chart.py`; unit tests: `tests/test_animated_proof_chart.py`; synthetic full-encoding test: `code/ci_synthetic.py`.
- All 10 genre palettes share the same chart renderer; only AI-work completed MP4 rendered. Original narration and subtitles inherited; no ASR or semantic timing verification.
- Run: `python quality/cycle1151/code/animated_proof_chart.py SOURCE.mp4 OUTPUT.mp4 --genre ai-work`.
- Safety: human review, rights review and smartphone playback required. No paid services, automatic posting or merge. Never treat synthetic data as genuine results.
- GitHub CI exercises synthetic 9s media only; the private 22.5s deliverable is tested locally.
