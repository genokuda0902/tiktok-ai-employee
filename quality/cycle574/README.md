# cycle574 — accessible burned-in captions (review only)

## Scope and baseline
- Parent: cycle573 (20s, 1080x1920, 30fps); SHA256 d581e69deef8e81e5a6cdd9f957095ed829cc552df16e325fd604d0a8a49ab93.
- Original v33 source is not recovered. This is a reimplementation and MUST NOT be described as equivalent to v33.
- New improvement: eight time-aligned Japanese on-screen captions burned into video plus eight matching SRT cues. Removes the previous 0.5s unreadable caption interval and improves accessibility where subtitle tracks are hidden.
- Japanese spoken narration is ABSENT. AAC track is instrumental only. Do not claim speech-caption synchronization.
- Inherited baseline media is NOT approved for publication; original reference v33 MP4 could not be materialized. No reference media, audio, or private images are committed.
- All media and publication state remain HUMAN_REVIEW / NOT_APPROVED. No auto posting, merge or paid API.

## Reproduce (requires approved, matching local baseline video)
```sh
python -m unittest discover -s quality/cycle574 -p 'test_cycle574.py' -v
python quality/cycle574/render_accessible_captions.py --source cycle573_formula_range_REVIEW_ONLY.mp4 --output cycle574_burned_captions_REVIEW_ONLY.mp4
ffmpeg -v error -i cycle574_burned_captions_REVIEW_ONLY.mp4 -f null -
```

Python 3.11+, FFmpeg with libass, Noto Sans CJK fonts. The input MP4 is intentionally not committed for asset-rights reasons.

## Local evidence (not GitHub CI)
- 9 tests passed.
- Output 20.000s, H.264 1080x1920 30fps, AAC, mov_text subtitles; full decode passed.
- SHA256 a65e5e759ce24bd3ca1a3ef8229c04f9be8e9c0e910d3a06e40339e9ebe02bb3.
- Full video and local source/test/QA bundle shared in the conversation, not attached to this PR.
- Reference 16-panel storyboard viewed; v33 raw MP4 unavailable (authorization denied).
- CI workflow creation was attempted, but the connector rejected it; CI status remains UNVERIFIED.
