# cycle956 — review-only no-generation-loss MP4 finalization

2026-10-29 JST. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**

## Distinct improvement

Unlike cycle954's scene03 background blur, and concurrent cycle955's scene07 content repair, this cycle adds a **shared MP4 finalization stage** for the 10-genre image-first pipeline. It rewrites H.264 VUI color metadata for a *provisional* HD SDR BT.709 interpretation, adds square-pixel SAR 1:1 and Japanese audio-track language (`jpn`), and guarantees faststart packaging **without re-encoding frames or AAC packets**. It does **not** claim perceptual visual improvement or correct master colorimetry; it is a compatibility hypothesis pending source/master and phone-player checks.

## Local evidence

- Input: private cycle954 review MP4, SHA256 `07b9442a73ac4b03de9c2b2e8512f5448690a54660e5391b6b97a5c52646de28`.
- Output: `cycle956_COLOR_TRACK_JP_REVIEW_ONLY.mp4`, SHA256 `c9b4680679977fdf20d139d9106e4ca219fad267595f005f3eb6e00e48a3414d`.
- 23.033333s; H264 1080x1920 30fps 691 frames; AAC 48kHz mono; `jpn` track tag.
- **691/691 decoded YUV frame MD5 hashes identical**, AAC ADTS stream SHA256 identical (`0045ddfb9eb47f798aa6ae3a465f885409dab58ce27ad0fa1479901becddc57d`). Full A/V decode PASS.
- Original video color tags were unspecified. Output tags are BT.709 primaries/transfer/matrix, limited range, SAR 1:1. This is an assumption, not a verified color grade. MP4 `moov` precedes `mdat`; source already had faststart.
- 11/11 local synthetic tests PASS. GitHub CI checks code and synthetic 1-second media only, not the private full MP4.

## Reproduce locally with a SHA-locked private source

```bash
PYTHONPATH=quality/cycle956 pytest -q quality/cycle956/tests/test_playback_metadata.py
python quality/cycle956/playback_metadata.py --source /private/cycle954.mp4 --output /private/cycle956.mp4 --genre ai_work --assume-hd-sdr-bt709 --qa /private/qa956.json
```

Only the AI-work source SHA is registered for review. Other 9 genre source files fail closed until individually reviewed and registered. No user footage, audio, private MP4 or reference video is uploaded to GitHub.

## Research and reference

Accessible summaries of `TikTok市場分析` / `TikTok動画研究` prioritize hook within 1.5s, 15–25s, real UI evidence, purposeful cuts, readable Japanese captions, and employee-reviewed manual posting. Prior user-provided 16-panel storyboard calls for more cinematic imagery, PC operations, Before/After and CTA. Original v33 MP4 and complete research transcripts unavailable for direct comparison. This cycle does not improve cinematic content; it protects already-rendered image and audio quality from another lossy encode.

## Unverified / publication gate

Independent Japanese ASR, pronunciation, speech/subtitle semantic and timing match, correct source/master colorimetry, inherited image rights, smartphone hardware playback, v33 quality parity, employee approval and actual Actions billing remain unverified. No merge, paid contract, private media publication or auto-post. **Employee approval followed by manual posting only.**
