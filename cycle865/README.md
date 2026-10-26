# cycle865 — remove overlapping first-second graphics (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original reimplementation, not recovered v33 source. No automatic posting, merge, payment, public media upload or external assets.

## Defect and measured improvement

In cycle864, the opening picture region included competing text layers, an English "Macros disabled" warning from a prior spreadsheet capture, and a cluttered question panel. On the original local 1-second frame, the central text and UI overlapped visibly. cycle865 replaces the first **89 frames (0.000–2.967s)** inside x=0..1079/y=330..1449 with a clean three-beat hook: one large question, a legible real Calc table with **fictional** A/B data, and a three-step label. This avoids repeated minor zoom changes. It does not add new cinematic live-action assets or claim a real AI-service demo.

The ten genre hook variants share explicit, unit-tested non-overlapping layout boxes and a fail-closed SHA-pinned private source manifest. Only ai_work was rendered to a complete Japanese MP4; the other nine hooks are code-level tests, not verified finished videos.

## Reproduce privately

Use Python 3.11, Pillow, OpenCV, NumPy and FFmpeg/FFprobe locally. **Do not upload the source MP4, inherited audio, extracted images, private manifest, or output MP4 to this public repo.**

manifest.private.json must equal POLICY in clean_hook.py plus the source file SHA256. Source is the cycle864 private review video, not a published or approved media asset.

    PYTHONPATH=cycle865 python -m unittest discover -s cycle865 -p 'test_*.py' -v
    python cycle865/clean_hook.py --source /private/cycle864_CINEMATIC_LAPTOP_JAPANESE_REVIEW_ONLY.mp4 --output /private/cycle865_CLEAN_HOOK_JAPANESE_REVIEW_ONLY.mp4 --manifest /private/manifest.private.json --report /private/render_report865.json
    PYTHONPATH=cycle865 python cycle865/verify_review.py /private/cycle864_CINEMATIC_LAPTOP_JAPANESE_REVIEW_ONLY.mp4 /private/cycle865_CLEAN_HOOK_JAPANESE_REVIEW_ONLY.mp4 /private/verification865.json

## Verified local technical results (2026-10-26 JST)

- Prior cycle864 SHA256: 5fcccffb4f194457230b06b7135e206d087c6985344d37aa5ff4a1075500c80f.
- Completed cycle865 MP4 SHA256: d4080e6187cdbd6333ffcc6aea9c0b4d7d97872b438ce47a56b2800174e5e6b0.
- 1080x1920, H264/30fps/691 frames/23.033s, AAC48kHz. Full video/audio decode passed.
- AAC ADTS elementary stream SHA256 identical before/after: 2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9.
- Local unit tests: **14/14 PASS**. Opening visual mean absolute pixel delta across sampled frames: 73.551–90.257. Protected caption-region delta 0.012–0.111. Outside modified frames sample delta 0.236.
- GitHub CI runs code unit tests and a **synthetic 1-second** H264/AAC smoke test, NOT the actual private Japanese MP4.

## Research and safety

Consulted accessible summaries of TikTok市場分析 and TikTok動画研究: first 1–1.5s hook, purposeful cuts, actual software demonstrations, readable Japanese subtitles, Before/After, manual employee approval. Complete task/chat transcripts were inaccessible. Directly inspected user-supplied 16-panel ChatGPT×Excel時短術16コマ絵コンテ.png, particularly the opening panel. Original v33 MP4 and generation source were unavailable for direct comparison. Current 8-scene review output is much less cinematic than the 16-panel storyboard.

**Unverified:** speech transcription, pronunciation, spoken Japanese meaning and subtitle alignment, inherited image/audio publication rights, real smartphone playback, staff approval, retention, original v33 parity and actual Actions billing. No claim of reference-equivalent quality or postability. The inherited source is private review-only, with synthetic data and unknown publication rights. No merge or public upload.
