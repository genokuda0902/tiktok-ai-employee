# cycle886 — genuine offline browser save action (REVIEW ONLY)

This is a **reimplementation**, not recovered v33 code. Base: unmerged cycle885 PR #251. No merge, no external upload, no automatic posting, no paid API.

## Distinct change vs cycle885
cycle885 animated three task cards in scene02. cycle886 replaces **scene07, frames 510–587** (17.000–19.600 s) with an **actual Chromium DOM interaction** in a locally authored, offline HTML page:
1. fill a Japanese instruction into the textarea;
2. click Verify, calculate fictional A=12+16+18=46 and B=8+9+12=29 using JavaScript `reduce`;
3. click Save, assert the UI status is `保存済み ✓`.

Three **real browser screenshots** are captured after those actions and turned into 78 portrait-video frames. This is not a screen recording of ChatGPT, Excel, or any third-party service. Every screenshot is fictional and has no user identifiers. The 10-genre `Story` copy validation and strict policy/source hash checks are shared; only AI productivity has a full local MP4.

## Local review MP4 — not in GitHub
- Source: cycle885 local review MP4, SHA-256 `5f92fc4a175b762dd0c8188170f725e1fa3175f6542fcafa2306fbcd14c02465`.
- Output: cycle886 local review MP4, SHA-256 `090e9ebe87a2aa8e05beba75b3b4f628f1bbcbf069807e64d2720773c7465d10`.
- 1080x1920, 30fps, H264, 691 frames/23.033 s, AAC 48kHz stereo. Full decode PASS.
- All 78 changed scene frames have sampled upper-frame MAE >5. Max outside-scene upper MAE 1.264, caption band max MAE 1.157, across all 691 frames.
- Source/output AAC elementary ADTS SHA-256 identical `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- Local 12 unit tests PASS including real browser actions and caption-safe overlays.
- GitHub CI uses **synthetic** H264/AAC media, not the inherited Japanese-audio MP4; browser-dependent tests are skipped there unless explicitly enabled with a provisioned Chromium runtime.

## Reproduce locally
Requires Python 3.11+, Pillow, Playwright Python package, installed system Chromium at `/usr/bin/chromium`, FFmpeg, and Noto Sans CJK Bold font.
Create a **private, untracked** JSON manifest with all `POLICY` fields exactly as in `offline_save_proof.py` and `source_sha256` equal to the input MP4 hash. Then run:

```sh
python video_engine/cycle886/offline_save_proof.py --source /private/cycle885.mp4 --output /private/cycle886.mp4 --manifest /private/source_manifest.json --work-dir /private/cycle886_work
CYCLE886_BROWSER_QA=1 PYTHONPATH=video_engine/cycle886 python -m unittest discover -s video_engine/cycle886 -p 'test_*.py' -v
```

## Research, reference and safety
Consulted accessible summaries of `TikTok市場分析` and `TikTok動画研究`: first 1.5s hook, purposeful cuts, real interface evidence, Before/After, readable Japanese captions, manual employee approval. Full chat/task texts unavailable. Directly inspected user's `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels / ~36s); original v33 reference MP4 not accessible. The new scene improves authentic local UI action, **not** cinematic people, original reference parity or 16-cut variety.

Unverified: independent Japanese ASR and pronunciation, word-level/semantic subtitle alignment, inherited media/voice public-use rights, smartphone playback, employee approval, GitHub Actions actual billing. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Keep all private video/audio/screenshots/manifests out of the repository.
