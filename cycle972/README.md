# cycle972 — animated source-data comparison (review only)

## Goal and previous difference
cycle970 had a static 4–6月 source-check table and arithmetic sums in scene05 (11.60–14.50s). This cycle replaces that scene's **artwork only** with an original three-beat grouped-bar comparison (4月, 5月, 6月) and then shows the **exact** 46 / 29 totals. No intermediate false totals. Caption region from y=1240 to bottom is left untouched in decoded source frames.

This is an **original reimplementation**, not recovered v33 source. The visualization uses fictional A=(12,16,18), B=(8,9,12) and is **not** a genuine Excel or ChatGPT screen recording. The latest main was 18e084c; independent PR #372 modifies the finished-report scene and was not touched. This PR is stacked on #371 and should not be merged automatically.

## Reproduce privately
Dependencies: ffmpeg, Noto CJK fonts, numpy, Pillow, opencv-python-headless.

```bash
python -m unittest discover -s cycle972 -p 'test_*.py' -v
python cycle972/chart_reveal.py --source <locally-authorized-cycle970.mp4> --output <private-cycle972.mp4> --report <private-report.json>
ffmpeg -v error -i <private-cycle972.mp4> -f null -
```

Never commit source MP4, extracted audio, private imagery or review output to public GitHub. CI uses synthetic media only.

## Local run evidence (2026-10-30 JST)
- Input: cycle970 review MP4, SHA256 `ebee379a95b4b46ce8f10606262cd6b019e28aad1e8a96b18d73bd1fb563c824`.
- Output: 1080x1920, H.264, 30fps, 691 frames, 23.033333s, AAC 48kHz. SHA256 `ae8ba688c6808ca13df8bd353d16d74ab00b2f98ab87f0a741e48a661cdb9648`.
- Changed frames 348–434; 9 local unit tests PASS; full audio/video decode PASS; original AAC elementary-stream SHA256 equals output `ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e`.
- Sampled caption-region mean absolute pixel difference <=1.115/255 after H.264 re-encode. This is not independent caption semantics or timing validation.
- Japanese speech content independent ASR: **UNVERIFIED**. Smartphone playback, rights, publication approval: **UNVERIFIED**.
- Source code is public-safe; actual MP4 is only in private conversation sandbox. No posting or merging.

## Next priorities
Independent Japanese ASR and subtitle alignment (not merely audio-energy analysis); smartphone review of chart pacing and subtitle readability; comparison to the inaccessible original v33 MP4. User-provided 16-frame storyboard and past TikTok market/video research summaries informed the design, but original full research chats and v33 video were unavailable in this run.
