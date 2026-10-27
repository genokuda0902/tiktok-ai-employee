# cycle914 — kinetic missing-data hook (review only)

**Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is an original reimplementation, not recovered v33. No public media, automatic posting, merge or paid service.

## New change versus cycle913
- cycle913 added an animated attention guide over the real Calc screenshot in scene02 (87 frames).
- cycle914 changes **scene01 (frames 0–86, first 2.9 seconds)** to a two-beat original kinetic hook: question → visibly missing June values → source-verification handoff. Fictional 4月/5月 values are 12/8 and 16/9; June remains **unfilled**, never fabricated. This is an editorial graphic, not recorded software use.
- Retains all later seven scenes, inherited Japanese AAC audio and burned-in caption area. The first scene headline and its original narration have **not** been independently semantically aligned.
- Ten genre IDs share source-pin, safe-area, palette and review-only guards. Only **ai_work** was rendered as a complete private MP4.

## Reproduce locally with private source only
Requires Python 3, Pillow, NumPy, FFmpeg, and Noto Sans CJK fonts. Keep source, frames, audio, verification JSON and completed MP4 out of public GitHub.

```bash
python3 -m unittest discover -s review_cycles/cycle914 -p 'test_cycle914.py' -v
python3 review_cycles/cycle914/kinetic_hook.py \
  --source /private/cycle913_GUIDED_REAL_CALC_REVIEW_ONLY.mp4 \
  --expected-sha 5a89bcbc8bdb477c1ac70544ba391e9b1f59cd90a5e789a8b8389c571e3e4eb0 \
  --genre ai_work \
  --frames /private/cycle914_frames \
  --output /private/cycle914_KINETIC_DATA_HOOK_JAPANESE_REVIEW_ONLY.mp4
```

## Local result, 2026-10-28 JST
- Source SHA256: `5a89bcbc8bdb477c1ac70544ba391e9b1f59cd90a5e789a8b8389c571e3e4eb0`
- New private MP4 SHA256: `c8fad3896247c97a0a0fab3c2d442f910fd34293f8fb1b6bc4d9d543a85c45e1`
- H.264 1080×1920, 30 fps, 691 frames / 23.033333s, AAC 48 kHz; full A/V decode PASS.
- AAC ADTS SHA256 identical source/output: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Changed opening region: 87/87 frames with quarter-scale MAE >2, min 32.61; non-target max 1.30, protected subtitle region max 0.638.
- Local offline unit tests 14 PASS. GitHub CI tests source and privacy rules only, **not the private full MP4**.

## Research, reference and remaining gates
Consulted accessible summaries of `TikTok市場分析` and `TikTok動画研究`: strong first 1.5-second hook, purposeful cuts, genuine software demonstrations, Before/After, readable captions, manual employee-approved posting. Full original chat transcripts unavailable. Directly inspected the user's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` via Library. Original v33 MP4 unavailable for direct comparison.

Reference's cinematic people, 3D robot, live ChatGPT/Excel operations and 16 distinct cuts remain substantially beyond this eight-scene flat graphic. No independent Japanese ASR, semantic/timing subtitle match, source publication rights, actual smartphone playback, employee approval, retention metrics, or actual Actions billing verification. **Not approved for publication.**
