# cycle1012 — end-card save CTA / private review only

2026-10-30 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Source, change, verification
- Input: private cycle1010 MP4 SHA256 `20e0840d790b458e7a3a406fc3e76b5288fff54ba2c4ccaa0fb4ea6d63cd58ef`.
- Local output: `cycle1012_SAVE_CTA_JP_REVIEW_ONLY.mp4`, SHA256 `fc9abeb4f63929485e1b4cbe5252f3109869ac049c3c77bc86a572b07b65b523`.
- Unlike cycle1010's **opening Before/After spotlight**, this cycle replaces decorative bars at 21.0–23.03s with an animated, original bookmark outline and **「保存して、明日1つ試す」** action CTA.
- End card CTA confined to y1196–1280; red employee-approval banner starts y1290; burned-in Japanese subtitle region starts y1490. The CTA does not assert approval or performance results.
- H.264 1080×1920 30fps, 691 frames, 23.033333s; AAC 48kHz Japanese-tagged. Full video/audio decode PASS. AAC ADTS SHA256 `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e` identical before/after. No selectable subtitle track; burned Japanese captions preserved.
- All 691 frames compared with every-fourth-pixel sampling: caption region max mean pixel difference 0.499/255; approval-banner region max 1.510/255; CTA region peak difference 48.827/255; 59 frames show CTA change >2/255. Pre-CTA max full-frame mean difference 1.352/255 (H264 re-encoding).
- Local 10/10 unit tests PASS. CI workflow checks the tests and a **synthetic two-second H.264/AAC clip only**. Actual private 23s MP4 is NOT on GitHub.
- 10 genre-specific CTA copy presets exist, but only the private `ai_work` source is permitted to render; all other genres fail closed.

## Research, reference and blockers
- Consulted accessible past `TikTok市場分析`/`TikTok動画研究` summaries: strong 0–1.5s hook, short meaningful scenes, Before/After, UI proof, legible Japanese captions, specific save CTA and human-reviewed manual posting. Full original research task/chat text inaccessible.
- Directly inspected user's Library image `ChatGPT×Excel時短術16コマ絵コンテ.png`: 16 panels/~36s, cinematic 3D robot/human scenes, actual-looking ChatGPT/Excel flow, explicit follow CTA. Original v33 MP4 and its original generation source not accessible. Current private video is only 8 scenes/23s; adding a CTA does **not** establish reference parity.
- Offline Japanese ASR not installed/available. AAC language metadata and audible energy do not verify Japanese words, pronunciation, caption meaning, or semantic timing. Publication rights, smartphone playback, employee approval, actual Actions billing, and retention remain unverified.
- No confidential media or reference storyboard committed. No merge, TikTok posting, paid service or external upload. This is a reimplementation, not recovered original v33 source.

## Local reproduction (requires private SHA-matched input)
```sh
python cycle1012/source/save_cta.py --source /private/cycle1010.mp4 --output /private/cycle1012.mp4 --report /private/qa.json --font /path/to/NotoSansCJK-Bold.ttc --review-only
python -m unittest discover -s cycle1012/tests -p 'test_*.py' -v
```

## Next
1. Acquire a legally usable **offline Japanese ASR** model and independently transcribe all eight spoken cues; compare semantic content and timing to burned captions. Do not call VAD/metadata an ASR substitute.
2. Add new rights-cleared cinematic cutaways and more real-operation continuity; test on a phone and obtain employee approval before any manual posting.
