# cycle1174: three-beat task focus (REVIEW ONLY)

Reimplementation, **not original v33**. The prior cycle1173 clean progress rail is preserved. This cycle replaces only the upper 1270px in scene 2, from 3.00–5.96 seconds, with original offline vector art: three sequential highlights (data aggregation, email, formatting). This removes redundant clutter from the upper panel. It preserves inherited Japanese narration and burned-in subtitle area; it does **not** prove semantic speech/subtitle alignment.

## Local private render

Install FFmpeg, Pillow and Japanese Noto CJK fonts. Create a private JSON manifest with keys `policy` (`HUMAN_REVIEW/PUBLICATION_NOT_APPROVED`), `asset_approval` (`review_only_no_publication`), `manual_post_only` (`true`), `roi_reviewed` (`true`), `genre` (`ai` or one of ten supported), `overlay_height` (`1270`), and `source_sha256` (actual SHA256 of your locally reviewed source). Run:

`python quality/cycle1174/guided_tasks.py --source /private/input.mp4 --output /private/review.mp4 --manifest /private/manifest.json --report /private/qa.json`

**Do not commit** private MP4, screenshots, voice, source manifest, secrets or private assets. This code does not upload media. CI runs unit tests and a synthetic video only. For other genres, visual ROI and wording still require manual review. No merge, posting, employee delivery or paid service. Japanese ASR, semantic subtitle alignment, rights, mobile device playback and approval are not verified.
