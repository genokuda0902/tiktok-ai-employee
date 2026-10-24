# cycle824 — sequential attention focus (review only)

## Delta / no duplicate experiment
- Builds on draft PR #139 (cycle823 AI-work fictional UI), not on the unrelated sales-business PR #137.
- A two-stage cyan focus frame draws the viewer from the left Before/first action to the right After/next action in the middle scene. It does not cover the caption-safe lower third.
- The exact same reusable postprocessor accepts ten genre palettes and arbitrary source MP4s.
- The local conversation review sample applies it to the existing cycle822 **sales_business** 23.933s Japanese-audio-inherited MP4, from 15–18s. CI applies it to **ai_work** 25.83s Japanese Open JTalk MP4, from 16–19.3s. These are different genres and source videos; do not conflate them.
- Audio is stream-copied. Tests reject unknown genres and out-of-bounds focus.
- No unapproved media or confidential images committed. No automatic posting, paid services, merge or publication approval.

## References and gates
- Past TikTok市場分析/動画研究: only prior summaries accessible; full task transcripts unavailable.
- User-provided 16-panel AI時短ラボ storyboard accessible via file library; original v33 MP4 unavailable this cycle.
- Main branch remains at 18e084c38db0dc55db7dfc0532b9451b1167f2aa; this is a stacked draft branch, not a main merge.
- Japanese speech text is generated from script, but speech naturalness and word-level subtitle alignment not independently verified.
- Smartphone playback, source rights, employee approval and reference equivalence unverified.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Reproduce locally
```bash
python -m unittest discover -s quality/cycle824 -p 'test_*.py' -v
python quality/cycle824/focus824.py --source INPUT_WITH_JAPANESE_AUDIO.mp4 --output REVIEW_ONLY.mp4 --genre ai_work --start 16 --duration 3.3
```
