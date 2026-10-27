# cycle884 — 10-genre focal-guidance row spotlight (REVIEW ONLY)

## Research and source
- Accessible historical summaries of **TikTok市場分析** and **TikTok動画研究**: immediate 0–1.5s hook, one clear message, UI evidence, Before/After, readable safe-zone Japanese captions, employee-reviewed manual posting. Original full chat transcripts unavailable.
- Directly viewed user's **ChatGPT×Excel時短術16コマ絵コンテ.png** in ChatGPT Library. Original v33 MP4, its original prompts/source and the cycle882 finished MP4 unavailable for direct video comparison.
- Checked latest main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py`, and open Draft PRs #246/#247/#248.
- This review video builds on **accessible cycle883 MP4** (`595d365549373f0de96ae6e8868725bea038be903bb194a00983b432c0c7b1fc`), not on #247's zoom preview or cycle882's private MP4. Do not claim comparative improvement over those variants.

## Distinct improvement
- Unlike cycle883's seven scene-transition wipes, this cycle animates the **opening scene's four fictional monthly-data rows** with a non-occluding, moving cyan/yellow outline at frames 18, 36, 54, 78. It guides attention while source values appear.
- Only frames 0–88 of the 23.033s/691-frame video are targeted. The inherited audio and lower Japanese subtitle area are not edited.
- Generic `Focus` timeline, geometry/safe-zone validator, 10-genre allowlist and review-only source-hash/policy gate. Other genres must provide their own reviewed frame coordinates and source footage.
- Synthetic local UI is fictional, not live ChatGPT/Excel usage. No time-saving or performance claim is invented.

## Reproduce locally with private source (never upload source/media)
Requires Python 3.11+, Pillow 11.3.0, FFmpeg and FFprobe.

```bash
python -m unittest discover -s video_engine/cycle884 -p 'test_*.py' -v
python video_engine/cycle884/ci_smoke.py
python video_engine/cycle884/row_focus.py \
  --source PRIVATE_cycle883_KINETIC_SCENE_TRANSITIONS_JAPANESE_REVIEW_ONLY.mp4 \
  --output PRIVATE_cycle884_FOCAL_GUIDANCE_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest PRIVATE_manifest.json --report PRIVATE_report.json \
  --work-dir PRIVATE_overlay_dir
```
Private manifest requires `source_sha256` (actual source hash), `synthetic_ui=true`, `review_only=true`, `publication_approved=false`, `external_upload=false`, `automatic_posting=false`, `source_rights_reviewed=false`.

## Measured local QA (private media outside GitHub)
- 1080×1920, H264/30fps/691 frames/23.033s, AAC48kHz. Complete video/audio decode PASS.
- All 691 frames sampled in upper and lower regions: 17/89 target frames have mean upper pixel difference >2; zero of 602 non-target frames exceed 2. Other target frames can still show smaller changes; no claim that every frame changed.
- Max sampled mean subtitle-band difference: 1.0177; max upper-region difference outside target: 1.1936 (re-encode noise).
- AAC elementary bitstream identical to cycle883: SHA256 `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Output SHA256 `1a57acc1d8151c52f53d5b104f7f913a685d07fbaee2bcc5a4cd6a0314680afb`.
- Local 12 unittest tests PASS; synthetic 45-frame H264/AAC smoke PASS. GitHub Actions verifies code/synthetic media, **not** the inherited-audio final MP4.

## Approval and gaps
- Independent Japanese speech transcription, semantic subtitle sync, smartphone playback, source rights, employee approval, original v33 video parity and TikTok retention remain unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid service, private-media upload or automatic TikTok posting.
