# cycle968 — mobile-readable prompt anatomy (REVIEW ONLY)

Distinct from cycle966's Calc formula proof and parallel cycle967's audio meter. Replace only scene04, frames 261–347 (8.70–11.60 seconds), with an original deterministic, high-contrast three-step prompt design: **目的 → 条件 → 出力**. Label this as an illustration, not a ChatGPT screen recording. Preserve the inherited burned Japanese subtitle region at y>=1490 and copy the Japanese AAC bitstream.

This is a reimplementation, NOT recovered original v33 source. The private MP4 is deliberately absent from public GitHub. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.

## Local reproduction (never upload the private source)

Requires Python 3.11+, numpy, Pillow, opencv-python-headless, ffmpeg and Noto Sans CJK Japanese fonts.

    python -m unittest discover -s cycle968 -p 'test_*.py' -v
    python cycle968/prompt_clarity.py --source /private/cycle966_REAL_CALC_PROOF_JP_REVIEW_ONLY.mp4 --output /private/cycle968_PROMPT_CLARITY_JP_REVIEW_ONLY.mp4 --report /private/cycle968_render.json
    ffmpeg -v error -xerror -i /private/cycle968_PROMPT_CLARITY_JP_REVIEW_ONLY.mp4 -f null -

The GitHub Actions workflow creates its own synthetic 3-second MP4; CI does NOT have access to the private completed Japanese video.

Ten genre palettes are defined. Only AI-work has a reviewed scene layout; the other nine fail closed. This is not evidence of ten rendered genres.

## Verified private local MP4 (2026-10-29 JST)

- Input cycle966 SHA256: afa207d9b22dc40ab4ba24c765e7b675bb7246332011cc2d91a827713931eb3c
- Output cycle968 SHA256: a777828ff5db82ba1df8e74c4c1f1419b4c893512707435cd3e6c17922567bd4
- H264 1080×1920 30fps, 691 frames, 23.033333s, AAC 48kHz stereo language=jpn.
- All A/V frames decoded. Source/output AAC ADTS SHA256 identical: ec98a3476d25362abd58bb40d2298b3a8d2eda3cf673187e4feb78133232c20e.
- Changed scene04: 87 frames, average mean pixel difference 35.323/255.
- Protected subtitle region y>=1490: max sampled per-frame mean difference 1.147/255 (re-encoding only).
- Outside edited scene: max sampled mean difference 1.936/255 (re-encoding only).
- Local 8 unit tests PASS; synthetic 3s render/decode PASS. The private full MP4 is shared in the ChatGPT conversation, not public GitHub.
- Reference: user-supplied 16-panel storyboard inspected; prior market/video research summaries consulted. Full original research chats and original v33 MP4 inaccessible.

Independent Japanese ASR, caption meaning/timing, smartphone playback, rights, employee approval and actual Actions billing remain UNVERIFIED. No auto-post, merge, paid contract or public media upload.