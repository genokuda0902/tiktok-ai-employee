# cycle1074 — three-task visual organization, review only

This is an original, **10-genre reusable** animated vector illustration (three scattered documents → ordered task stack) at 2.900–5.800 seconds, scene 02. It is distinct from cycle1072's opening rim light and concurrent PR #474's subtitle-safe zoom. The original narration and eight burned-in captions remain unchanged. No confidential media is committed.

## Local reproduction

```bash
python -m unittest quality.cycle1074.test_task_stack -v
python -m quality.cycle1074.task_stack --source /path/to/review_source.mp4 --source-sha256 EXACT_SHA256 --out /private/review_only.mp4 --genre ai_work
```

The script fails closed if source hash, format, or duration differs. CI runs a 6-second synthetic H.264/AAC video only, not the private completed MP4. Do not post. Independent Japanese speech transcription, semantic subtitle match, original v33 MP4 comparison, release rights, and phone playback remain unverified. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
