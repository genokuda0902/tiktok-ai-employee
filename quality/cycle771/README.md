# cycle771 — editorial safe-area image-slide prototype (0 JPY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No posting, merge or paid API.

## Verified improvement vs cycle770
- Rebuilt **all 8 scenes** with original vector graphics, simplified visual hierarchy and no overlapping slide text.
- Replaced the unsaid hook question with a first slide that matches the inherited Japanese narration: 「この基板、実はパソコン。」
- Burned 16 original SRT cues into a fixed Japanese subtitle safe area at (540,1585), leaving bottom platform UI space.
- Preserved all **668** original AAC packets through separate silent-render/remux steps. Original audio PCM SHA is unchanged.
- Verified locally: 1080×1920 H.264 30fps, 429 frames, 14.314s container, complete audio/video decode, **16/16** media checks and **12/12** local tests.
- Generic compositor and 10-genre theme presets are included. Only the science genre has a finished video; other themes are previews, not videos.

## Files
- `compositor.py`: the exact shared MP4 composer used to produce the deliverable. Inputs: eight 1080×1920 PNGs, `config/phrase_cues.srt`, source audio/video, ffmpeg with libass and Noto Sans CJK JP.
- `tests/test_ci_smoke.py`: stdlib synthetic audio/PNG end-to-end MP4 test; no inherited material needed.
- `genres.json`: ten palette presets.
- `.github/workflows/cycle771-offline-smoke.yml`: optional isolated CI on this work branch.

## Source and QA
Full original vector slide renderer, the eight PNGs, inherited audio source, comparison imagery, QA JSON and reproducible code/tests are provided in the cycle771 ZIP shared in the conversation. The GitHub branch contains the genre-neutral compositor and CI tests, **not** the full proprietary inherited media.

## Limitations
No phoneme-level timing validation; Japanese voice pronunciation and reference-video parity are not human-verified; inherited audio rights remain uncleared; no smartphone playback test; no employee approval. Only employee-approved **manual posting** is permitted.
