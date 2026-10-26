# cycle878 — mobile-safe Japanese captions (review only)

**Change from cycle877:** The original 8 sentence captions were small and placed in a dark lower strip. This revision redraws exactly the same inherited Japanese sentences in **64px Noto Sans CJK Bold**, two lines per cue, within x=90–865, y=1450–1840; stronger opaque navy contrast and an 8-stage progress indicator. The 8 editorial timings are unchanged. Source visual scenes above y=1450 and AAC audio are retained; only the subtitle strip is re-encoded. It does **not** prove the Japanese speech matches the text.

## Reproduce locally (private source, never commit media)

```bash
PYTHONPATH=. python -m unittest discover -s cycle878 -p 'test_*.py' -v
PYTHONPATH=. python -m cycle878.ci_smoke
PYTHONPATH=. python cycle878/caption_safe_area.py --source /private/cycle877.mp4 --output /private/cycle878.mp4 --manifest /private/review_manifest.json --report /private/render.json
```

The manifest must exactly contain `POLICY` plus `source_sha256`. All 10 genre names in `cycle874.chart_truth.GENRES` can be passed through the same `CaptionCue` geometry validator and renderer with their **own reviewed scripts**; this cycle renders only `ai_work`. Do not recycle AI-work narration across genres.

## Known limitations / safety

- This is a **reimplementation**, not the original v33 source. Full `TikTok市場分析` and `TikTok動画研究` transcripts, the original v33 MP4 and current reference storyboard file were not accessible this run; prior confirmed storyboard findings were consulted.
- Caption text was transcribed from visible inherited captions and not independently speech-recognized. Editorial windows were inherited, not phoneme-aligned. Human listening/ASR, pronunciation, smartphone testing, source rights, employee signoff and reference parity remain unverified.
- `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`. No paid APIs, no media or voice upload to public GitHub, no automatic merge/posting. CI tests code and a **synthetic** 1-second A/V sample only.
