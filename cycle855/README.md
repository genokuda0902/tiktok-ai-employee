# cycle855 — evidence-led three-beat opening hook (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original reimplementation, not recovered v33 source. Stacked on unmerged Draft PR #196, **not merged into main**. Parallel Draft PR #197 implements a separate 8-slide editorial route and is not merged.

## Measured change from cycle854

- In scene 01 only, **frames 0–88** (89/691, 0–2.967 s), replace the original dark static desk picture inset with three native 908×758 visual beats: (1) a high-contrast `まだ手作業？` question; (2) a concrete fictional spreadsheet screenshot extracted from the *same source video*; (3) `対象→目的→確認` checklist. Four-frame crossfades avoid hard flash.
- The full output remains 1080×1920, 30 fps, 691 frames/23.033 s. The original upper title and lower Japanese burned-in captions remain outside picture rectangle x=86..994, y=476..1234. The original Japanese AAC elementary stream is copied, not reencoded.
- No external footage, logos, people, employee/customer data or claimed time savings are introduced. The inherited source media's public-use rights are **unverified**. The real Japanese review MP4 is **private in ChatGPT sandbox** and is not uploaded to public GitHub.
- Ten genre palette support, strict SHA-pinned local review manifest, fail-closed input, no overwriting or automatic posting; 14 local tests plus a synthetic-only CI render. Only `ai_work` was rendered as a full Japanese review video.

## Reproduce with local review source (do not publish)

```bash
PYTHONPATH=cycle855 python -m unittest discover -s cycle855 -p 'test_*.py' -v
python cycle855/hook_evidence.py \
  --source /private/cycle854_CINEMATIC_WORKFLOW_FOCUS_JAPANESE_REVIEW_ONLY.mp4 \
  --output /private/cycle855_EVIDENCE_LED_HOOK_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest /private/source_manifest.private.json \
  --report /private/qa855.json
python cycle855/verify_review.py /private/cycle854_CINEMATIC_WORKFLOW_FOCUS_JAPANESE_REVIEW_ONLY.mp4 \
  /private/cycle855_EVIDENCE_LED_HOOK_JAPANESE_REVIEW_ONLY.mp4 /private/verification855.json
```

Manifest must be exactly `POLICY` from `hook_evidence.py` plus `source_sha256` of the local MP4. No manifest, media, confidential image or audio committed.

## Research, provenance, limits

- Accessed available summaries of `TikTok市場分析` and `TikTok動画研究`: 0–1.5-second visual hook, short purposeful beats, real UI demonstrations, readable Japanese subtitles, manual employee-reviewed posting. Full original task/chat transcripts unavailable.
- Inspected user's `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels, 36 seconds). Opening robot, cinematic photography and 16-scene variety remain unmatched. Original v33 reference MP4 inaccessible; no direct comparison or quality-equivalence claim.
- Checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open PRs including #196/#197, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md` and prior code. Source v33 renderer still not recovered.
- AAC bitstream equality is technical proof of audio preservation, **not** proof of spoken Japanese quality or caption semantic synchronization. Smartphone playback, inherited asset rights, employee approval and GitHub Actions billing unverified.

No paid API, no purchases, no auto-post, no merges, no public media upload.