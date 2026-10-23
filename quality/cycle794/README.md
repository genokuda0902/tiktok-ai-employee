# cycle794 — UI prompt focus guidance (review only)

New quality issue: at 6.2–8.6 seconds in cycle793, a mock AI prompt interface has no explicit visual guide to its input and send controls. Add sequential cyan focus outlines for the input (6.22–7.78s) and send (7.80–8.60s) with a pointer; no actual click is claimed. Unlike cycle793's number collision restoration, this targets UI tutorial clarity. Reuse ten-genre configurable safe-area geometry. Original source media and inherited Japanese AAC remain local, never committed to GitHub. CI generates synthetic tone only, not narrated production MP4.

Local reproduction: `python -m unittest discover -s quality/cycle794 -p 'test_*.py' -v` and `python quality/cycle794/focus_guidance.py --config quality/cycle794/config.json --input /LOCAL/cycle793.mp4 --output /LOCAL/cycle794_UI_FOCUS_GUIDANCE_REVIEW_ONLY.mp4 --report /LOCAL/qa.json`.

Reference 16-panel storyboard and AI JITAN guide consulted. TikTok市場分析 / TikTok動画研究 historical summaries available; full research transcripts and original v33 MP4 inaccessible. Reimplementation, not recovered v33. Human audio/caption semantic review, rights, mobile playback and employee approval pending. No merge, payment, posting or publishing.
