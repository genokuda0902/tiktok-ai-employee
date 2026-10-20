# cycle708 — animated contrast hook (REVIEW ONLY)

Baseline: cycle707 local MP4; reference: user-provided 16-panel AI時短ラボ storyboard (inspected, **not** reused).
Main HEAD at inspection: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
PR: #64 (draft). No merge or publication.

## Actual change
- 0–2.5s: original vector before/after comparison (paperwork vs animated verified sales bars), instead of static result-first graph.
- Generic `HookCopy` and claim-validation reusable across ten genres.
- No asserted percentage of time saved; fictional sales, simulated interface, and BGM-only labels retained.
- 2.5–20s remains identical to cycle707 in frame-difference QA.

## Local reproducible deliverable
MP4: `cycle708_contrast_hook_BGM_ONLY_REVIEW_ONLY.mp4`, H.264 1080x1920 30fps 20s 600 frames, AAC 32kHz.
SHA-256: `b6b603f081756ccc9d17c36a28cb25f63c2c65895213a41c26b0b685f43d0805`.
Full renderer, video, logs and QA contact sheet: ChatGPT conversation attachment `cycle708_source_video_qa.zip` (not uploaded to GitHub).
Local unit tests: 10 passed; full MP4 decode: PASS.
The code committed here is **only the reusable hook and its standalone tests**, not the complete renderer. The exact local renderer is in the ZIP.

## Unresolved / do not publish
- Japanese spoken narration absent (BGM only), speech-to-caption sync unverified.
- Original v33 reference MP4 not accessible for direct comparison; only user-provided storyboard inspected.
- Full results of historical 'TikTok市場分析' and 'TikTok動画研究' unavailable; task definitions and available guidance consulted.
- GitHub workflow creation was blocked by connector safety checks. No cycle708 CI run or Actions artifact was produced.
- Mobile playback, rights/employee sign-off and human visual approval not verified.
- Existing v33 code still not recovered. This is a reimplementation.

Next: solve free Japanese TTS + timed captions; recover CI workflow write or use an approved workflow mechanism; commit exact full renderer, test and artifact.
