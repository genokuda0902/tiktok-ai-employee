# TikTok video quality cycle1175 — 2026-11-03 JST

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED** — no automatic posting, merge, paid service, or private media committed.

## Difference from cycle1174
- Chapter 3 now shows three **source-true magnified crops** at 6.16–8.73 seconds: existing formula `=SUM(B2:B4)`, fictional totals `46 / 29`, and human-review status `要確認`.
- All enlarged pixels come from the original source video, not a fabricated UI. Caption area stays protected.
- Early rejected renders showed wrong crop coordinates (dark cells and clipped numbers). The final ROI positions were visually corrected.

## Verified real MP4
- Local file: `cycle1175_SOURCE_TRUE_UI_LENS_JP_REVIEW_ONLY.mp4` (not uploaded to public GitHub).
- Source SHA256: `0a2c63f2100801294d595c4da2edfdd5241b59d8e8b776a497f562f3ab3de1e8`.
- Output SHA256: `9144673657b90a9f732dd0b2ea463e83473a0ea3a2c21a98007592e11e26092c`.
- H264 1080x1920, 30fps, 691 frames / 23.033333s, AAC 48kHz language tag jpn, 3,284,181 bytes.
- Full A/V decode PASS; AAC ADTS source/output bit-identical PASS; 8 equal audio intervals non-silent PASS.
- All 691 frames protected y>=1270 (1/4-resolution): mean MAE 0.07049/255, max frame 0.12988/255; 74 upper-region frames materially changed.
- 6 local unit tests PASS, 9-second local synthetic render PASS. Eight sample scenes visually checked for subtitles.
- Independent Japanese ASR, semantic speech/subtitle accuracy and word-level timing NOT verified.

## GitHub
- Base PR #575, commit `0f3920d9926827650cb6a5a5ad54bd5b69b822f5`.
- Draft PR: https://github.com/genokuda0902/tiktok-ai-employee/pull/577
- Branch: `quality/cycle1175-ui-focus-lens`; main `18e084c38db0dc55db7dfc0532b9451b1167f2aa` at check time.
- GitHub Actions tests only synthetic media, **not** the private completed MP4. Check latest Actions conclusion separately.

## Research and next steps
Accessible summaries of `TikTok市場分析` / `TikTok動画研究` reviewed; user's 16-panel / ~36-second storyboard directly inspected. Full research chats and original v33 MP4 unavailable. Current output is 8 scenes / 23s; it still lacks the reference's cinematic people/robot footage, true operating footage and 16-scene diversity. v33 source code is not recovered. Ten genre palettes share the renderer; ROIs must be reviewed per input and rights-approved per asset.

Next priority: offline/free Japanese ASR or explicit human narration/caption audit, then approved real footage and better scene variety. Smartphone playback, source rights, employee approval and Actions actual billing not verified.
