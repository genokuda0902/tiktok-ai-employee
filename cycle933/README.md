# cycle933 — actual GUI cell evidence lens (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Employee approval and manual TikTok posting are mandatory. This is a new reimplementation, not recovered v33 code or proof of reference parity.

## Improvement compared with cycle932 (PR #318)
The previous scene05 showed a real LibreOffice Calc GUI but cell B4 (blank -> 18) and the recalculated total B5 (28 -> 46) were small on a phone. This cycle adds a **1.51x by 1.62x** evidence inset cropped directly from the real fictional GUI pixels, plus a highlight around the active cell, for all 87 scene05 frames (11.6–14.5 s). The inset does not invent cell values or represent Microsoft Excel/ChatGPT footage. The original burned-in Japanese caption region below y=1260 is protected. Other scenes and original AAC bitstream are retained.

Ten genre-safe palettes and fail-closed tests are included. One full AI-work MP4 was rendered locally. This branch is stacked on unmerged PR #318, which itself is stacked on #315; **no merge**.

## Reproduce privately
Requires Python 3.11+, Pillow, FFmpeg, Noto CJK fonts and the **authorized private** cycle932 source MP4. The source is SHA pinned. Do not commit private videos or confidential media to public GitHub.

```bash
python cycle933/src/evidence_lens.py \
  --source /private/cycle932_REAL_CALC_SCENE05_REVIEW_ONLY.mp4 \
  --output /private/cycle933_REAL_GUI_EVIDENCE_LENS_REVIEW_ONLY.mp4 \
  --workdir /private/cycle933_render \
  --genre ai_work \
  --expected-source-sha 8f186fadd541a74aa1dabf8eff52b131e879d9cda7af0696f2ceb938be62148e
python -m unittest discover -s cycle933/tests -p 'test_*.py' -v
```

## Verified local result (private MP4, not committed)
- Source SHA256: `8f186fadd541a74aa1dabf8eff52b131e879d9cda7af0696f2ceb938be62148e`
- Output SHA256: `fa76d35ce3b9f10fb77436ce6b647577d2e19a69a8cdc11af95437ce11fbbfe8`
- H.264 1080x1920 30fps, 691 frames, 23.033 s, AAC 48 kHz.
- Full audio and video decode PASS. AAC ADTS SHA256 identical: `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 87/87 scene05 frames changed (minimum 1/8-scale mean absolute pixel difference 16.016).
- Outside scene05 maximum 1/8-scale MAE 0.225; protected subtitle band maximum 0.155 (re-encoding difference).
- 11/11 local synthetic unit tests PASS. GitHub CI tests code and synthetic pixels only, not the completed private MP4.

## Reference and remaining blockers
Available TikTok市場分析/TikTok動画研究 summaries consulted: strong opening hook, one message, real demo, legible captions, safe areas, manual review. User's ChatGPT×Excel 16-panel storyboard is known from prior inspection, but its original image and the original v33 MP4 were not directly accessed in this run. Original v33 source and full chats unavailable. Current 8-scene video is still visually simpler than the cinematic 16-panel reference.

No independent Japanese ASR/pronunciation or subtitle semantic/timing validation (no offline ASR model available), no phone playback, no inherited-media commercial rights clearance, no employee approval, and no Actions billing verification. No paid services, automatic posting, merge, or private-media public upload. **Do not publish.**
