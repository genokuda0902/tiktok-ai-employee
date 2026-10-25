# cycle844 — image-first question hook (review only, 2026-10-25 JST)

This is a **reimplementation**, not the recovered original v33. Built on the **unmerged** cycle843 PR #174, without merging it or other parallel PR #175. Changes only the first 96 frames (0–3.2 s) of the image panel (x47–881, y334–1040) into a high-contrast, photo-led question hook with gentle push-in and legible Japanese editorial type. The original frame supplies the photo; no external imagery or private data is uploaded. The original baked Japanese captions, narration, scene 2–8, and duration are preserved.

The user-supplied 16-panel storyboard emphasizes a question within 0–2 s, polished imagery, short scenes, demonstration and Before/After. Prior accessible TikTok市場分析/TikTok動画研究 summaries emphasize early hooks, 15–25 s, captions, real operations and human review. **Full task/chat transcripts and the original v33 MP4 were unavailable in this run**, so there is no direct quality parity comparison. The original v33 source/prompts are still missing. No 3D robot/Wan 2.2 generation (explicitly out of scope per handoff).

## Reproduce locally, with fictional review-only source

Python 3.11+, OpenCV, numpy, Pillow, ffmpeg, ffprobe, Noto Sans CJK:

```sh
PYTHONPATH=. python -m unittest discover -s cycle844 -p 'test_*.py' -v
PYTHONPATH=. python -m cycle844.cinematic_hook \
  --source /local/cycle843_REVIEW_ONLY.mp4 \
  --output /local/cycle844_REVIEW_ONLY.mp4 \
  --manifest /local/review_manifest.json --genre ai_work
```

The manifest requires a SHA256 of the exact source and all `REQUIRED` privacy/review flags in `cinematic_hook.py`; missing flags fail closed. `source_rights_reviewed=false` means **not approved for publication**. The 10 genre copy slots are reusable; only `ai_work` was rendered. CI tests and A/V smoke use synthetic media only; the Japanese review MP4 is in private ChatGPT sandbox, not GitHub.

## Local factual results

- Input SHA256: `5fc045b74a2a166e9d9ad928593f5b20587af688bf3d6976cec9a03cffcfb8b0` (cycle843).
- Output SHA256: `31b0c2ca47c08629b9873e12d707c4adc79d1d29b05dcabd246508a831746888`.
- 1080×1920 H264, 30 fps, 691 frames, 23.033s, AAC 48kHz; full video/audio decode PASS.
- Decoded audio PCM MD5 identical before/after: `813f69e5c926b70c927e46e27704e267`.
- 12/12 offline unit tests PASS; synthetic-only GitHub CI must be independently checked.
- At 1.2s: mean absolute pixel difference in changed image region 36.703 /255; subtitle region 0.411 /255 (re-encoding noise). At 4.2s (outside changed interval), image region 0.712 /255.
- **NOT VERIFIED:** independent Japanese speech transcript, word-level caption timing, v33 direct comparison, phone playback, rights/publication permission, employee approval, actual GitHub Actions billing.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, paid service, auto posting or unauthorized distribution.

Next: independent Japanese narration and subtitle semantic/timing audit; richer approved source imagery; smartphone playback and rights review before human-approved manual posting.
