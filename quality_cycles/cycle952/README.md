# Cycle952 — Three-field mobile reading guide (human review only)

**New, distinct improvement:** cycle951 PR #347 removed double-exposed text at seven scene cuts. This cycle adds a scene-4 purpose → condition → format focus rail and contextual label inside the fictional prompt editor. Parallel PR #348's arithmetic/semantic QA ledger is not changed or merged.

The local source is the private cycle951 review MP4 (H.264 1080×1920, 30fps, 691 frames, 23.033s). This code does **not** contain or publish source media. It creates transparent field overlays, fades them on/off in three beats (8.94–11.38s), encodes video using local FFmpeg, and copies AAC from the original file without transcoding. The source captions, header and footer are outside the overlay region.

## Reproduce with authorized source

    python -m pip install Pillow pytest
    python quality_cycles/cycle952/editor_focus.py --input /path/to/authorized_source.mp4 --output /path/to/review.mp4 --workdir /tmp/focus --genre ai_work
    python -m pytest -q quality_cycles/cycle952/tests

There are **10 palette definitions**, but geometry is visually approved only for ai_work. All other genres fail closed until their own scene layout has been checked. No auto-posting, public media upload, merging, or paid service.

## Actual local MP4 QA (not performed by CI)

- Source: cycle951 review-only MP4; output: cycle952 review-only MP4, 5,008,591 bytes, SHA256 0f270382d848e9c89d9e75bcad7815fc61f01ca2a9f8c7d5c0f2c04de2dacd82.
- H.264 1080×1920 30fps, 691 frames, 23.033s; full video/audio decode PASS.
- AAC 48kHz ADTS SHA256 unchanged from source; independent Japanese ASR **NOT** performed.
- Highlight border mean absolute pixel differences at 9.33/10.14/10.97s: 28.852 / 29.629 / 36.707. Caption region differences due to lossy reencode: 1.211 / 1.209 / 1.195 intensity levels.
- Local tests: 31/31 PASS. CI tests source and synthetic overlay only, not the actual MP4.

## Research and restrictions

Earlier TikTok market/video research: 0–1.5s hook, 15–25s, short readable Japanese captions, clear demo/Before–After, safe zones, human-approved manual posting. User-provided 16-panel storyboard referenced from earlier work; original v33 MP4 and research full texts unavailable here. Original reference's cinematic visuals and diverse live demos are **not** verified as matched.

Unverified: independent Japanese speech recognition and subtitle semantic/timing alignment, original v33 side-by-side, inherited media commercial rights, smartphone playback, employee approval, actual GitHub Actions billing.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Never merge, auto-post, or assert commercial rights without explicit approval.
