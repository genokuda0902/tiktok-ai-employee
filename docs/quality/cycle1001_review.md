# Cycle1001 — Staged BEFORE → AFTER reveal (review-only)

Previous cycle999 improved the legibility and specificity of the scene-06 Japanese BEFORE/AFTER card. This cycle makes the explanation sequential: for the first 0.60 seconds from t=14.50, the AFTER region shows a short transition cue, then fades out over 0.65 seconds to reveal the existing concrete revision. No change to burned captions, narration or other scenes is intended.

- Source: locally accessible cycle999 23.033-second review MP4, not uploaded to public GitHub.
- New feature: a 10-genre configurable color overlay, transparent outside scene-06 AFTER panel.
- Safety: preserves subtitle region below y=1390; FFmpeg stream-copies original Japanese AAC.
- Tests: 8 local deterministic unit tests; CI additionally creates/decodes a synthetic 1080x1920 30fps H.264/AAC sample.
- Limits: no independent Japanese ASR, no semantic subtitle synchronization test, no v33 direct reference comparison, no commercial rights verification, no smartphone test, no employee approval.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Do not merge, charge or auto-post. Posting only manually after employee approval.
