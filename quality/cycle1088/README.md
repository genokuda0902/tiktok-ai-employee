# cycle1088 — truthful chart-to-proof bridge (review only)

Previous cycle1086 rendered real Calc source and 46+29=75 in scene06. This cycle does **not repeat scene06**. It replaces scene05's static chart summary with three progressive computed totals (営業A 46 / 営業B 29 / 合計 75), leading into scene06. This is synthetic data and is **not** evidence of AI productivity gains.

Ten genre color presets share the same layout and explicit data validation. A 49-frame overlay changes frames 380–428 (12.667–14.300s). All drawn pixels are above y=1170; Japanese captions remain below y=1280. Source H264 1080×1920/30fps and AAC 48kHz are required; audio is stream-copied.

This is a **reimplementation, not recovered original v33 source**. The private review MP4/audio are not uploaded to GitHub. Source SHA-256 pinning is fail-closed, but is **not** media rights approval. Inputs must be explicitly synthetic. CI uses synthetic media, not the finished private Japanese video.

```bash
PYTHONPATH=. python3 -m unittest quality.cycle1088.test_chart_total_bridge -v
PYTHONPATH=. python3 -m quality.cycle1088.chart_total_bridge --smoke
PYTHONPATH=. python3 -m quality.cycle1088.chart_total_bridge --source /private/previous.mp4 --source-sha <sha256> --data-json quality/cycle1088/synthetic_data.json --out /private/review_only.mp4
```

Local real MP4 QA: 691 frames / 23.033s / full A/V decode PASS, previous AAC ADTS SHA256 equals new; caption region sampled on all frames max mean pixel difference 0.4217/255; 12 local tests PASS. Input SHA256 c2a296c40f1fe19e99bda2c57c215fb1534f6c7dd81c2afede2dede1492feb73; final output SHA256 f88f92cd900a8968088e03bea1f17730db67ac0853c54e6705458cab70551ca1. The completed MP4 is NOT committed to GitHub.

Research: accessible TikTok市場分析 / TikTok動画研究 summaries and directly inspected user's 16-panel/36s storyboard; original v33 MP4 and complete research chats unavailable. Our 8-scene/23s visual remains less cinematic and less varied. Independent Japanese ASR/semantic caption matching, smartphone playback, source rights, employee approval, and actual Actions billing are unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, auto-post, external media upload, or paid service.
