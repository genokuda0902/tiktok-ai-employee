# cycle842 — Before/After process illustration (review-only)

Reimplementation, **not original v33**. Adds a fictional, animated BEFORE/AFTER
process comparison in scene 8's image-only region. Unlike cycle841's generic
bar chart, this directly addresses the user 16-panel storyboard's explicit
Before/After requirement without inventing time-saving measurements.

## Reproduction (local authorized fictional source only)

Python 3.11+, Pillow 10–12, FFmpeg, ffprobe, Noto Sans CJK fonts:

```sh
PYTHONPATH=. python -m unittest discover -s cycle842 -p 'test_*.py' -v
PYTHONPATH=. python -m cycle842.before_after \
  --source /local/approved-for-review.mp4 \
  --output /local/cycle842_review.mp4 \
  --manifest /local/manifest.json --genre ai_work
```

Manifest requires fictional data, explicit no personal/confidential media,
review_only=true, publication_approved=false, external_upload=false,
automatic_posting=false, source_rights_reviewed=false, and SHA256 of exact
input. Fails closed if metadata missing or source hash mismatched.

## Local result, 2026-10-25

- Based on previous local cycle841 MP4 (PR #170), source SHA256
  `2f29c252048b10123e36a3a86aaf621355dbbefbfe75c11f5c9837b8ea2b8942`.
- Review output SHA256
  `c8ba143e9b4d3c99a68c9a639863e7324a111e4a97fde10e42345db1c6737fa3`.
- 1080x1920 H264 30fps 691 frames / 23.033s, AAC 48kHz 23.033s;
  full A/V decode PASS, decoded PCM MD5 equal before/after
  `813f69e5c926b70c927e46e27704e267`.
- 13/13 local tests PASS. New panel changes image-only region x45..1005,
  y370..1130 during frames 588..690. Existing captions/title and audio preserved.
- Ten genre palettes implemented, only ai_work rendered locally.
- The Japanese review MP4 and private source are in ChatGPT sandbox only;
  **not** uploaded to GitHub. CI runs synthetic media only.
- No independent ASR/semantic narration verification, word-level caption sync,
  phone playback, original v33 direct comparison, or rights/employee approval.
- Other open PR #171 contains a *parallel* editorial layout; not merged.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid service, or posting.

Full TikTok市場分析 / TikTok動画研究 chat transcripts and original v33 MP4
were unavailable; prior summaries and the user 16-frame storyboard were used.
