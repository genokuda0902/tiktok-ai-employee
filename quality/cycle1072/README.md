# cycle1072 — cinematic hook rim-light (REVIEW ONLY)

This cycle adds subtle moving bokeh and a short orbit glint around the existing robot in **0.000–2.900 s**. It does not rewrite subtitles, speech or any later scene. It is distinct from cycle1070's scene-04 typed CSV example and from concurrent cycle1139's whole-scene camera push-in. This is a reimplementation, not recovered v33 code.

## Reproduce locally

```bash
python -m unittest quality.cycle1072.test_scene_light -v
python -m quality.cycle1072.scene_light --source /path/to/approved_source.mp4 --source-sha256 EXPECTED_SHA256 --out /path/to/review_only.mp4 --genre ai_work
```

CI uses synthetic video only; do not commit or upload the real review MP4, private images or extracted audio. The SHA256 allowlist must be provided by the operator. All ten genres are supported via a palette, with captions and top question protected by bounding geometry. Source is not a recovered v33 master.

## Quality limitations

A valid video, tests, and acoustic energy checks do not prove semantic speech-to-caption alignment. Independent Japanese ASR, phone playback, release rights, human approval, and comparison with original v33 MP4 remain unresolved. Publication is prohibited; employees manually post only after approval. No paid service or automatic merge.
