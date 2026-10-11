# Cycle509 — synthetic spreadsheet proof / HUMAN_REVIEW

## Verified local output (2026-10-12 JST)
- Base: cycle508_semantic_beats_REVIEW_ONLY.mp4 (not in repository)
- New 7.5–15.0s: simulated spreadsheet cells, typing `=SUM(B2:B5)`, result 720, animated bar chart.
- Input numbers are fictional: 120+150+200+250=720. This is **NOT** a real Excel capture or a measured time-saving claim.
- Output: 20.00s, 1080x1920, H.264/AAC, 30fps, full decode PASS.
- Japanese screen captions retained (16 intervals); **Japanese spoken narration NOT AVAILABLE**, sync NOT VERIFIED.
- SHA-256 of local MP4: `e39aa5acb350f3993c20e49b29a4593c77dec3a1a9c21d8b95c961ec5a7a26c4`.
- QA: 34 local pytest tests passed. No CI claim without workflow run evidence.

## Source and reproducibility
Full local generator, manifest, tests, video, and QA evidence are in the cycle509 ZIP delivered in the ChatGPT conversation. The repository files here provide the shared fail-closed manifest and quality gate; **they do not reproduce the full MP4 without the local generator and the cycle508 base video**. Do not claim end-to-end reproducibility from this branch alone.

## Safety
Reference v33 original and unapproved/confidential imagery are NOT committed. No auto-post, no merging, no publishing, no paid API. All outputs remain review-only pending human quality and rights approval.

## Next step
Use existing free Japanese TTS workflow on a permissioned Actions runner; generate new speech, align actual words to subtitle timecodes, verify audio before enabling approval. Verify source MP4 rights independently.
