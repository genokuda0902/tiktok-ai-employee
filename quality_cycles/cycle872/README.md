# cycle872 — portrait-led editorial slides (review only)

This branch adds a portable technical QA core and tests for a locally rendered 23.033s Japanese-narrated 1080×1920 H.264/AAC review video.

## What changed vs cycle871
- Added **new AI-generated photographic portrait accents** in opening and closing scenes. The source portrait crops are only 253×203 and 224×207 pixels; enlarged images are **not** native high-resolution photos.
- Retained 8 original vector-style slide compositions, 2× Japanese text rasterization, 24 burned-in subtitle beats and the locally recorded synthetic browser demonstration.
- Updated the common 10-genre registry to match the actual names in `TikTok_10ジャンル_初期100企画.xlsx`.
- Added photo/headline/caption-safe geometry checks.

## Tests
`python -m unittest discover -s quality_cycles/cycle872 -p 'test_*.py' -v`

The finished MP4 and source assets are **not committed** because source voice rights, portrait approval, reference-video comparison and employee approval are outstanding. The complete local reproduction package was delivered separately to the user. GitHub CI tests the portable QA logic, **not the finished MP4**.

Status: **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid service or automatic posting.
