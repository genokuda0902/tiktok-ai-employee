# cycle871 — cinematic photo + offline Chromium template-save demo (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is a reimplementation, not recovered v33. No merge, public/private-media upload, automatic posting, purchase or paid API.

## Actual change vs cycle870
Scene 07 (frames 510–587, 17.000–19.600s) used a cinematic **generated still** with only a three-label overlay. This cycle preserves the generated-photo ambience but composites **26 genuine Chromium screenshots** of a local, synthetic HTML app. Playwright fills Japanese example prompt text and clicks a Save button; a Python-exposed callback writes the fictional prompt to a local text file, which is asserted. This is **not** footage of ChatGPT, Excel or an actual third-party product. Captures are displayed at 10fps inside the 30fps master. The 78 scene frames are newly composited. No new source photo is generated this cycle.

Ten genre headline/action presets share the renderer; only AI-work was rendered as a full private MP4. The existing Japanese AAC and burned-in subtitles are inherited unchanged.

## Reproduce locally (private review)
Requires Python with Pillow and Playwright, locally installed Chromium at /usr/bin/chromium, ffmpeg/ffprobe, Noto Sans CJK fonts. Capture only fictional values:
```sh
python cycle871/capture_offline_browser.py /PRIVATE/frames
PYTHONPATH=cycle871 python -m unittest discover -s cycle871 -p 'test_*.py' -v
```
Supply your **private** prior cycle870 MP4 and **private** approved-for-review photo, and construct a JSON manifest exactly matching `POLICY` plus `source_sha256`, `photo_sha256` and 26 `screenshots_sha256` values. Then:
```sh
python cycle871/photo_ui_proof.py --source /PRIVATE/cycle870.mp4 --photo /PRIVATE/photo.png --frames_dir /PRIVATE/frames --output /PRIVATE/cycle871.mp4 --manifest /PRIVATE/manifest.json --report /PRIVATE/report.json
```
The renderer fails closed on missing media, mismatched hashes, invalid genre, clipping, and overwrite attempts. It does not upload anything.

## Local verified evidence
- Source cycle870 SHA256: `f9a33cc9fde966c37fc5fecb0eb36d747a3686532046e6eb7b6bb026b440d4b8`
- New private MP4 SHA256: `5766f76ead244655350544dc538458c9e7ef46d36d0740ca4b8ce73b1923a65a`
- H264 1080×1920, 30fps, 691 frames / 23.033s; AAC48kHz, inherited ADTS SHA256 `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9` bit-identical.
- Full A/V decode PASS. 78/78 scene frames changed. Caption ROI y1490:1840 checked for all 691 frames, max quarter-sampled mean delta 0.1563. Outside-scene sample max delta 0.3504. Local ten tests PASS.
- The private complete Japanese MP4, photo, browser screenshots and save file are **not committed to public GitHub**. GitHub CI checks unit tests and a synthetic 1s A/V clip only.

## Sources and remaining gates
Accessible prior summaries of `TikTok市場分析` and `TikTok動画研究` reviewed; full chat/task transcripts inaccessible. User's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` directly inspected. Original v33 MP4 unavailable; no direct video comparison or v33 parity claim. Current 8 scenes/23s still differ from 16 storyboard panels/36s in live action, cinematic diversity and production value.

`main` verified as `18e084c38db0dc55db7dfc0532b9451b1167f2aa`. Reviewed `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, `src/build_daily.py`, open PR #223 and #224. Stacked on unmerged #224; parallel #223 not merged.

**Unverified:** independent Japanese speech transcription/naturalness, semantic subtitle alignment, rights of all inherited media and voice, physical phone playback, employee approval, viewer retention, exact GitHub Actions billing. Employee approval and manual TikTok posting only.
