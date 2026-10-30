# cycle1013 — chapter-boundary micro-dip (human review only)

## New change vs cycle1011
cycle1011 shortened four near-silent gaps by 0.533s. cycle1013 instead introduces a chapter-aware, approximately 0.27s luminance dip around each of seven scene cuts (8 frames at 30fps), using FFmpeg's frame-evaluated brightness filter. This avoids ghosted text that a cross-dissolve would create. No scene, subtitle, voice, chapter timing, or duration is intentionally removed. This is a visual experiment, not a measured retention gain.

## Real private MP4 verification (not on public GitHub)
- AI-work review clip: 22.500s, 1080x1920, H.264 30fps, 675 frames; AAC Japanese-tagged 48kHz mono.
- All audio/video frames decoded; eight chapter markers retained; no extra selectable subtitles.
- Original and revised AAC packet-payload SHA256 identical: a6f25563169c5b4cbcd6d65fa563a2951ead48b7f45b89a7314bd89aae539738.
- Measured near-cut mean luminance difference approximately 4.3–16.5/255, far-from-cut median frame MAE approximately 0.192/255 (re-encoding). These are objective changes, **not proof of subjective quality improvement**.
- The actual private video is distributed only as a conversation review attachment, not stored in public GitHub. GitHub CI tests a synthetic 3s clip only.
- Ten genre IDs use the same renderer. Only AI-work has a real full-length rendered sample.

## Research and review restrictions
Accessible earlier summaries of TikTok market research and video study suggest 15–25s, a strong 1.5s opening, readable Japanese captions, visual evidence and human approval. User's 16-panel storyboard was previously inspected in earlier cycles, but the v33 original video remains unavailable for direct comparison. This run uses the cycle1011 private review MP4.

Independent Japanese ASR, pronunciation/subtitle timing verification, reference-video equivalence, rights for all original media, smartphone playback, actual GitHub Actions billing and employee approval remain **NOT VERIFIED**. Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No auto-posting, merge, paid purchase or public upload of private footage.

## Reproduce with approved private input
```bash
python3 -m unittest discover -s tests -p 'test_cycle1013_chapter_dip.py' -v
python3 tools/quality/cycle1013_chapter_dip.py --source /private/approved.mp4 --output /private/review.mp4 --genre ai_work
```
