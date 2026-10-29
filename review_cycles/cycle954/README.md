# cycle954 — review-only document depth-focus

**2026-10-29, distinct from cycle952 and parallel cycle953.**

- Input: private `cycle952_EDITOR_FIELD_FOCUS_JP_HUMAN_REVIEW.mp4`, SHA256 `0f270382d848e9c89d9e75bcad7815fc61f01ca2a9f8c7d5c0f2c04de2dacd82`.
- New effect: in scene03, 5.8–8.7s, blur and tint **only the background outside the example weekly-report document** to separate the paper from surrounding clutter. Fade in/out 0.32s. Keep top headings, existing Japanese burnt-in subtitles and footer outside the effect. 86 scene frames modified.
- Distinct from cycle952 editor field-focus overlay, cycle948 document sharpening, cycle941 zoom/pan, cycle943 review-list scan, and concurrent cycle953 cinematic scene02 replacement.
- Ten genre color/intensity presets are defined; only `ai_work` geometry is manually reviewed and SHA-locked. All other genres fail closed until approved. No publication asset is committed.
- Private output: `cycle954_DOCUMENT_DEPTH_FOCUS_JP_HUMAN_REVIEW.mp4`, SHA256 `07b9442a73ac4b03de9c2b2e8512f5448690a54660e5391b6b97a5c52646de28`.
- Output: 23.033333s, 1080×1920, H.264 30fps, **691 frames**, AAC mono 48kHz bitstream-identical to source, full A/V decode PASS, 13/13 local synthetic tests PASS.
- Example 6.8s measurement: background Laplacian variance 3.401→0.936 (reduced high-frequency distraction). Paper text area mean pixel difference 1.976/255, subtitle region 0.919/255 (recompression). These are engineering metrics, not viewer preference or v33 quality proof.
- Recovery log: first encode had 690 frames due to `-shortest`; removed `-shortest` and rerendered to 691. Initial paper mask blurred its right edge; expanded protected paper polygon and rerendered.
- Research referenced: accessible summaries of TikTok市場分析 / TikTok動画研究, user's 16-panel storyboard notes (hook, concrete work demonstration, before/after, readable Japanese captions). Original v33 MP4 and full research transcripts unavailable for direct comparison.
- Unverified: independent Japanese ASR, speech/caption semantic or timing match, inherited source commercial rights, original v33 quality parity, smartphone hardware playback, employee approval, actual GitHub Actions billing.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, public MP4/source media upload, automated posting, new paid contract, or charge.

## Reproduce privately

```bash
pip install numpy opencv-python-headless pytest
pytest -q tests/test_scene_depth_focus.py
python scene_depth_focus.py --source /path/to/approved_private_cycle952.mp4 --output /private/review.mp4 --genre ai_work
```

Renderer requires the exact SHA-locked source. CI only runs synthetic tests and cannot prove output video or rights.
