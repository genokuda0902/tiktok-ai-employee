# cycle567 — visible Japanese step cues (REVIEW ONLY)

The original 20s synthetic video had a soft subtitle track that many mobile players hide. This reimplementation adds eight short **visual step annotations** in a reserved bottom panel (x50..1030, y1625..1775), keeping the spreadsheet proof region (y<1600) intact. The visual annotations are **not transcripts**; there is no Japanese narration.

## Local reproducible command
```bash
python quality/cycle567/render_visible_captions.py --source /path/to/cycle566_rights_safe_score_REVIEW_ONLY.mp4 --output /tmp/cycle567_REVIEW_ONLY.mp4 --cues-json quality/cycle567/genre_example.json
CYCLE567_SOURCE=/path/to/cycle566_rights_safe_score_REVIEW_ONLY.mp4 CYCLE567_OUTPUT=/tmp/cycle567_REVIEW_ONLY.mp4 python quality/cycle567/test_visible_captions.py
```
Dependencies: Python 3.11+, ffmpeg with libass, libx264 and Noto Sans CJK JP. No external APIs or paid assets.

Source MP4 intentionally NOT committed: inherited synthetic visuals require a final rights/privacy review. The script copies procedural music and the previous optional soft subtitle track without modifications. Source audio has **no narration**.

## QA / publication gates
- Unit: 4 tests; local integration: 4 tests (2026-10-14, 8/8 PASS on actual media).
- Actual preview: 1080x1920 H.264 30fps 600 frames, AAC + mov_text, 20.000 seconds.
- Visual cue panel changed at all eight sampled scene times; original content upper ROI mean absolute gray difference 0.028 at 10.5s.
- Audio and subtitle bitstream MD5 match previous cycle.
- Narration NOT_GENERATED, semantic sync NOT_TESTABLE, rights HUMAN_REVIEW.
- PUBLICATION_NOT_APPROVED; employee must approve and manually post only.
- Never call the visuals a v33 reproduction or a verified TikTok-safe-zone rendering.

## 10-genre adaptation
Supply a JSON file with `genre` and contiguous `cues` from 0 to 20 seconds; the same ASS composer, safe region and tests can be reused. No actual testing of other genres is claimed.

## Next
Use a rights-cleared offline/CI Japanese TTS and verify the actual spoken content, then align subtitles by measured speech timings. PR/CI must be run before integration.
