# v33 recovery checkpoint — 2026-09-18

## Verified baseline
- Original completed video: `AI_Jitan_v33_REAL_SPREADSHEET(1).mp4` (available in the ChatGPT session sandbox, **not committed to GitHub**).
- SHA-256: `b190414f6e3e191cea184d80e28ca7a3404d37a3f212eb94964f95b7674ea712`.
- ffprobe duration: 31.553333 seconds; prior inspection: H.264 512x910, AAC audio.
- Source-generation code, original prompts, and scene asset selection remain **unlocated**. A video file alone cannot establish reproducibility.

## Current binding product decisions
- v33 is the quality baseline. Do not regress to v20 or claim the old silent daily pipeline reproduces v33.
- Use high-quality **approved/public-safe images** with zoom/pan/transitions and optional simple video clips (e.g., sanitized spreadsheet demos). Include new narration and synchronized Japanese captions.
- Natural robot motion / Wan 2.2 is explicitly **out of scope**; earlier instructions in PROJECT_HANDOFF.md are superseded by this decision.
- Initial 6 employees; later 100. Employees review, request revisions, and post to TikTok manually. No automatic TikTok posting.

## Security incident / unsafe prototype
- A separate session prototype used `IMG_5805.png`–`IMG_5812.png` and `IMG_5814.png` without public-release approval. User identified these as confidential. Its output `v33_engine/demo_render.mp4` is **DO NOT PUBLISH / DO NOT DISTRIBUTE**.
- Never commit the confidential images, that demo, extracted audio, or original MP4 without explicit approval and a privacy/license review. Do not treat the prototype as a recovered v33 engine.
- Reject unapproved sources by default. No external upload, publication, or employee delivery without authorization.

## Recovery gates (not yet passed)
1. Locate original v33 source code/prompts/scene plan in prior conversation or repository and commit them with provenance; if unavailable, mark any new code a **reimplementation**, not recovered original.
2. Implement a strict allowlist for assets, plus no-private-data and license review; fail closed if approval metadata is missing.
3. Generate a **new-topic** video using approved assets, newly generated narration and synchronized captions, and compare it against v33 on legibility, timing, storytelling, and visual quality. Do not claim virality.
4. Commit exact code, manifest, pinned dependencies, commands, QA outputs and immutable commit SHA; update PROJECT_HANDOFF.md at each milestone.
5. Only after video-quality acceptance, connect employee onboarding, Drive, LINE WORKS, review/revision and performance collection, then verify end-to-end for 6 employees.

This document is a checkpoint, not a claim of completed recovery or equivalence.