# cycle896 — offline source-evidence magnifier (review only)

Date: 2026-10-27 JST. Source: cycle894 private review MP4, SHA256
`7e423364d2865d22fa0499aa8e716af35732459f142967913e36d5b085f1e0f7`.
This source is **not committed or uploaded**. Original v33 MP4 and source code are not accessible.
This is a reimplementation, not a recovered v33 pipeline.

## Distinct improvement
cycle894 rebuilt final Before/After (frames 588–690). cycle896 instead rebuilds
scene07 frames **510–587 (17.000–19.600s)**. It crops pixels from the actual
offline local browser simulation and displays the verification area enlarged,
alongside native Japanese text: input -> recompute -> save. The fictional values
are A=12+16+18=46 and B=8+9+12=29. This is **not** real Excel/ChatGPT footage.
The crop/high-contrast native-text module accepts ten genre IDs, though only
the AI-productivity video was rendered. Unknown genre/unsafe ROI/PII-like text/
unverified time-saving claims or missing publication flags fail closed.

## Local reproduction (only with authorized, exact-hash source)
Install Python 3.11, Pillow, OpenCV for local audit, ffmpeg/ffprobe and
fonts-noto-cjk. From this folder:

```bash
python -m unittest -v test_proof_magnifier.py
python proof_magnifier.py \
  --source /private/cycle894.mp4 \
  --output /private/cycle896_review_only.mp4 \
  --manifest manifest_local.json \
  --work /tmp/cycle896_frames \
  --report /tmp/cycle896_render_report.json
python verify_local.py --source /private/cycle894.mp4 \
  --output /private/cycle896_review_only.mp4 \
  --report /tmp/cycle896_verify.json
```

## Verified locally
- 13/13 unit tests PASS.
- H.264 1080x1920, 30fps, 691 frames, 23.033s; AAC 48kHz stereo.
- 78/78 target frames visibly different, minimum target MAE 52.609.
- Caption-protected y1490:1840 MAE max 1.125 (visually preserved).
- Untargeted upper-region MAE max 1.220; original AAC elementary stream SHA
  `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9` preserved.
- Full A/V decode PASS. Output SHA256
  `8be7da9de4ad858563713342f47a6c7083810a9d98db6034083aa60c5a8b2946`.

CI tests the code and synthetic video only; it does **not** access the private
completed MP4 or prove Japanese ASR accuracy. The user reference 16-panel
storyboard was directly inspected; original v33 MP4 and full research chats
were not accessible. Still lacks the reference's real-life footage and cinematic
variety. Japanese narration content/pronunciation, subtitle semantic sync,
rights, smartphone playback, employee approval and actual Actions billing
remain **UNVERIFIED**.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, posting, private media
upload, external delivery, paid subscription or billing action.
