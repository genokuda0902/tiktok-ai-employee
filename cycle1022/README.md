# cycle1022 — 8-step visual progress + audio-boundary audit (review only)

2026-10-31 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Provenance and baseline
- Main verified: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- Base is open Draft PR #421 / commit `19f13abaf242f007a124893244b87b90c6ee7272`; parallel PR #422 untouched.
- Prior local cycle1020 review MP4 SHA256 `3442c9e039947f625c907f0aba0815466408e46efd549cf9e9be5c2be96e480e`.
- Consulted accessible `TikTok市場分析` and `TikTok動画研究` summaries. Directly viewed user's `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels, 36s, cinematic people/robot, real spreadsheet scenes). Full research chats and original v33 MP4 inaccessible.
- Checked `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py` (still contains `-an`).

## Distinct change vs cycle1020
- cycle1020 redesigned the Japanese subtitle panel and exported 8 human listening clips.
- cycle1022 adds a small **8-stage scene-progress rail** below the title, automatically advancing at the SRT cue boundaries. Original audio and baked subtitle region remain untouched except for video re-encoding.
- Adds **signal-only** per-cue RMS and ±150ms boundary measurements to the QA JSON. This is NOT independent Japanese speech recognition, spoken-word alignment or semantic subtitle verification.
- Ten configurable genre colors; full-length rendered only for `ai_work`.

## Reproduce locally (approved private input only)
```sh
python cycle1022/source/step_rail_audio_audit.py \
  --source /private/cycle1020_CAPTION_PANEL_JP_REVIEW_ONLY.mp4 \
  --srt cycle1022/fixtures/captions.srt \
  --output /private/cycle1022_review.mp4 --report /private/cycle1022_qa.json \
  --genre ai_work --review-only
```

## Actual local QA
- Output MP4 SHA256 `e734bccfc0152c22a11f1f600008067e414bca08d59227c12d29cce3d2437099`.
- H.264 1080×1920 30fps, 691 frames, 23.033s; AAC 48kHz tagged Japanese.
- Full A/V decode PASS; original AAC ADTS payload unchanged. 8 caption cues retained.
- Seven local tests PASS. Sampled 7 frames: rail-band mean difference 24.661–59.791/255; subtitle-band difference 0.665–0.834/255.
- GitHub Actions uses synthetic 2s A/V, not private completed MP4.

## Outstanding gates
Independent Japanese transcription and spoken timing, human listening, source rights, smartphone playback, employee approval, reference parity, and actual Actions charges remain unverified. **Do not post, merge, upload private media, or pay for services.** Employee approval before manual TikTok posting.
