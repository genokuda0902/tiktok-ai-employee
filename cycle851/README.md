# cycle851 — Actual Calc correction, not a simulated ChatGPT result

**Scope:** Review-only / HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Stacked on unmerged cycle850 PR #189. Reimplementation, not recovered v33 source.

## Delta from cycle850

- Replace scene 06's static illustrated "修正点" laptop card with an **actual locally recorded LibreOffice Calc interaction** on entirely fictional numbers.
- Before: May AI result `17`, source `18`, `CHECK`; total `50` vs `51`, `CHECK`. During recording, operator types `18` into B4. After: row `OK`, total `51` vs `51`, `OK`, driven by genuine spreadsheet formulas.
- 85 of 691 frames (422–506 / 14.067–16.867 s) are composited into the original central image area only. Existing Japanese narration, burned-in subtitles, heading and CTA are preserved. No new claims of measured time savings or real customer data.
- Shared 10-genre rendering component with strict SHA-pinned local manifest and fail-closed review gates; 10 offline unit tests and a synthetic-only CI render.

## Local commands (all assets kept out of public GitHub)

```bash
PYTHONPATH=cycle851 python -m unittest discover -s cycle851 -p 'test_*.py' -v
python cycle851/real_calc_correction.py \
  --source /private/cycle850-review.mp4 \
  --capture /private/fictional-real-calc-screen-recording.mp4 \
  --output /private/cycle851-review.mp4 \
  --report /private/cycle851-qa.json
ffmpeg -v error -xerror -i /private/cycle851-review.mp4 -f null -
```

The GUI recording is an original local screen capture, not an official ChatGPT screen or evidence of AI model accuracy. The public PR stores **code, tests, CI and this document only**, never the rights-unverified source audio/images, capture, or finished MP4. The Japanese review MP4 is distributed privately via ChatGPT sandbox for employee assessment.

## Research and outstanding checks

Previous `TikTok市場分析` and `TikTok動画研究` summaries indicate: first 0–1.5 s hook, 15–25 s, one message, short cuts, real demos, Before/After, safe Japanese captions, human-approved manual posting. Full research task transcripts were not retrieved. The user-supplied 16-panel storyboard was visually inspected; original v33 MP4 could not be retrieved. v33 remains the quality benchmark, **not matched or proven**. Animated robot remains cancelled per handoff.

Still unverified: independent Japanese ASR/pronunciation/semantic subtitle alignment, public rights for inherited footage and voice, employee sign-off, phone playback, actual GitHub Actions billing. No merge, automatic posting, paid API or external upload.

Next priority: independent Japanese audio/caption timing QA, then approved image-first 12–16 visual beats with cinematic photographic assets; avoid repeated micro-transition tweaks.