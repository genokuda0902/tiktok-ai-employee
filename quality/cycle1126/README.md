# cycle1126 — animated save → reuse completion cue (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Reimplementation, not original v33. No media, personal information, private manifests, or extracted audio committed. Do not merge or publish without staff approval and rights/privacy review.

## Research and provenance
- Directly reviewed user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels, about 36 seconds), showing a stronger end CTA and scene variety than this 8-scene, 23.033s reimplementation.
- Accessible summaries of `TikTok市場分析` and `TikTok動画研究`: hook within ~1.5 seconds, purposeful cuts, real UI proof, readable Japanese captions, Before/After, CTA/loop, manual employee posting. Full source chat transcripts unavailable. Original v33 MP4 not available in this run.
- Checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, unmerged PR #525 and parallel #526, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, and existing `src/` and `quality/cycle1124/` implementation.
- Source is local cycle1124 review-only MP4, SHA256 `3caccf4358354c6cf0e756f52f31f98809024a40a6690a158edb895906c84ea0`.

## Distinct change versus cycle1124
- cycle1124 fixed the inconsistent formula `=SUM(C2:C4)` → `=SUM(B2:B4)` and added two-stage spreadsheet focus at 6.0–8.7 seconds.
- cycle1126 adds a smooth two-stage **completion action cue** during 20.8–22.8 seconds: highlight `02 保存する` then `03 次回も再利用`. This makes the closing narration's habit-building action visible, closer to the reference CTA, without asserting unverified results.
- The two buttons remain within the upper safe zone; existing burned-in Japanese subtitle area is not overlaid. A subtle fade and pulse direct attention; no new spoken words or false performance claims.
- Shared renderer is genre-configurable for 10 categories; strict exact SHA, review-only policy, genre, frame-aligned timing, safe-zone and PII checks reject unsafe manifests.

## Local result
- Output MP4 SHA256 `68d13d172353e06fa6913a176de347a7eae1e592791fdd460ce760418007fc2e`.
- H.264 1080×1920, 30fps, 691 frames, 23.033333s; AAC 48kHz with Japanese language tag; zero soft subtitle tracks.
- Entire output video/audio decoded successfully; AAC elementary bitstream identical to cycle1124.
- Comparison at 21.2/22.2s: button-region mean RGB pixel difference 20.96 / 18.35 (out of 255); subtitle-region mean RGB pixel difference 0.674 / 0.680, reflecting whole-video re-encoding.
- Local tests: 8 PASS (includes all 10 genre configurations and a synthetic 1.5s A/V render).
- Completed private MP4 shared only in ChatGPT artifact, not in GitHub. CI tests synthetic media only.

## Reproduce locally (no private media in repository)
Install Python 3.11+, Pillow, FFmpeg, FFprobe, and Noto CJK fonts.
Create a local JSON manifest with exact keys `policy`, `asset_approval`, `source_sha256`, `genre`, `cue`. `cue` has `start`, `switch`, `end` (30fps grid), and two `steps` with normalized `rect` and `label`. Source SHA must match exact local MP4; label content must be reviewed.
```sh
python quality/cycle1126/completion_cue.py --source /private/previous.mp4 --output /private/review.mp4 --manifest /private/manifest.json --report /private/qa.json
python -m unittest discover -s quality/cycle1126 -p 'test_*.py' -v
```

## Remaining blockers
Independent Japanese speech-to-text and semantic/timing alignment for all eight cues (especially 20.3s onward), smartphone playback, rights/staff approval, reference v33 original side-by-side, and Actions actual billing. Reference has richer people/robot cinematics and cuts. Next: offline Japanese ASR if model/license can be obtained at zero cost; otherwise explicit human transcript checklist, then improve approved cinematic imagery. No automated posting, merge, or paid services.
