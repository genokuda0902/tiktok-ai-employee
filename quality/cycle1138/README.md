# cycle1138 — cinematic hero key-light sweep (REVIEW ONLY)

**Independent cycle after cycle1136's seven content-only scene wipes.** This cycle adds a subtle animated cyan key-light sweep to the opening robot subject for 29 frames (0.967 seconds), starting at frame 4. The image is still a 2D reimplementation; this does **not** reproduce the cinematic 3D reference.

## Repeatable free local command

Requires FFmpeg/FFprobe, Python 3.11+, Pillow 10–11, NumPy 1.24–2.x. No external AI or paid API.

```sh
python quality/cycle1138/cinematic_hero_light.py --source /private/previous.mp4 --output /private/new.mp4 --manifest /private/manifest.private.json --report /private/qa.json
python -m unittest discover -s quality/cycle1138 -p 'test_*.py' -v
```

Private manifest must contain exactly: `policy=HUMAN_REVIEW/PUBLICATION_NOT_APPROVED`, `asset_approval=private_review_only`, source SHA256, genre, audited ROI, start frame, sweep frames, RGB light color and max alpha. The source is checked against its SHA. For this review only, the subject ROI was x=110,y=475,w=670,h=500; frame 4..32, alpha<=0.16. Frame 33 is transparent. The top headline, bottom chapter rail and burned-in Japanese subtitles are not overlaid. The original AAC elementary audio is stream-copied.

**Ten genre configurations** (ai/business/money/learning/health/food/travel/beauty/career/life) are validated by the same fail-closed manifest code. Only AI/Excel actual review video was generated. Other genres need individually audited subject ROI, scene cut boundaries and source approval; do not assume this opening geometry is universally correct.

## Verified local result

- Source (cycle1136) SHA256: `fea134e081c44363eb1bf3f8aecac57c4da4ed074efaffaee317eefcec379687`.
- New review-only MP4 SHA256: `4a881fc32e9bd03117801c6c82f9c4e96795b2a172d71be9541d4d5b5eef3f45`.
- H264 1080x1920/30fps, 691 frames/23.033s; AAC 48kHz jpn. Full A/V decode PASS. Audio elementary ADTS SHA256 unchanged: `27c264983af59b982989997b1e7648f703c1610f35d057b17f6346848e3e6a65`.
- Measured robot ROI MAE vs previous at 0.7s: 7.917/255; Japanese caption ROI MAE: 0.216/255; headline ROI MAE: 0.439/255. These are pixel differences, **not** a quality score. Visual comparison checked.
- 12 local tests PASS, including a synthetic H264/AAC/jpn end-to-end render and ten-genre config checks. CI also uses synthetic media, never private real MP4.
- Research: accessible past `TikTok市場分析` and `TikTok動画研究` summaries only (hook within 1.5s, purposeful cuts, real UI proof, Before/After, safe Japanese captions, human review). Full original chats inaccessible. User's `ChatGPT×Excel時短術16コマ絵コンテ.png` inspected: 16 panels/~36s, 3D robot/person/real UI/CTA. Original v33 MP4 unavailable in this run.
- Current 8 scenes/23.033s still lack cinematic human/robot footage and reference variety. Independent Japanese ASR/semantic subtitle match, source rights, smartphone playback, employee approval and actual Actions billing **NOT VERIFIED**.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, auto-post, paid contract, confidential source commit or public upload.
