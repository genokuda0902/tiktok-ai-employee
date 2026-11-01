# cycle1122 — Japanese audio metadata + caption timing signal QA (REVIEW ONLY)

## Distinct change vs cycle1120
- cycle1120 removed a default-enabled soft subtitle stream to prevent doubled on-screen Japanese captions.
- cycle1122 preserves that single burned-in caption layer and **corrects the MP4 audio stream language from `und` to `jpn`** using a no-reencode remux.
- Adds a 20-ms RMS-based, eight-cue caption/sound-activity review report, including characters per second and signal-active fraction. **This is NOT ASR and cannot establish Japanese narration/caption semantic agreement.**
- Shared code accepts exactly ten genre identifiers; fails closed on missing/pinned source SHA, wrong media, unexpected soft subtitles, cue overlap, or output overwrite. No automatic posting or publication.
- Source/video/audio rights remain unverified, so completed review MP4, SRT and private manifest are **NOT** committed to this public repository.

## Research and reference
- Consulted accessible historical summaries of **TikTok市場分析** and **TikTok動画研究**: first-second hook, purposeful short cuts, real UI evidence, readable Japanese subtitles, employee review before manual posting. Full original task/chat transcripts not accessible.
- Directly viewed user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` from file Library: 16 panels, ~36 seconds, character/robot imagery, real-looking ChatGPT/Excel demonstration, Before/After and CTA. Original v33 MP4 source unavailable here; no equivalence claim.
- Verified main commit `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py` (still silent `-an`) and open parallel PRs #521/#522. This branch starts from main and does not merge any PR.

## Local real review MP4 (NOT in GitHub)
- Source: cycle1120 MP4, SHA256 `8aa7ec8fb2c3db22a924c8be1762de5ba0529a794f36b29cea434a609fc70449`.
- Output: `cycle1122_JP_AUDIO_ACCESSIBILITY_REVIEW_ONLY.mp4`, SHA256 `5da1827e0674c5b363780d19da9d4ab099e6266a4a4c6f13b8a123b46859d90a`.
- H264 1080x1920 30fps, 691 frames / 23.033333s; AAC 48kHz; stream-copy video and audio elementary bitstreams identical to source; subtitle tracks=0; full A/V decode PASS.
- Audio language: `und` -> `jpn`. Eight SRT cue intervals have signal present, with signal-active fractions 0.531–0.683 and caption speed 5.17–7.59 characters/second. These measurements are **not** proof that Japanese words match subtitles.
- Local standalone implementation 5 tests PASS; GitHub CI exercises synthetic 1.8-second A/V only, never private source media.
- Review file shared through ChatGPT conversation, not GitHub public artifact.

## Reproduce with locally approved review source
```bash
python -m unittest discover -s quality/cycle1122 -p 'test_*.py' -v
python quality/cycle1122/japanese_audio_accessibility.py \
  --source /PRIVATE/cycle1120.mp4 --output /PRIVATE/cycle1122.mp4 \
  --srt /PRIVATE/captions_NOT_ASR.srt \
  --manifest /PRIVATE/source_manifest.private.json --report /PRIVATE/qa.json --genre ai
```
The private manifest must be exactly:
```json
{"policy":"HUMAN_REVIEW/PUBLICATION_NOT_APPROVED","source_sha256":"<actual SHA256>","genre":"ai","asset_approval":"review_only_no_public_rights_claim"}
```

## Remaining gates
Independent Japanese ASR, pronunciation, subtitle semantics and timing, smartphone hardware playback, source media rights, employee approval, reference v33 direct comparison and actual GitHub Actions billing: **NOT VERIFIED**.
Current 8-scene/23s review video is less varied than the 16-panel/36s storyboard. This cycle improves accessibility metadata and review tooling, **not** cinematic visual quality.
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid contract, external private-media upload or auto-post.
