# cycle843: kinetic example cards (human review only)

This is a **zero-paid-service** FFmpeg/libass extension of cycle842. It adds 8
scene-specific animated example cards to the lower photo region without covering
the existing one-phrase Japanese captions. All 10 genres share the same layout
engine, with genre-specific accent colors.

## Render locally

Python 3.11 and FFmpeg with libass/Noto Sans CJK are required. A cycle842 MP4
is required as input and **is not committed** because source image and narration
rights are not yet cleared.

    cd automation/cycle843
    python -m unittest -v test_kinetic_action_cards.py
    python kinetic_action_cards.py \
      --source /path/to/cycle842_MASKED_PHOTO_DISSOLVES_JAPANESE_HUMAN_REVIEW.mp4 \
      --output /path/to/cycle843_KINETIC_ACTION_CARDS_JAPANESE_HUMAN_REVIEW.mp4 \
      --manifest manifest.review.json --genre ai_work

The renderer uses \`-c:a copy\`; compare the AAC elementary stream hash with
the input and run full video/audio decode before claiming a successful render.
It is not a substitute for checking spoken Japanese naturalness or exact
semantic subtitle alignment.

## Review gates

- Do not merge or publish automatically.
- No paid services, external media uploads or auto-posting.
- No approval of model/asset rights, final narration rights or employee review.
- No direct reference-video comparison or phone hardware playback has occurred.
- CI tests only the generator contract and safety policy, **not** the MP4.
- New independent native-resolution photographs remain a separate TODO.

## Difference from cycle842

cycle842: seven photo-only dissolves, 24 subtitle beats, original audio.
cycle843: all preserved, plus eight timed animated concrete examples and
ten-genre policy/position tests. The previous source photos are reused.
