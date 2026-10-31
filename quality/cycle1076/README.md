# cycle1076 — Writer template three-beat review markers (REVIEW ONLY)

Original narrow-gutter animated checks for **purpose → condition → format**, applied only to scene 07 (17.333–20.300s) on an already reviewed video. This guides the viewer through a static real LibreOffice Writer screenshot without pretending to show an actual live operation. The Japanese narration and eight burned-in captions are inherited unchanged. It is distinct from cycle1074's scene-02 document stack and the parallel cycle1143 illustration work.

Ten reusable genre palettes, source SHA256 fail-closed, 18 local unit tests. No third-party images, no private media in source or GitHub CI.

```bash
python -m unittest quality.cycle1076.test_writer_review -v
python -m quality.cycle1076.writer_review --source /private/cycle1074.mp4 --source-sha256 EXACT_SHA256 --out /private/cycle1076.mp4 --genre ai_work
python -m quality.cycle1076.writer_review --smoke
```

CI uses synthetic 21-second H.264/AAC only, not the private completed 23-second MP4. No independent Japanese ASR, semantic subtitle match, rights clearance, smartphone playback, or human publication approval. Do not post or merge without review.
