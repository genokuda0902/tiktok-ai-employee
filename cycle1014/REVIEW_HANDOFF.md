# cycle1014 — real soundtrack waveform / human review only

Date: 2026-10-30 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Change from cycle1012
- Prior cycle1012 added a save CTA in the final 2 seconds; its lower-third waveform remained an existing graphic.
- This cycle replaces only the lower audio visualization (x70–1010, y1710–1846) with a 48-bar waveform computed from the **actual decoded AAC soundtrack** using 30Hz PCM RMS. The progress track is computed from video frame count.
- This is an audio-signal visualization, **NOT voice recognition**. Background music or other sounds may also affect bars. It does not prove Japanese narration accuracy, meaning, or word-level caption sync.
- Shared 10-genre registry and fail-closed render policy: only exact SHA-matched local AI-work source can render a private full video; other genres require explicit approved sources. Synthetic-CI mode accepts only a named <=3.1s fixture.

## Verified private MP4, not in GitHub
- Input: cycle1012 MP4 SHA256 fc9abeb4f63929485e1b4cbe5252f3109869ac049c3c77bc86a572b07b65b523.
- Output: cycle1014_REAL_AUDIO_WAVEFORM_JP_REVIEW_ONLY.mp4 SHA256 b27da279d11e07d3c59a4da32038b51b3a61f25c132fa4ac75ca484efa5d2362.
- H.264, 1080×1920, 30fps, 691 frames, 23.033333s; Japanese-tagged AAC 48kHz. Full video/audio decode PASS.
- AAC elementary stream SHA256 ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e identical before/after. No selectable subtitle track. Existing burned-in Japanese text retained.
- Caption ROI y1490–1700 sampled every 15 frames/every 4th pixel: maximum mean difference 0.563/255; waveform ROI y1710–1846 mean difference 38.705/255; top ROI mean 1.196/255 (lossy re-encode).
- 8 caption intervals cross-checked for **audio signal energy only** (fraction >-35dB): 0.724, 0.563, 0.646, 0.667, 0.667, 0.667, 0.652, 0.598. None prove words match captions.
- Local unit tests: 9/9 PASS. CI validates tests and a synthetic 2-second A/V, **not** the private full MP4.
- Private completed MP4 and reference media stay in ChatGPT conversation attachments, not public GitHub.

## Research and limitations
- Read accessible summaries of TikTok市場分析 and TikTok動画研究: early hook, purposeful cuts, readable captions, real UI and manual approval.
- Directly inspected user's Library image ChatGPT×Excel時短術16コマ絵コンテ.png: 16 panels/~36s, cinematic robot/person imagery and UI demonstration. Original v33 MP4 and full research chats were inaccessible. No reference parity claim.
- Checked main PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and src/build_daily.py (still -an silent), latest open PRs including #413 and parallel #414.
- Independent Japanese ASR, caption semantic alignment, source publication rights, smartphone playback, employee approval and actual Actions billing remain unverified.
- No merge, paid API, purchase, external media upload, automatic posting or public release.

## Reproduce with private source and SRT
python cycle1014/source/audio_truth_waveform.py --source /private/cycle1012.mp4 --output /private/cycle1014.mp4 --srt /private/cycle1012_ONSCREEN_TEXT_NOT_ASR.srt --report /private/qa.json --review-only

## Next
1. Obtain legally usable offline Japanese ASR model and independently compare spoken words and timestamps with all eight caption cues.
2. Add rights-cleared new visual scenes and continuity toward reference's 16-scene diversity; smartphone review and employee signoff before any manual post.
