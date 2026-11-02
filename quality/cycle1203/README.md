# cycle1203 — contrast-adaptive central diagram detail (HUMAN_REVIEW)

Previous cycle1201 added an eight-step chapter progress rail. This cycle introduces a **different** improvement: mild contrast-adaptive sharpening (CAS) limited to the central information panel (x=72–1008, y=390–1250). It aims to improve the fine Japanese text in illustrations while leaving burned-in Japanese narration captions, progress rail and footer outside the processing ROI. Audio is copied without re-encoding.

## Reproduce

- python quality/cycle1203/code/content_detail.py cycle1201.mp4 cycle1203.mp4 --genre ai
- python -m unittest discover -s quality/cycle1203/tests -p 'test_*.py' -v
- python quality/cycle1203/tests/ci_smoke.py

Python 3.11 + free FFmpeg with cas, libx264, AAC. No external stock assets, paid API, cloud upload or auto-posting. Ten genre profiles are available but only the AI example has been rendered; the ROI must be checked for every other genre.

## Actual local output (not committed)

- File: cycle1203_CONTENT_DETAIL_HUMAN_REVIEW.mp4
- SHA256: 2415470e5ae5e4cf34bae8c4930528523cb4b99fb5cf3cb91268045ad269f89b
- 22.5s / 1080×1920 / 30fps / 675 frames / H.264 + AAC 48kHz Japanese language tag.
- Full video/audio decode PASS; source/output AAC ADTS hash identical.
- Central content edge gradient average 52.191 → 54.583 (+4.58% across 24 sample patches), proxy only, not human-readability proof.
- Outside ROI mean absolute pixel difference max 0.237/255 over 8 sampled frames; differences from lossy re-encoding, not direct editing.
- 10/10 unit tests and synthetic 30-frame render/decode PASS.
- CI scope is synthetic 30-frame test, **not** the actual review MP4.

## Limitations

Independent Japanese speech transcription, semantic/timing agreement with subtitles, original v33 direct comparison, source commercial rights, real phone playback, employee approval, and reference parity remain **NOT VERIFIED**. Existing market/research summaries were consulted via prior-cycle notes; the original reference was unavailable. No publishing authorization is implied.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Do not merge or post without explicit human approval.
