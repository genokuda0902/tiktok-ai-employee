# Cycle1156 — source → formula → result (REVIEW ONLY)

Incremental reimplementation over unmerged cycle1154, not original v33 source. The previous scene 05 mixed a table, a formula card, and a chart with some inherited content visible behind the card. This change replaces only 11.55–14.35s with an original, opaque 3-phase animated panel: month-by-month fictional source values → checked arithmetic → animated comparison chart.

Arithmetic: April 12+8=20, May 16+9=25, June 18+12=30; A=46, B=29, total=75. 10 genre palettes, no employee data. The underlying Japanese narration and burned subtitles are preserved, but independent ASR/semantic alignment is NOT VERIFIED.

## Reproduction (private source, not included in public repo)

- Source: cycle1154_PROBLEM_VISUAL_JP_REVIEW_ONLY.mp4 (SHA256 85c20f33c0d5d7055bd81bddc856bf70958254ed929be6c0ab67455b5ac7ac1b).
- Output: cycle1156_SOURCE_FORMULA_RESULT_JP_REVIEW_ONLY.mp4 (SHA256 855509adc699189b8b5b7391b2b323a5624e9eedec94ac33ab7f092f7a016f91).
- Use a private manifest containing policy HUMAN_REVIEW/PUBLICATION_NOT_APPROVED, asset_approval review_only_no_publication, manual_post_only true, source_sha256, genre ai, window [11.55,14.35].
- Command: python quality/cycle1156/proof_story.py --source <private-source.mp4> --output <private-output.mp4> --manifest <private-manifest.json> --workdir <private-workdir>
- Required: Python 3.11, pillow==11.1.0, ffmpeg/ffprobe, fonts-noto-cjk.

## Verified local QA

- Real MP4 1080×1920, H264/30fps, AAC/48kHz, 23.033333s/691 frames, full video+audio decode PASS.
- Source and output encoded AAC ADTS SHA256 both 27c264983af59b982989997b1fbe7648f703c1610f35d057b17f6346848e3e6a65 (bit identical).
- 84 overlay frames; nine sample frames: subtitle area MAE 0.4025–0.8409 / 255; active visual area MAE 42.329–46.724 / 255 (three sampled active times).
- Local unit tests 11 PASS; synthetic A/V render 150 frames and full decode PASS.
- User storyboard: 16 panels/~36s, cinematic/real operation variety. This version remains 8 scenes/23.033s. Original v33 MP4 and full research chat originals unavailable in this run.

## Not verified / prohibitions

Rights of inherited source, independent Japanese speech recognition/caption meaning/timing, phone playback, employee approval, and GitHub Actions billing remain unverified. No public media upload, no merge, no automated TikTok posting, no paid service. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
