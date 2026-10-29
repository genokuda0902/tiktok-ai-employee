# cycle947 — concrete revision instruction, human review only

## Distinct change
- Base: cycle946 hard-cut smoothing (three cuts, 7-frame wipes).
- New: scene 06 replaces an abstract AFTER card with a specific, readable Japanese correction instruction and an **explicitly fictional** improved-heading example.
- Three stages in the central illustration only: 15.55–16.10 s, 16.10–16.55 s, 16.55–17.35 s. Lower burned-in subtitle area is not covered.
- No new speech or claims, and no app operation is represented as real. 10 genre accent presets; one AI-productivity MP4 rendered locally.

## Actual local media QA
- Source: cycle946 MP4 SHA-256 `48fda405481ac3f6544d9ef4ea957fd927b579b4ebf41b3a6b2ff4c7d045699d`
- New cycle947 MP4 SHA-256 `2227970fcf61102af40077af14f0c6742a4f9e3998c44eb0a2d79e6ee6c28216`
- Full audio/video decode: PASS. H.264 1080x1920 30fps, 691 frames, 23.033 s. AAC 48kHz.
- AAC elementary stream SHA-256 unchanged: `0045ddfb9eb47f798aa6ae3a465f885409dab58ce27ad0fa1479901becddc57d`
- Lower caption region mean pixel difference in sample frames: 0.874, 0.877, 0.664 (re-encoding).
- Changed central card pixel difference in sample frames: 32.941, 42.656, 46.068.
- Local pytest: 16/16 PASS. CI tests generated PNGs and command constraints, **not** the actual local MP4.
- The MP4 and QA images are kept private as local conversation artifacts, **not** uploaded to this public repository.

## Reproduce
Install Python, Pillow, ffmpeg, Japanese Noto CJK fonts. Run:
```bash
python quality_cycles/cycle947/concrete_revision_example.py input.mp4 output.mp4 --genre ai_productivity
python -m pytest -q quality_cycles/cycle947/tests/test_concrete_revision_example.py
```
The exact prior MP4 must be supplied locally. The workflow does not generate or upload a finished video.

## Safety / unresolved
Reference v33 original unavailable for direct comparison; independent Japanese ASR semantic/timing validation, source asset commercial rights, smartphone playback, employee approval and actual Actions billing unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid contract, upload, auto-post or publication.
