# cycle1084 — truthful, auditable total reconciliation (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. This is a reimplementation, not recovered v33 source.

Previous cycle1082 scene06 displayed `46 -> 75` as if an error had been corrected. However the fictional source data show **Sales A = 46, Sales B = 29, total = 75**. The old comparison could mislead viewers. This cycle replaces **scene06, frames 429–519 (14.300–17.333s)** with a three-step reconciliation: A 46 + B 29 = total 75. All totals are calculated from explicit JSON. The image is tagged fictional and does not claim AI accuracy or productivity improvements.

The common renderer uses ten genre palettes, keeps all pixels below y=1280 transparent, and preserves inherited Japanese voice and captions. CI uses synthetic sound and pictures; it cannot prove speech meaning, voice naturalness, publication rights or smartphone playback.

## Reproduce locally (private review files only)

```bash
/usr/bin/python3 -m unittest quality.cycle1084.test_proof_reconcile -v
/usr/bin/python3 -m quality.cycle1084.proof_reconcile --smoke
/usr/bin/python3 -m quality.cycle1084.proof_reconcile --source /private/cycle1082.mp4 --source-sha VERIFIED_SHA256 --data-json quality/cycle1082/sample_data.json --out /private/cycle1084.mp4 --genre ai_work
```

No MP4, extracted frames, confidential images, narration, or private manifests are committed. Prior `TikTok市場分析` and `TikTok動画研究` research summaries were available (hook, purposeful scenes, real UI, readable Japanese captions, manual review). Original full chats and reference v33 MP4 were not accessible in this run. The user's 16-panel storyboard was known from previous direct inspection, but not independently re-opened in this run. The video still has 8 scenes / 23.033 seconds vs storyboard 16 panels / ~36 seconds; cinematic visual quality and independent Japanese narration transcription remain open.
