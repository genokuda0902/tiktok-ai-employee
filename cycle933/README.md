# cycle933 — scene-aware Japanese text clarity (review only)

Base: local verified cycle932 MP4 (23.033s, 1080x1920, 30fps, H.264/AAC).
Changes only scene03 (5.8–8.7s; 87 frames), using edge-weighted local sharpening of the paper/text region, **not** a camera zoom. Ten genres use bounded strength presets. Header, caption, footer, and audio are not intentionally changed; the full video is re-encoded, so minor compression differences are expected.

Run locally:
```bash
python -m pip install numpy opencv-python-headless
python -m unittest discover -s cycle933/tests -v
python cycle933/src/scene_clarity.py --source SOURCE.mp4 --output OUTPUT.mp4
ffmpeg -v error -xerror -i OUTPUT.mp4 -f null -
```

Local verification: 11/11 tests; 691 decoded video frames; H.264 1080x1920 30fps; AAC 48kHz bitstream SHA256 matches input; video duration 23.033s. On scene03 at 7.25s, the measured Laplacian variance in the targeted paper ROI increased ~47.5% (a proxy for edge sharpness, not a human readability score). Actual MP4 is **not committed to the public repository**; CI uses synthetic frames.

Difference from cycle932: previous work added simulated cursor clicks to scene04; this cycle improves the legibility of small Japanese text in scene03. A zoom trial was rejected because it produced ghosted text; the first encode used `-shortest` and lost 3 frames, then was corrected to 691 frames.

Not verified: independent Japanese ASR/subtitle alignment; source v33 direct comparison; inherited material rights; real smartphone playback; employee approval; actual Actions billing.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, paid service, or automatic posting.**
