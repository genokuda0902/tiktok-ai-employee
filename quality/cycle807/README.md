# cycle807 — animated fictional KPI evidence panel (review only)

2026-10-24 JST. No purchases, no merges, no publishing, no automatic TikTok posts.

## Provenance and dependencies
- Repo main checked: `18e084c38db0dc55db7dfc0532b9451b1167f2aa` (unchanged).
- This branch is stacked on unmerged Draft PR #105 / commit `bae69f34bc7e83942949c514f7675aaa71aa29df`. Parallel PR #106 adds kinetic captions to a different branch and is NOT incorporated.
- Previous source: cycle806 23.933s 718-frame Japanese review-only MP4 from successful Actions run `40052191577`, artifact `12543508519`. The artifact expires after 7 days; regeneration will require refreshing the approved source chain.
- Past TikTok市場分析 and TikTok動画研究: only earlier summaries accessible (0–1.5s hook, concise 15–25s, operation demonstrations, before/after, subtitle-safe areas, specific CTA). Full task/chat research transcripts NOT accessed.
- User's ChatGPT×Excel 16-panel storyboard inspected via Library. Original reference v33 MP4 NOT accessible this run. No visual quality equivalence claim.

## One distinct cross-genre improvement
The earlier scene 3 displayed three unlabeled-progress bars with no explicit current/target values. This patch animates three explicitly fictional example KPIs with labeled **current and target percentages**, a goal marker and a conspicuous `架空データ` disclaimer. Values: 18/25%, 12/20%, 68/80%. This is not company performance data.

Only scene 3 (frames 179–262, 84 frames / 2.8 seconds) is overlaid. Narration and all original subtitles are preserved. Ten-genre palette contract, one rendered sales_business video.

## Reproduce locally
```bash
python -m pip install Pillow==11.3.0
python -m unittest discover -s quality/cycle807 -p 'test_*.py' -v
python quality/cycle807/evidence_kpi.py --source cycle806_BUSINESS_PACING_REVIEW_ONLY.mp4 --output review_output/cycle807_KPI_EVIDENCE_REVIEW_ONLY.mp4
ffmpeg -v error -xerror -i review_output/cycle807_KPI_EVIDENCE_REVIEW_ONLY.mp4 -f null -
```

Japanese Noto Sans CJK Bold font is required; use `CYCLE807_FONT` to override. FFmpeg and ffprobe are required. CI downloads previous unapproved review-only artifact, does NOT commit binary MP4.

## Local verification before push
- 11 unittest cases passed.
- Output 1080×1920 H.264/30fps, 718 frames, 23.933333s, AAC/48kHz.
- Complete video/audio decode passed; audio elementary AAC stream hash unchanged.
- Output SHA256: `3a9b1b8824ac11d7b345592718808db7e5458fb15b36d99faa7810cbbf9550a8`.
- CI status must be checked separately; no claim until verified.

## Remaining blockers
- No independent Japanese ASR, pronunciation/naturalness, subtitle meaning check, smartphone playback, source voice license review or employee approval.
- v33 source video and full research transcripts unavailable; visual quality still far below cinematic/photorealistic reference.
- HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Employee-approved manual posting only.
