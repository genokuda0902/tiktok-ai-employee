# cycle790 — scene-aware focus pulse (HUMAN_REVIEW)

**Difference from cycle789:** Previous cycle changed Japanese captions to progressive karaoke highlighting. This cycle instead adds animated double-stroke focus rings on eight illustrated subjects. The original 16 subtitle cues and inherited Japanese AAC are preserved.

## Full renderer and tests

- src/focus_overlay.py: complete 1080×1920 post-processing renderer with 8 safe-area focus boxes, 10 genre palettes and two-pass FFmpeg mux to preserve the last AAC packet.
- tests/test_focus.py: 8 unit tests.
- .github/workflows/cycle790-focus.yml: free public-repo CI, 429-frame H.264/AAC technical smoke render using **synthetic tone, not Japanese speech**.

## Local reproduction

Requires Python 3.11+, FFmpeg with libass and Noto CJK fonts.

    python -m unittest discover -s cycles/cycle790/tests -v
    python cycles/cycle790/src/focus_overlay.py --input /path/to/cycle789_review.mp4 --output /tmp/cycle790_review.mp4 --work /tmp/cycle790_work --genre science

**The inherited review input and final Japanese-narrated MP4 are not committed to GitHub because narration rights are not independently verified.** The local ZIP in the conversation includes both for reviewer-only reproduction.

## Approval gate

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Human review still required for voice naturalness, rights, smartphone playback, factual correctness and aesthetic quality. Employee approval before manual posting only. No paid services, auto-posting or merge.
