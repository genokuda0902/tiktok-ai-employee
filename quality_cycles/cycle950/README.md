# cycle950 — 8-scene chapter badge (review only)

## What changed
- Local baseline: cycle948 document clarity MP4, because its actual bytes were mounted.
- Also inspected recent parallel PR #345 (cycle949 action-following spreadsheet cues); this change is distinct from both.
- Replaces tiny top-right 01/08 with a larger, consistently styled STEP 01 / 08 pill and smooth within-scene progress accent.
- Protects all content below y=250, including existing Japanese narration, baked captions, headline, and footer.
- 10 genre accent presets. Hard-coded geometry fails closed on unsupported genres and unexpected frame counts.

## Local MP4 QA (actual media not uploaded to GitHub)
- File: cycle950_STEP_BADGE_JP_HUMAN_REVIEW.mp4
- SHA256: 5c87ee465b19c7aa09cc34b6b69ca261de37f87f61cf68983bde11182f366b92
- H.264, 1080x1920, 30fps, 691 frames, 23.033333s; AAC 48kHz; full A/V decode PASS.
- AAC elementary stream SHA256 identical to baseline.
- Mean absolute pixel difference: badge ROI 23.938, unchanged content ROI 1.084, subtitle ROI 0.178 (re-encode difference).
- Local offline tests: 31/31 PASS. GitHub CI validates code only, not the private local MP4.

## Evidence and limitations
- Research summaries: first 1–1.5s hook, 15–25s, short purposeful beats, legible Japanese subtitles, real examples, before/after and human approval.
- User's 16-panel storyboard referenced through accessible prior notes; original v33 reference MP4 unavailable for direct comparison.
- No independent Japanese ASR/caption semantic timing check, inherited commercial media rights, smartphone device playback, employee approval or actual Actions billing verification.
- No private user media or original reference uploaded to this public repository.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Manual posting only after employee approval. No merge, paid service, or auto-post.
