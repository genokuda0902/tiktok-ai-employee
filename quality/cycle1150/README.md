# cycle1150 — proof-first hook (review only)

Goal: test the research hypothesis "show a concrete finished result in the first 1.5 seconds" without disturbing existing Japanese narration or subtitles. Different from cycle1148's CTA de-ghosting. Source remains the private, unapproved cycle1148 review video; no source video, extracted audio, or image assets are committed.

- Ten genres: ai, business, money, learning, health, food, travel, beauty, career, life. Per-genre accent and a manifest-supplied short proof text.
- AI example: fictional spreadsheet result 46 + 29 = 75. Arithmetic is checked if proof_numbers are supplied.
- The hook appears at 0.12–1.50s in the unused first-scene progress panel, ROI x52..896, y1305..1387, with alpha fade. Existing caption panel begins around y1490; fail-closed protected boundary y1480.
- Fail-closed source SHA-256, review-only asset policy, manual posting, time window, font-width and caption geometry checks.
- No publishing, merge, external asset upload, license claims, or paid service.

Run locally with Python 3.11, FFmpeg/ffprobe, Noto CJK fonts and Pillow 11.1.0:

```bash
PYTHONPATH=quality/cycle1150 python -m unittest discover -s quality/cycle1150/tests -p 'test_*.py' -v
PYTHONPATH=quality/cycle1150 python quality/cycle1150/tests/ci_smoke.py
PYTHONPATH=quality/cycle1150 python quality/cycle1150/proof_first_hook.py \
  --source /private/path/approved-for-review-only-source.mp4 \
  --output /private/path/cycle1150_review.mp4 \
  --manifest /private/path/manifest.json \
  --report /private/path/report.json
```

The local manifest must contain `policy`, `genre`, `source_sha256`, `asset_approval: review_only_no_publication`, `manual_post_only: true`, `proof_text`, optional `proof_numbers`, and `window`. The local manifest itself is not committed.

CI runs only 10-genre unit tests and a 2-second synthetic A/V render/decode. The private full-length review MP4 is tested locally and delivered in the conversation, not on GitHub. Independent Japanese ASR, semantic subtitle timing, original v33 parity, rights, mobile playback, staff approval and actual billing remain unverified.
