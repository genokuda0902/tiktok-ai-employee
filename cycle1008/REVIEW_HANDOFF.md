# cycle1008 — default-caption duplication repair (PRIVATE HUMAN REVIEW)

2026-10-30 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Concrete difference from cycle1006
- Prior review MP4 has burned-in Japanese captions **and** a selectable Japanese mov_text track whose ffprobe disposition.default was **1**, not 0. A player that auto-enables default subtitles can show Japanese text twice.
- Attempted FFmpeg `-disposition:s:0 0` on a synthetic MP4. The MP4 muxer still reported the sole subtitle track as default=1; this approach failed the regression test and was rejected.
- New review MP4 omits the optional mov_text track entirely; the already burned-in captions remain, and an **8-cue Japanese SRT sidecar** is exported for optional manual use. This is a safe default playback variant, NOT an embedded selectable-subtitle accessibility solution.
- Video and AAC elementary streams were verified bit-identical to cycle1006; no picture, voice or caption wording changed. This fixes a playback packaging problem, not the cinematic gap.

## Verified local private MP4
- Input: cycle1006 review MP4 SHA256 `cbe0d3e32ca90cb0c3d1cae1d78bfc898bde8a4e0bb47842e4aa6e4e1f446d8e`.
- Output: cycle1008_SINGLE_CAPTION_SAFE_JP_REVIEW_ONLY.mp4 SHA256 `25c38de04d557190dd93ca44211e88364e7629511548dc5ae2ae331ca7981d06`.
- 1080x1920 / 30fps / H264 / 691 frames / 23.033333s; Japanese-tagged AAC 48000Hz. Full video and audio decode PASS.
- Source/output elementary video SHA256 `09aa73a72955ca014e15dde64f9fa2e2ec7529581cfe816aeeaf4ae1097ee4d4`.
- Source/output AAC ADTS SHA256 `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`.
- SRT 8 cues SHA256 `eecd576cd1968c3b8d422eb5178ca416280a625f499d9eecc519c40b673c7739`.
- 8 local unit tests PASS; GitHub CI uses synthetic 2-second media only, not private MP4. See CI run URL after execution.

## Research and reference
- Accessible prior `TikTok市場分析` / `TikTok動画研究` summaries: immediate hook, concise scenes, genuine sanitized operation, Before/After, Japanese captions and employee-reviewed manual posting. Full original research chats unavailable.
- Directly viewed user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` in Library: 16 panels, about 36s, cinematic robot/person and ChatGPT/Excel demo. Original v33 MP4 unavailable. Current 8 scenes/23s remain far less varied. No parity claim.

## Repo/safety
- main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, based on unmerged cycle1006 PR #407 `f61cab1ed8b9e9027829773dceb726e9d163d5af`; parallel PR #408 untouched.
- Read `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py` and cycle1006 renderer/QA.
- 10 genre identifiers registered, only `ai_work` privately tested; all other genres fail closed.
- No public media upload, merge, auto-post, paid service or contract. Private MP4 and Japanese audio not committed.
- Independent Japanese speech recognition, subtitle semantic sync, source rights, phone playback, employee approval, actual Actions billing remain **UNVERIFIED**.

## Reproduce on an approved local private source
```bash
python cycle1008/source/caption_default_guard.py --source /private/cycle1006.mp4 --output /private/cycle1008.mp4 --report /private/cycle1008.json --expected-sha cbe0d3e32ca90cb0c3d1cae1d78bfc898bde8a4e0bb47842e4aa6e4e1f446d8e --review-only
python -m unittest discover -s cycle1008/tests -v
```

Next: independent Japanese speech transcription and caption semantic/timing QA; approved distinct shots; smartphone caption behavior. Keep manual employee approval and publication block.
