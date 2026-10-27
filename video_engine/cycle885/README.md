# cycle885 — kinetic task cards / review-only

Release status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Sources and constraints
- Historical accessible summaries from TikTok市場分析 and TikTok動画研究: 0–1.5 s hook, purposeful cuts, practical on-screen proof, Before/After, safe Japanese subtitles, employee-reviewed manual posting. Original chat/task transcripts not accessible.
- User's ChatGPT×Excel時短術16コマ絵コンテ.png directly inspected from the file Library: 16 panels / about 36 s, cinematic robot and people, UI/Excel demos, CTA. Original v33 reference MP4 not available for direct playback comparison.
- Checked main at 18e084c38db0dc55db7dfc0532b9451b1167f2aa, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, cycle884 code, and open PRs #249 and parallel #250.
- This is a reimplementation, not original v33 source. No robot animation, unapproved private assets, paid services, posting, or merging.

## Distinct improvement
Previous cycle884 used cyan/yellow focus outlines on four rows in the first 89 frames. This cycle replaces the second scene (frames 89–169, 2.967–5.667 s) with three sequentially entering task cards: 月別データを集計 / 同じ表を毎週更新 / 転記と数字の照合. An explicit まずは1つ、書き出そう call-to-action appears after the task sequence. All are fictional demonstration tasks, not actual AI output. The original Japanese AAC stream and burned caption region are inherited unchanged in content.

Shared implementation: ten-genre allowlist, three-task story model, timed easing, geometry/safe-zone checks, privacy-sensitive copy checks, source-SHA/policy fail-closed validation. Only ai_productivity was rendered to a full review MP4. Other genres require their own approved script/media/coordinates.

## Reproduction with PRIVATE local input (do not commit/upload)
Requires Python 3.11, Pillow 11.3.0, FFmpeg and FFprobe. Font: NotoSansCJK-Bold.ttc. On CI, imageio-ffmpeg supplies a free FFmpeg binary.

    python -m unittest discover -s video_engine/cycle885 -p 'test_*.py' -v
    python video_engine/cycle885/ci_smoke.py
    python video_engine/cycle885/task_cards.py --source PRIVATE_cycle884.mp4 --output PRIVATE_cycle885.mp4 --manifest PRIVATE_manifest.json --report PRIVATE_report.json --work-dir PRIVATE_overlays

Manifest requires source_sha256 equal to actual source SHA256, synthetic_ui=true, review_only=true, publication_approved=false, external_upload=false, automatic_posting=false, source_rights_reviewed=false.

## Verified LOCAL technical result (2026-10-27 JST)
- Input cycle884 private review MP4 SHA256: 1a57acc1d8151c52f53d5b104f7f913a685d07fbaee2bcc5a4cd6a0314680afb.
- Output cycle885 private review MP4 SHA256: 5f92fc4a175b762dd0c8188170f725e1fa3175f6542fcafa2306fbcd14c02465.
- H264 1080×1920, 30fps, 691 frames, 23.033 s; AAC 48kHz stereo; full A/V decode PASS.
- All 691 frames compared at 1/8 spatial sampling. 80/81 target frames had upper-region mean pixel difference >5; outside-target upper max mean 1.147; protected caption band max mean 1.1686 (compression differences).
- Source/output AAC elementary stream SHA256 identical: 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9.
- Local 15/15 unit tests and 1-second synthetic A/V smoke PASS. CI tests synthetic A/V and code only, not the private final MP4. No private video/audio or generated images are uploaded to GitHub.

## Gaps / next priority
This improves pacing and task visibility, not reference-equivalent quality. Natural human/robot imagery, real AI/Excel interactions and 16-panel cinematic variation remain missing. Independent Japanese ASR/pronunciation and semantic subtitle alignment, smartphone playback, inherited voice/media publication rights, employee approval, and GitHub Actions billing remain unverified. Next: source/voice rights and independent transcript QA, then approved image-first real-world footage. Manual posting only after approval.
