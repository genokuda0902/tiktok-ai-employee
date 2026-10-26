# cycle856 — readable offline prompt (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Original reimplementation, not recovered v33 code. Stacked on unmerged Draft PR #198; parallel #199 photo/subtitle route remains untouched. No merge, no auto-post, no external media upload, no paid service.

## Change vs cycle855

Scene 04, frames **251–335** (85/691, 8.367–11.200 seconds) replaces a cramped local prompt-entry mock with an original offline 2-line Japanese typing animation, large 51px nominal CJK text, 3 progressive constraint chips, and explicit Japanese "no actual AI send" disclosure. The previous mock extended outside the generic picture inset, so the full old UI bounds (x44..1036, y330..1420) are covered, avoiding ghosted duplicate strips. The protected upper title and lower burned-in subtitle region remain outside the replacement.

The actual private Japanese review MP4 is **1080x1920, H.264 30fps, 691 frames / 23.033s, AAC 48kHz**. The source AAC elementary stream is copied bit-identically. No new audio, external image, personal/customer data, brand UI, or productivity claim. Ten genres share the renderer/palettes and content schema; only ai_work has been rendered with the real Japanese review media.

## Local reproduction (private review media only)

~~~bash
PYTHONPATH=cycle856 python -m unittest discover -s cycle856 -p 'test_*.py' -v
python cycle856/prompt_legibility.py --source /private/cycle855_EVIDENCE_LED_HOOK_JAPANESE_REVIEW_ONLY.mp4 --output /private/cycle856_LARGE_PROMPT_JAPANESE_REVIEW_ONLY.mp4 --manifest /private/source_manifest.private.json --report /private/qa856.json
python cycle856/verify_review.py /private/cycle855_EVIDENCE_LED_HOOK_JAPANESE_REVIEW_ONLY.mp4 /private/cycle856_LARGE_PROMPT_JAPANESE_REVIEW_ONLY.mp4 /private/verification856.json
~~~

The local manifest must equal POLICY from prompt_legibility.py plus SHA-256 of the private source. Never commit this manifest, inherited source video, output MP4 or extracted Japanese audio to public GitHub. CI uses synthetic video/tone only.

## Evidence, research and limits

- TikTok市場分析 / TikTok動画研究: accessible prior summaries establish 0–1.5s hook, short purposeful scenes, demonstrative UI, Before/After, safe Japanese captions, human-approved manual posting. Full original task/chat text not accessible.
- User's ChatGPT×Excel時短術16コマ絵コンテ.png was directly inspected (16-panel robot/photo/real Excel reference). Original v33 MP4 not available in current session, so no direct quality comparison.
- Verified main 18e084c38db0dc55db7dfc0532b9451b1167f2aa, PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md, open PRs including #198 and parallel #199, prior code and local cycle855 MP4.
- Local 12 tests pass; full output A/V decode pass; AAC elementary SHA equal; three protected-region checks average 1.19–1.21 pixel difference due to re-encoding. Actual source/output mean difference inside replaced scene 43.8–48.9.
- Independent Japanese transcription/pronunciation, semantic caption alignment, source media rights, smartphone playback, employee approval, reference quality and Actions billing remain unverified. No publishing approval.

Next: independently audit spoken Japanese against caption timing and verify reference comparison with rights-cleared original; improve overall imagery with approved high-quality sources, not just isolated UI frames.
