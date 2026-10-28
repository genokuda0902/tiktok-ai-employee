# cycle943 — 3-beat human-review focus scan (draft, not approved)

**Change from prior separate-route cycle941:** cycle941 applied feather-masked micro-motion to scenes 1/3/7/8. cycle943 improves scene 5 (11.6–14.5 seconds), with 3 sequential, gently faded focus scans over: (1) numbers and evidence, (2) dates and proper nouns, (3) definitive claims. The scan is a *visual inspection cue*, not evidence of approval. Existing unapproved labels and warning remain unchanged.

**Parallel-work check:** PR #332 adds scene 7 reuse microcuts; PR #333 adds scene 8 CTA. Neither is merged here. No duplicate modification of those scenes. This branch starts from main; the local private MP4 is derived from cycle941 review video, so the code alone is not a fully reproducible standalone film without that source.

**Local video QA (not CI):** source `cycle941_SAFE_MICROMOTION_JP_HUMAN_REVIEW.mp4`, source SHA256 `7ce4c7691384a594e9bd7789ab95e086ae78a8969e4181ef0bb43d7d7b60e508`; output `cycle943_REVIEW_SCAN_JP_HUMAN_REVIEW.mp4`, SHA256 `100b913c4a59748f511587d33873d6cd2a4bc9199bae556fca2d09f20b3764ab`. 1080×1920, H.264, 30 fps, 691 frames, 23.033s, AAC mono 48kHz. Full audio/video decode passed; original AAC elementary stream identical. 87/87 frames processed in scene 5, 29 per beat. Source-to-output re-encode produces small changes outside focus region; subtitles/warning text were not intentionally edited. 15 local tests pass. 10 genre palettes are configured; only AI-productivity genre was rendered. Private MP4 is shared only through ChatGPT, not committed to this public repository. GitHub CI tests code and synthetic frames, **not** the actual private video.

**Research basis:** accessible summaries of TikTok市場分析 and TikTok動画研究 (one message, readable Japanese captions, purposeful 6–10 beats, first 1.5s hook, 15–25s total, safe zones, human approval) and prior user's 16-panel storyboard description. Original v33 video and complete original research chat transcripts not accessible for direct side-by-side comparison.

**Still unverified:** independent Japanese ASR/semantic caption sync, subjective narration quality, commercial rights of inherited visuals, real-phone playback, reference v33 parity, employee approval, actual Actions billing. No claim of publication-ready quality. No payment, media upload, auto-post, or merge.

## Local commands

```sh
python -m unittest discover -s cycle943/tests -v
python cycle943/src/review_scan.py --source SOURCE.mp4 --output review.mp4 --report report.json
```

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Employee approval, then manual posting only.**
