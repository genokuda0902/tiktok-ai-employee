# cycle1034 — scene 03 → scene 04 caption-safe wipe

Reimplementation, **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No source media, reference images, audio, or finished private MP4 committed to GitHub.

## Difference from cycle1032
cycle1032 completed the fictional April–June chart (A=46/B=29). This cycle adds a **new 11-frame leftward scene-content wipe** at frames 256–266 (8.533–8.900s), from spreadsheet verification to prompt composition. The outgoing scene still is cropped to y=140–1250, so the burned Japanese subtitle panel y>=1490 and audio remain unchanged. This is a small visual transition, **not** the missing cinematic imagery or new voice validation.

## Reproduce locally (only on approved private source)

```bash
python3 -m pytest -q cycle1034/tests
python3 cycle1034/source/scene_wipe.py \
  --source /private/cycle1032_THREE_MONTH_EVIDENCE_JP_REVIEW_ONLY.mp4 \
  --output /private/cycle1034_SCENE_TRANSITION_JP_REVIEW_ONLY.mp4 \
  --report /private/cycle1034_qa.json \
  --expected-source-sha 7dee8f6b1955ae3bc4039590a8bab7e57ed5dc36325886a4fddb7f289b80942b \
  --genre ai_work --review-only
```

GitHub Actions tests **only synthetic 2-second media**, not the completed private MP4. No automatic posting, no merge, no billing operation. 10 genre IDs are accepted by common validator, but only `ai_work` has a verified full private video; others fail closed until approved genre-specific source is available.

## Reference and limits
Prior TikTok市場分析 / TikTok動画研究 summaries: first 1.5s hook, real UI proof, clear before/after, readable captions, manual employee review. User 16-panel storyboard inspected: 16 scenes/~36s, robot/people/cinematic cuts. Original v33 MP4 and full research chats unavailable. Independent Japanese ASR, spoken content/caption semantic sync, source publication rights, smartphone playback, employee approval and actual Actions billing unverified. Do not claim equivalence or publishing readiness.
