# cycle1124 — two-stage formula/result focus (review only)

HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Original reimplementation, not recovered v33 source. No merge, posting, or public media distribution.

## Prior state and research
- Source cycle1122 private MP4 SHA256: 5da1827e0674c5b363780d19da9d4ab099e6266a4a4c6f13b8a123b46859d90a.
- cycle1122 only changed AAC language metadata; eight signal windows detected, no independent Japanese ASR.
- Accessible summaries of TikTok市場分析 and TikTok動画研究: immediate hook, purposeful cuts, real UI proof, Before/After, readable captions, manual employee review. Full original transcripts unavailable.
- User 16-panel ~36-second ChatGPT×Excel時短術16コマ絵コンテ.png directly inspected; original v33 MP4 inaccessible this run.
- Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, open PRs #523 and #524, PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md.
- PR #524 independently improves soft transitions; no duplicate transition changes here.

## Distinct issue and fix
At 6.0–8.66 seconds, the original scene03 animated hint could display =SUM(C2:C4) even though the spreadsheet formula bar shows =SUM(B2:B4) for sales A, 12+16+18=46. The previous hint was inconsistent with the visible spreadsheet.

This change masks the stale hint with a high-contrast banner and provides two accurate guides:
- 6.00–7.25s: ① 数式：=SUM(B2:B4) plus cyan formula focus outline.
- 7.25–8.66s: ② 合計欄：46 / 29 plus amber totals focus outline.

All values are fictional. This does not imply AI verified the data. Manifest requires exact source SHA, review-only approval, ten supported genre IDs, PII-pattern rejection and bounded focus coordinates/timing. Existing files cannot be overwritten.

## Local finished private MP4
- SHA256 2a5c41857bb82999323ca26c3b29e78a0409c805bd657bebda72eaacd83de01b.
- H264 1080x1920, 30fps, 691 frames, 23.033333s; AAC 48kHz tagged Japanese; zero soft subtitle tracks.
- Full A/V decode PASS; AAC elementary stream identical to cycle1122.
- 12 sampled-frame comparisons; subtitle ROI mean pixel difference 0.418–0.982 / 255. Re-encoding also changes pixels outside the focus scene.
- Eight local unittest cases PASS, including 10 genre configurations and a synthetic 2-second A/V render.
- Real MP4 shared only as private ChatGPT artifact; not committed to GitHub. CI tests synthetic media only.

## Reproduction
Install FFmpeg, FFprobe, Python 3.11+, Pillow, Noto CJK font.
Prepare local private manifest with exact fields: policy, asset_approval, source_sha256, genre, focus_scene. Focus scene has start/split/end/focuses; each of two focuses has label/rect/badge_xy.

python quality/cycle1124/scene_focus.py --source /private/source.mp4 --output /private/output.mp4 --manifest /private/manifest.json --report /private/qa.json

python -m unittest discover -s quality/cycle1124 -p 'test_*.py' -v

## Unverified gates
Independent Japanese ASR, pronunciation and caption semantics/timing, smartphone playback, media/voice rights, staff approval, original v33 parity, retention and actual Actions charges. Reference ~16 scenes/36s is more cinematic and varied than current 8-scene/23s video. Next: independent narration transcript + caption alignment; approved cinematic assets. No merge, auto-post, paid services or public private-media upload.
