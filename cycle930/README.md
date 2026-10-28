# cycle930 — review-only evidence comparison (10 genres)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is an original synthetic reimplementation, **not** the recovered original v33 engine.

## What changed
Unlike cycle929 PR #313's scene05/08 approval gate and parallel PR #314's keyword ribbon, this cycle replaces **scene06** (frames 435–521; 14.5–17.4 seconds) with a large side-by-side fictional AI draft 17 / source data 18, then three sequential stages: find difference → check source → prepare correction. The final card still says **未承認**, never a completed employee approval. The numbers are illustrative, not real financial results.

Source: private cycle929 MP4 SHA256 `1c538feccafd1d9d3339449a549e91c42b1e2415f0adb21b9adeac6ca85c7a1b`.
Output: private review-only MP4 SHA256 `cc9304cb82610e0375e5274c640486d8f6957455f09cfd6a1ad4ed7660698ceb`.

## Local reproduction (private, rights-reviewed media only)
Requires Python 3.11, Pillow 11.3.0, free Noto CJK font and ffmpeg:
```bash
python cycle930/src/scene06_evidence.py \
  --source /private/cycle929_INTEGRATED_HUMAN_REVIEW_ONLY.mp4 \
  --output /private/cycle930_EVIDENCE_COMPARISON_JP_REVIEW_ONLY.mp4 \
  --workdir /private/cycle930_temp \
  --expected-source-sha 1c538feccafd1d9d3339449a549e91c42b1e2415f0adb21b9adeac6ca85c7a1b
python -m unittest discover -s cycle930/tests -p 'test_*.py' -v
```

## Private local technical QA
H.264 1080×1920 / 30fps / 691 frames / 23.033s, inherited Japanese AAC 48kHz ADTS hash identical to source. All video/audio frames decoded. All 87 target frames changed; outside-scene 1/8-resolution max MAE 0.265; subtitle region max MAE 0.232. Local 12/12 unit tests and 12/12 video technical checks passed. The completed MP4 is shared privately in ChatGPT, **not** this public repository. GitHub CI tests synthetic renderer and safety policy only.

## Reference and remaining gates
Directly viewed user's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png`, plus accessible previous summaries of TikTok市場分析 / TikTok動画研究. Original v33 MP4, full research chats, independent Japanese ASR, word-level speech-caption timing, rights clearance, actual phone playback, employee approval, and actual Actions billing are unavailable/unverified. This 8-scene graphic style does not match the reference's cinematic photography/robot and 16-panel diversity. No merge, public posting, automatic TikTok posting, paid service, or private media upload.
