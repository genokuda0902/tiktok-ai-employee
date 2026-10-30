# cycle996 — review-only scene flash guard

**New improvement vs cycle994:** cycle994 raised shadow detail in the center artwork. This cycle detects large brightness jumps at manifest-declared scene boundaries and adds a 5-frame (~0.167 s) feathered dissolve **only** when the mean central-region luma discontinuity is >=55/255. This is a transition/comfort improvement, not a new narration or a v33 reproduction. Original Japanese AAC audio and optional Japanese mov_text subtitle bitstreams are copied without re-encoding. Baked captions/footer/header are excluded from pixel processing, though codec compression may alter them slightly.

## Source / reproducibility

Source video: private review-only `cycle994_SHADOW_LIFT_JP_REVIEW_ONLY.mp4`, SHA256 `b9e99c1b3878815d78bd9c76391fa995739a92b2962909be1eb8b4803f90a443`. Not committed to public GitHub.

Requires local Python 3.11+, `numpy`, `opencv-python-headless`, and free FFmpeg/FFprobe. No paid APIs or external uploads.

```bash
python cycle996/flash_guard.py \
  --input /private/cycle994_SHADOW_LIFT_JP_REVIEW_ONLY.mp4 \
  --output /private/cycle996_FLASH_GUARD_JP_REVIEW_ONLY.mp4 \
  --report /private/cycle996_render_report.json \
  --genre ai_work --cuts 87,174,261,348,435,522,609 --review-only
python -m unittest discover -s cycle996 -p 'test_*.py' -v
python cycle996/ci_synthetic.py
```

Manifest-declared scene boundaries are required. This module does not automatically infer scene cuts or grant asset rights. It refuses unknown genres, missing audio/subtitles, invalid source format, and zero qualifying transitions. The ten genre names are shared QA presets, not ten approved outputs. Only `ai_work` was rendered with private source.

## Evidence and remaining gaps

Local 691-frame 23.033s H.264 1080×1920/30fps MP4 produced; AAC 48kHz and mov_text packet hashes unchanged. Full A/V decode PASS; 8 Japanese subtitle cues extracted. At cuts 174/348/522 the immediate central luma jump dropped by 71.19% / 68.72% / 70.85%. Caption region mean absolute pixel difference max 0.8047/255 on 19 sampled frames. Unit tests 6 PASS; synthetic 2s MP4 test PASS. GitHub Actions validates only synthetic data, not private 23s MP4.

Research consulted: accessible prior TikTok市場分析/TikTok動画研究 summaries (1.5s hook, one message, real UI/Before–After, readable captions, human review); user Library `ChatGPT×Excel時短術16コマ絵コンテ.png` inspected (16 panels, ~36s, robot/person/ChatGPT/Excel UI and CTA). Original v33 MP4 and full research chat transcripts were not accessible in this run. Current 8 scenes/23s still lack the reference's 16-scene cinematic breadth and seamless ChatGPT→Excel workflow.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Japanese narration content has not been independently transcribed; caption meaning/timing, actual smartphone playback, source licensing/publication rights, employee approval, and Actions actual billing are not verified. No merge, auto-post, publication, confidential media upload, paid contract or payment.
