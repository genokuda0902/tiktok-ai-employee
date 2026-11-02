# cycle1144 — synthetic cursor proof (review-only)

Distinct from cycle1142's B/C formula arithmetic overlays. Original drawn pointer guides attention in scene 06: B5 (46) → C5 (29) → total (75), 90 frames at 30fps, without altering existing captions or Japanese AAC elementary stream.

Source/tests are in `source_tests.tar.xz` (SHA256 `fa081a17938d55800f7ea27ff55f56539520722efbc2f188ad0f768d506c0116`, Git blob `28602a651a59b6e122bc9b25e90dd39e0aa9648a`). Extract: `tar -xJf quality/cycle1144/source_tests.tar.xz -C quality/cycle1144`. Run `PYTHONPATH=quality/cycle1144 RUN_MEDIA_SMOKE=1 python -m unittest discover -s quality/cycle1144 -p 'test_*.py' -v`.

For a real render, supply your **local** review-only MP4 and a private JSON manifest with exact SHA256, genre, three approved waypoints and window; run `python quality/cycle1144/cursor_guide.py --source INPUT.mp4 --output OUTPUT.mp4 --manifest PRIVATE.json --qa QA.json`. Do not commit source video, audio, private manifest, storyboard or MP4.

Cursor is a synthetic instructional illustration, not real recorded mouse interaction. CI uses synthetic 2-second H264/AAC only. Ten genre configurations share fail-closed source hash, private approval and safe ROI checks. No merge, automatic posting, paid API, or public release.