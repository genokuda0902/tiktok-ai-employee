# cycle837 — offline fictional prompt-input demonstration (2026-10-25 JST)

## Baseline and research
- Latest main observed: 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
- Stacked on unmerged PR #162 / commit 877926f43835c3a78326eaafdc23294fd53865c7. Do not merge automatically.
- Read PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, cycle836/HANDOFF.md and cycle833 10-genre frame definitions.
- Past TikTok市場分析 / TikTok動画研究 research summaries consulted; full transcripts unavailable.
- User's 16-panel AI×Excel storyboard inspected: especially panel 4 (Japanese prompt input), realistic screen operations, bold captions. Original v33 MP4 unavailable here; no direct v33 comparison.

## Improvement vs cycle836
- Replaces scene 4 (frames 285–383; 9.500–12.800s) of a 25.833s AI-work video.
- Previously a laptop illustration showing a static purpose/condition/example list; now a readable **locally rendered prompt UI** that types a fictional instruction, shows a fictional CSV attachment, and changes the action/status indicator.
- Explicit on-screen provenance: LOCAL WORKFLOW / ローカル再現UI / 実際のAI送信なし. **Not actual ChatGPT, not real browser operation, and not an AI API connection.**
- 10 genre-specific fictional prompts, protected subtitle/CTA zone, fail-closed provenance manifest and offline unit tests.
- Attempted to record Chromium locally, but browser policy blocked file:// and localhost. Abandoned browser capture, used a fully offline Pillow renderer instead. Never claim actual browser capture.
- Reimplementation, NOT recovered v33 engine. Do not commit inherited video/audio/GUI assets; public-use rights are unapproved.

## Reproduce
- Install free ffmpeg, fonts-noto-cjk and Pillow.
- PYTHONPATH=. python -m unittest discover -s cycle837 -p 'test_*.py' -v
- bash cycle837/ci_smoke.sh: synthetic source + sine tone only, not Japanese review.
- Rights-gated local review: python cycle837/prompt_demo_insert.py --demo ui_demo.mp4 --source cycle836_REAL_WRITER_SAVE_JAPANESE_REVIEW_ONLY.mp4 --out cycle837_LOCAL_PROMPT_UI_JAPANESE_REVIEW_ONLY.mp4 --manifest fictional_manifest.json

## Verified local results
- 14 unit tests PASS; synthetic-only AV smoke PASS.
- Japanese review MP4: H.264 1080x1920, 30fps, 775 frames, 25.833333s; inherited AAC 48kHz mono.
- Full audio/video decode PASS; extracted AAC stream SHA-256 exactly matches cycle836: c0fdb1450eea77f8f2a0f08ff07c71469fd275252feea40efc082792805256d9.
- Pixel mean absolute difference at changed 11.6s: 40.013; outside changed interval at 8.2s: 1.152; protected subtitle region at 11.6s: 0.809 (re-encoding drift).
- Local review MP4 SHA-256: 7b5d7e7079f365aca40594f5a19c1326fe9c424cc0c69c1ac7ac98288c02d074.
- Local review video exists only in private conversation sandbox; GitHub Actions artifact is synthetic fixture and is NOT a Japanese review MP4.

## Still unverified / gates
- Speech transcription, pronunciation, Japanese voice-caption semantic match and word-level timing; smartphone playback; inherited asset rights; employee approval; v33 parity.
- Human review required. PUBLICATION_NOT_APPROVED. No auto-merge, paid API, automatic TikTok posting, or publication.
- Next: independent Japanese voice/subtitle audit and native-HD approved imagery; avoid repeating layout-only changes.
