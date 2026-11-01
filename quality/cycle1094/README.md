# cycle1094 — subtle camera push-in on opening hook (review only)

**Difference from cycle1092:** cycle1092 corrected false intermediate totals in scene06. This cycle modifies only the opening hook frames 0–44, applying a smooth 1.00→1.12 digital camera push-in on the robot illustration region (x90–990, y390–1140). The hook title and lower Japanese captions are never overlaid. No new factual claim, source media or audio is added.

This is an original reimplementation, not recovered v33 source. It uses a local, SHA256-pinned private source MP4 and preserves its AAC stream. **Never upload source or output MP4 to public GitHub without media-rights and privacy approval.**

```bash
python3 -m unittest discover -s quality/cycle1094 -p 'test_*.py' -v
python3 -m quality.cycle1094.hook_camera_motion --smoke
python3 -m quality.cycle1094.hook_camera_motion \
  --source /private/cycle1092_STABLE_TOTAL_JP_REVIEW_ONLY.mp4 \
  --source-sha <actual_SHA256> \
  --manifest quality/cycle1094/manifest.json \
  --out /private/cycle1094_HOOK_CAMERA_MOTION_JP_REVIEW_ONLY.mp4
```

The CI renders **synthetic** 2-second H.264/AAC only, not the inherited Japanese review MP4. Ten genre palette presets are validated, but completed real-video QA covers only AI-work. Source media/audio rights, independent Japanese ASR, caption meaning and timing, phone playback, employee approval and actual Actions billing remain unverified. `HUMAN_REVIEW / PUBLICATION_NOT_APPROVED`. No auto-post, paid services, or merge.

## 2026-11-01 local checkpoint (source not published)
- Source cycle1092 MP4 SHA256: `8cd93dadba53243970d18265c404cd556af203385b3532c370935e150cb51306`.
- Output cycle1094 MP4 SHA256: `7baf6bae7d23666b5f1fef7ce051a92838d9248b6587632d51c89c09be31506f`.
- 691 frames, 23.033333 seconds, 1080×1920 30fps H264 + AAC 48kHz stereo; full A/V decode PASS.
- Audio AAC ADTS SHA256 identical source/output: `76801539a721f7d968b5a8bf725fd056ab00de5a74bd09caf50112993c4aa2f8`.
- Frames 0–44 robot camera push-in only. Every third frame compared: hook ROI mean pixel difference 29.261/255; outside-hook ROI mean 0.247/255; subtitle y1490–1840 maximum mean difference 0.511/255.
- Local seven unit tests PASS; synthetic 2s A/V smoke PASS. Source and output remain private local review attachments.
- Directly inspected user's 16-panel `ChatGPT×Excel時短術16コマ絵コンテ.png` from Library; prior research summaries consulted. Full `TikTok市場分析` and `TikTok動画研究` chat texts and original reference v33 MP4 unavailable this run. This hook motion is not comparable to the cinematic person/robot/16-panel reference as a whole.
- Next priority: independent Japanese ASR + eight subtitle meaning/timing comparisons, especially >=20.300s; verify smartphone playback, rights and employee approval. No publication or merge.
