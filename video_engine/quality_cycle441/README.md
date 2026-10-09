# cycle441 — evidence-focus review checkpoint

Date: 2026-10-09 JST. Base main: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.

## Changes
- Introduced 8 genre-neutral focus cues across 4 of 8 scenes, with source-first/answer-second timing.
- Added a 0–0.8s curiosity mask/reveal on the corrected 54万円 figure.
- Previous cycle440 had adaptive two-beat Japanese captions; cycle441 retains them and adds timed evidence spotlights.
- Review MP4 produced in ChatGPT sandbox: `tiktok_cycle441_evidence_spotlight_review.mp4` (20.000s, H.264 1080x1920 30fps, AAC 48kHz).
- MP4 SHA-256: `d44a9c4506fe24a2f67f364442c56c04e15bfa3da0770fe8c4e26ec2401cc74a`.
- Full video/audio decode passed; 43 local regression tests passed (local archive includes baseline tests).
- GitHub PR tests: 7 focus-cue tests; local source is stored separately in the cycle441 ZIP.

## Gaps / strict gates
- No Japanese narration (SFX only), so speech-caption sync is not verified.
- Original reference MP4 was not accessible; user 16-panel storyboard was available.
- The original v33 generator is not recovered; this is a new reimplementation.
- Full renderer is in the conversation ZIP, not in this PR.
- Workflow creation was blocked by tool safety checks; GitHub CI execution has not been confirmed.
- All graphics/data are invented; rights review and human approval remain required.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED; no automatic TikTok posting, paid services or merges.

## Next
1. Restore authorized free Japanese TTS (AivisSpeech/Kokoro), then generate a new WAV and measure scene-by-scene sync.
2. Save full renderer and pinned dependency manifest to the PR, run independent CI.
3. Obtain permitted reference MP4 bytes and compare scene quality visually.
