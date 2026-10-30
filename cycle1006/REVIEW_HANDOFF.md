# cycle1006 — arithmetic provenance in the source chart (PRIVATE REVIEW ONLY)

**2026-10-30 JST — HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Difference from cycle1004
- Previous cycle1004: four small corner-bracket focus cues in task/prompt/chart/template scenes.
- This cycle: adds a legible source→sum proof inside the existing 4–6月 chart at **12.95–14.45 seconds**. Explicitly fictional example: 営業A 12+16+18=46; 営業B 8+9+12=29. No invented real performance claim.
- The card is restricted to x75..1005, y972..1166; the Japanese baked subtitle region begins below y1280. No source images, sound, private videos or user reference are committed.
- Ten genre identifiers are present; only ai_work is allowed for private review. Nine other genres fail closed. This is not ten validated outputs.

## Local completed full video (NOT on GitHub)
- Private input cycle1004 SHA256: eafad7ae3e054351846857b87253cad97aff2805ce0e3468ba5dc2aeed5eab0d.
- Private output cycle1006_SOURCE_FORMULA_PROOF_JP_REVIEW_ONLY.mp4 SHA256: cbe0d3e32ca90cb0c3d1cae1d78bfc898bde8a4e0bb47842e4aa6e4e1f446d8e.
- 1080x1920 H.264 30fps; 691 frames, 23.033333 seconds; Japanese-tagged AAC 48kHz; 8 Japanese mov_text subtitle cues.
- Full video decode PASS; full audio decode PASS. AAC elementary ADTS SHA256 unchanged ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e. SRT SHA256 unchanged eecd576cd1968c3b8d422eb5178ca416280a625f499d9eecc519c40b673c7739.
- 15-frame sample QA: card ROI difference 29.57–31.52/255 in full display window, maximum caption ROI difference 0.286/255. 14 local unit tests PASS. Mobile physical playback NOT tested.
- Local private files: cycle1006/output/ (MP4, card PNG, before_after1006.jpg, render_report.json, verified_local.json). Shared in ChatGPT conversation only, NOT publicly uploaded to GitHub.

## Research and reference
- Read accessible prior TikTok市場分析 / TikTok動画研究 summaries: first 1.5-second hook, intentional scene changes, authentic/sanitized UI, readable Japanese subtitles, employee manual approval.
- Directly viewed user's Library image ChatGPT×Excel時短術16コマ絵コンテ.png (16 panels, approximately 36 seconds). The original v33 MP4 and full research chats were inaccessible.
- Current 8 scenes / 23.033s still lacks reference's cinematic person/robot shot variety and continuous demonstration; not equivalent.

## Repo and release safety
- Main at inspection: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Based on open Draft PR #405 head e46672347790338d77e546bbcb4cb028ebe10f23. Parallel PR #406 was open and untouched.
- Reviewed PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, src/build_daily.py and prior cycle1004 renderer/tests.
- CI runs unit tests and synthetic 3-second H264/AAC/Japanese subtitle sample; NOT the real private full MP4.
- Independent Japanese speech recognition, semantic subtitle alignment, commercial rights, smartphone playback, employee sign-off, original v33 parity and actual Actions charges UNVERIFIED.
- No merge, posting, production deployment, paid API, contract, or confidential asset upload.

## Reproduce with an approved local private source
python cycle1006/source/arithmetic_proof.py --source /private/cycle1004.mp4 --output /private/cycle1006.mp4 --card /private/proof.png --report /private/render.json --expected-sha SOURCE_SHA256 --review-only

python -m unittest discover -s cycle1006/tests -p 'test_*.py' -v

python cycle1006/source/verify.py /private/cycle1004.mp4 /private/cycle1006.mp4 /private/verified.json

Next: independent Japanese narration transcription and cue-by-cue semantic/time verification; then approved new-shot diversity and real-phone playback. Do not release without employee approval.
