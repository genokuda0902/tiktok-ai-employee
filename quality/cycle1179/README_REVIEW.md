# Cycle 1179 — main-diagram legibility (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No automatic posting, paid service, merge, or unapproved asset upload.

## Change vs cycle1177
Cycle1177 added acoustic-pause-triggered cues near Japanese captions. This cycle instead selectively enhances fine detail in the **main diagram panel** (x=60..1020, y=390..1320), leaving the header, narration/subtitles and footer outside the processed area. The common FFmpeg engine has 10 genre profiles and accepts an explicit, safe panel ROI. It does not change Japanese narration or caption wording.

## Private local result
The actual 22.5s review MP4 was generated locally, **not committed to GitHub**. Source: cycle1177 private MP4; output: cycle1179 private MP4. Both are 1080x1920, 30fps, H264, 675 frames, 22.5s; AAC 48kHz Japanese-tagged audio is bitstream-identical. Full 675-frame decode passed. On 8 sampled scenes at 1/3 phone scale, Laplacian variance in the diagram panel rose by an average 52.23% (46.30% to 58.14%). This is an edge/detail proxy, **not proof of human readability**. Protected region maximum per-frame mean absolute RGB differences (0..255) over all 675 frames: header 0.3582, subtitle 0.2405, footer 0.0904. Local unit and synthetic integration tests: 7/7 PASS.

## Reproduce on private input
```bash
python -m unittest discover -s quality/cycle1179/tests -v
python quality/cycle1179/code/diagram_clarity.py PRIVATE_SOURCE.mp4 PRIVATE_OUTPUT.mp4 --genre ai
```
The CI test generates a **synthetic** 1080x1920 H264/AAC clip and checks audio bitstream identity, decode, ROI bounds and genre coverage. CI does not test the private MP4. No real footage, audio, screenshots or private assets are stored in this PR.

## Limitations and next priority
Japanese independent ASR, pronunciation and semantic caption match remain unverified; local ASR model unavailable. Reference v33 MP4 unavailable for direct comparison; only historical market/video research summaries and 16-panel storyboard summary were available. Smartphone hardware playback, commercial rights, employee approval, viewing retention and GitHub Actions actual billing remain unverified. Do not publish without employee review and manual posting.
