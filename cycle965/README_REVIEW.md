# cycle965 — original bookmark/save CTA (review only)

Source: private cycle963 Japanese image-slide MP4, SHA256 `161a3f1f9bfb3b4774613880a564cfff922077cb2d71dd657bd5eea9ca18506f`. The user MP4 is **not** uploaded to this public repository.

## New quality change
A compact, original vector bookmark and Japanese `保存` prompt fade into the empty left gutter of the final scene's burned-caption panel, starting at 20.85s. This provides a clear save action without replacing the Japanese narration or existing subtitle text. The first two candidate layouts covered captions; they were rejected and corrected before the final MP4.

This differs from cycle963's seven original transition sound cues and parallel cycle964 PR #365's spreadsheet arithmetic-continuity edit. The visual effect has not been validated for audience retention.

## Local actual MP4 verification (not CI media)
- Output SHA256: `05f98e17f0825dedb1f0334f0474f9e169f103eafaa8c448a6facc4f2b22c878`
- H.264 1080x1920, 30fps, 691 frames, 23.033s; full A/V decode PASS.
- AAC 48kHz, Japanese language tag; audio ADTS elementary stream SHA matches source exactly.
- CTA region x79..147, y1430..1542. Sampled mean absolute difference outside CTA max 1.1349/255 (re-encoding). 9/9 local synthetic unit tests PASS.
- 10 genre palettes, only `ai_work` visually reviewed. All other genres fail closed.
- No third-party image/audio, no paid APIs, no auto-posting, no merge.

## Unverified
Independent Japanese ASR and semantic narration/subtitle timing, original v33 reference video comparison, inherited-source commercial rights, smartphone playback, employee approval, actual GitHub Actions billing.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Employee approval is required before manual posting.

Reproduce with authorized local media:
`python3 cycle965/code/review_cta.py --input authorized.mp4 --output review.mp4 --report qa.json --genre ai_work`

Public CI uses synthetic MP4 only. No user media is committed.
