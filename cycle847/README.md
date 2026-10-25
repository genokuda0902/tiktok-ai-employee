# cycle847 — One-frame subtitle flash guard (review only)

**New issue, not another transition SFX tweak.** Cycle846 preserved 691 frames but its burned-in Japanese caption panel briefly dimmed to near-black on 11 isolated frames. A 1080×1920 frame scan identified exact zero/near-zero bright-text events at frames **28,57,119,199,226,380,463,552,574,633,660** (0.933–22.000s). This is a frame-level visual defect, not a claim about speech meaning.

The new common module detects only **single-frame** caption dropouts bracketed by legible captions with a stable background scene. It copies the previous caption ROI for one frame, leaving non-caption imagery untouched before re-encoding. Persistent missing subtitles and scene cuts are not repaired automatically. It is reusable for ten genre IDs with a configurable ROI; ten genres have NOT been rendered or validated. Source SHA256 and fail-closed review-only manifest are mandatory.

## Verified local review video
- Source cycle846 SHA256: `a4cc272f0f7ffe2d97821236d3143007274762f261d5b5ec5b42bef4b754704b`
- cycle847 output SHA256: `800ba2fca29a2e401baee5e3d0fe98d771eb03e2c6726302f2dac8804220bf1f`
- 11/11 flagged frames now show readable bright captions; 1080×1920, 30fps, 691 frames, 23.033s, H264+AAC, full A/V decode PASS.
- AAC audio elementary stream SHA256 identical before/after: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 9 local unit tests PASS. Local Japanese MP4 is in the ChatGPT conversation sandbox only, **NOT GitHub**. CI tests synthetic generated frames/audio and source code, not the actual Japanese MP4.

## Run
```bash
PYTHONPATH=cycle847 python -m unittest discover -s cycle847 -p 'test_*.py' -v
PYTHONPATH=. python -m cycle847.subtitle_flash_guard --source /local/cycle846.mp4 --output /local/cycle847.mp4 --manifest /local/review_manifest.json --genre ai_work
```

Dependencies: Python 3.11, numpy, opencv-python-headless, ffmpeg/ffprobe. Source material must be fictional and review-only. No public release rights implied. Prior research: TikTok市場分析 and TikTok動画研究 summaries available; full task chats and original v33 MP4 unavailable. User-provided 16-panel storyboard image was directly reopened and visually inspected this cycle (AI時短ラボ 16話構成ストーリーボード.png): cinematic robot, Japanese hook, genuine-looking AI/Excel workflow, Before/After and CTA; this one-frame fix does not close those visual gaps.

**Remaining:** Japanese ASR/semantic subtitle sync, naturalness, original v33 visual parity, rights clearance, smartphone playback, employee approval. No paid services, merge, auto-posting or external media upload. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
