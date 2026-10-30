# cycle1010 — opening Before/After spotlight (PRIVATE HUMAN REVIEW)

2026-10-30 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Verified input and output
- Input: cycle1008 private review MP4, SHA256 `25c38de04d557190dd93ca44211e88364e7629511548dc5ae2ae331ca7981d06`.
- Output: cycle1010 private MP4, SHA256 `20e0840d790b458e7a3a406fc3e76b5288fff54ba2c4ccaa0fb4ea6d63cd58ef`.
- H.264 1080×1920, 30 fps, 691 frames, 23.033333 s; Japanese-tagged AAC 48 kHz, ADTS audio elementary stream SHA256 `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e` identical before/after.
- No embedded selectable subtitle; original burned-in Japanese captions remain. Full video and audio decode PASS; local 11/11 unit tests PASS.
- Original 8 scenes remain 8; this is a **dynamic focus improvement, not new footage**.

## Specific change vs cycle1008
- Added an animated teal outline + opposite-panel dimming to the **actual 0.0–1.5s opening Before/After shot**. 45 frames generated; overlay confined to y280–1250, above subtitle-safe y1280.
- A first local draft wrongly extended spotlight to 2.9s, affecting the following scene. That draft was rejected, timing was corrected to 1.5s, and the final MP4 was regenerated.
- Sampled differences in the focus area at 0.4s / 1.1s were 16.158 / 8.264 mean absolute pixel values (0–255). Sampled caption area mean difference remained below 0.9 (compression drift).
- Video re-encoded with CRF18; AAC was stream-copied without changing elementary data.

## CI, reference, security
- CI uses synthetic 2-second FFmpeg footage only. The actual 23s MP4 and the user reference storyboard are **not uploaded to GitHub**.
- Available summaries of TikTok市場分析/TikTok動画研究 consulted. User's 16-panel ChatGPT×Excel storyboard directly viewed. Full original research chat text and original v33 MP4 not directly accessible.
- Reference has cinematic human/robot visuals and ~16 panels / 36s; current result is 8 scenes / 23s, not parity.
- No offline Japanese ASR model available; speech semantics, pronunciation, cue timing **not independently verified**. Audio codec/language metadata is not proof of spoken Japanese.
- Source rights, mobile playback, employee approval, and actual GitHub Actions billing not verified. No merge, auto-post, paid contract, public private-media upload.
- Ten genre identifiers; only ai_work private input allowed, all others fail closed.

## Reproduction
```sh
python cycle1010/source/spotlight_review.py --source /private/cycle1008.mp4 --output /private/cycle1010.mp4 --report /private/qa.json --review-only
python -m unittest discover -s cycle1010/tests -p 'test_*.py' -v
```
Requires locally installed FFmpeg, FFprobe, Python, Pillow and exact pinned private input SHA. No source media is stored in GitHub.

## Next
1. Obtain an offline Japanese ASR model and verify transcript against all eight burned-in subtitle cues, without uploading private audio.
2. Replace repeated imagery with approved distinct scenes and real task UI cutaways, then compare reference quality with human review.
