# cycle448 — review-only filter transition

Original synthetic dataset: 8 unique IDs; 2 require follow-up. Animated filtering shows 8 rows, fades 6 completed rows, and moves 2 pending rows to the top over 75 frames (2.5 seconds, 30 fps).

Reproduce the 75 PNG frames locally:
`python quality/cycle448/filter_transition.py --story quality/cycle448/story.json --output frames`

Then use FFmpeg to insert this animation into seconds 10–12.5 of a **locally available, approved, synthetic** 20-second source. The prior cycle447 MP4 is not in this repository; do not claim repository-only E2E reproducibility.

Local review MP4: 1080×1920 H.264/AAC 20 seconds, 600 frames, full decode verified. Sound is non-verbal SFX only; Japanese narration and voice/caption synchronization are **missing**. The video is not approved for publishing.

The 14 local unit tests were run separately. Test-file GitHub upload was blocked; repository CI has not run. No merging, external delivery or auto-posting.
