# cycle1444 — review-only reproducibility checkpoint
Baseline: cycle1443 (12 s, 12 fps, 1080x1920, no narration).
Change: 15 fps output, 12 s, same three-scene original spreadsheet animation; review-only watermark.
Local output SHA-256: 3a51cee5bf8241bbb38657275d3cd8871b2167614678ab33dddd457b8788d668
Local ffprobe: h264 1080x1920. Full ffmpeg decode: PASS. unittest: 3 PASS.
Audio: ABSENT. Japanese voice: NOT IMPLEMENTED. Caption: three timed screen-text segments, no speech synchronization.
Source: local cycle1444/render.py and test_render.py. Full renderer not yet committed: this checkpoint is NOT independently reproducible.
Original reference v33 unavailable for direct comparison. DO NOT PUBLISH.
Next: commit complete renderer and test, add Japanese narration + synchronized captions, make Actions artifact accessible.
