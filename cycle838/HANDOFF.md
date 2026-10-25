# cycle838 — image-only dissolves + objective narration-gap diagnostics (2026-10-25 JST)

## Source of truth / research
- Confirmed main HEAD: `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.
- Stacked on unmerged PR #165 (cycle837) and its HEAD `343424d01363f35d861d88ca26774bc451b3123d`. Parallel PR #164 is unmerged. **Do not merge automatically.**
- Read `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `cycle837/HANDOFF.md`, `cycle833/focal_layout.py`, and the current main workflow.
- Consulted available **summaries** of TikTok市場分析 / TikTok動画研究 (short cuts, readable captions, actual demonstrations, image-first). Full task transcripts were unavailable.
- Inspected the user's 16-panel AI×Excel storyboard. Original v33 MP4 was not available; no direct v33 comparison.
- Binding scope: image-first, approved/public-safe materials; robot animation / Wan 2.2 is OUT OF SCOPE; employee manual TikTok posting only.

## Change vs cycle837
- cycle837: locally drawn fictional Japanese prompt input replaces scene 4 illustration.
- cycle838: **7 scene-boundary dissolves** on the 956×1000 image region only, 8 frames (267ms) each, no video-duration change. Headings and subtitle/CTA safe zones are not composited.
- FFmpeg image extraction and alpha fades are portable across the existing 10 genres using `cycle833.focal_layout`.
- Audio is stream-copied unchanged, not regenerated. The inherited Japanese track remains unapproved for public distribution.
- Objective silence-gap audit added; this is **not speech recognition**, and cannot establish transcript correctness.

## Reproduction
- `PYTHONPATH=. python -m unittest discover -s cycle838 -p 'test_*.py' -v`
- `bash cycle838/ci_smoke.sh` — synthetic FFmpeg test pattern + 440Hz tone, **not Japanese media**.
- Local human-review only: `PYTHONPATH=. python cycle838/transition_review.py --source cycle837_LOCAL_PROMPT_UI_JAPANESE_REVIEW_ONLY.mp4 --out cycle838_IMAGE_DISSOLVES_JAPANESE_HUMAN_REVIEW.mp4 --manifest fictional_manifest.json`
- Manifest must explicitly declare fictional-only, no personal data, no approval, no upload and no posting. Inherited media is NOT committed or uploaded to GitHub.

## Verified locally
- 18 unit tests PASS; synthetic AV smoke PASS; output video and audio full decode PASS.
- Japanese review MP4: H.264, 1080×1920, 30fps, 775 frames, 25.833333 seconds; AAC 48kHz mono stream copied unchanged.
- Audio ADTS SHA256 matches cycle837: `c0fdb1450eea77f8f2a0f08ff07c71469fd275252feea40efc082792805256d9`.
- Review MP4 SHA256: `7dcfa1a2e5d29ed700b781a96640b0f03f586a3dffe800de77feb43ae59d2fb1`.
- At frame 103 (3.43s) image-region MAE vs cycle837 >5, while outside transition at frame 120 (4.0s) MAE <3. Caption-region sampled MAE <3.
- FFmpeg silence detection: 7 pauses of 0.845–0.917s near all 7 scene cuts. **Newly identified pacing issue for next cycle.**
- MP4 shared only in the private conversation sandbox, not in GitHub Actions artifact. CI fixture is synthetic-only.

## Remaining quality and publication gates
- No ASR transcript or word-level Japanese narration/caption timing verification; no smartphone playback; inherited asset/publication rights and employee approval unresolved.
- v33 reference original inaccessible; no quality-equivalence claim.
- Next: prioritize reducing 0.85–0.92s narration gaps **without breaking subtitle sync**, and independent Japanese voice/subtitle audit; continue improving native-HD approved imagery.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No paid API, merge, auto-post, or unapproved external media upload.
