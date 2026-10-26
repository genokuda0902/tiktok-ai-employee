# cycle857 — coherent real-Calc preview (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. Stacked on Draft PR #200; parallel photo route #201 remains untouched. No merge, paid service, public media upload or posting.

## Difference from cycle856

Scene 03 (frames 170–250, 5.667–8.367 seconds) previously used an unrelated Calc screenshot with yellow macro warning, update banner and a different task dataset. cycle857 replaces the picture inset with a larger, focused crop of the **same fictional sales table** already shown in scene 05 (source frame 362). The real Calc capture is reused; no generated AI result is claimed. The three visual beats emphasize the example, rows and totals. The title, original Japanese burned-in subtitle and original AAC are preserved. This makes the story consistent and removes OS chrome, but it does not increase the source footage's native resolution.

The new renderer uses an FFmpeg overlay rather than writing 691 raw 1080×1920 frames through Python, after the first local raw-frame attempt timed out and produced an incomplete MP4. That incomplete file was deleted and replaced; the final output has all 691 frames. Local tests and synthetic CI use ten genre presets, strict source SHA/policy, no-overwrite and fail-closed gates.

## Private local reproduction

```bash
PYTHONPATH=cycle857 python -m unittest discover -s cycle857 -p 'test_*.py' -v
python cycle857/coherent_preview.py \
  --source /private/cycle856_LARGE_PROMPT_JAPANESE_REVIEW_ONLY.mp4 \
  --output /private/cycle857_COHERENT_CALC_PREVIEW_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest /private/source_manifest.private.json --report /private/qa857.json
python cycle857/verify_review.py /private/cycle856.mp4 /private/cycle857.mp4 /private/verification857.json
```

The private manifest is exactly `POLICY` plus `source_sha256` and must never be committed. Source video, derived images, Japanese voice and completed MP4 remain private ChatGPT artifacts, not in GitHub. CI uses only synthetic color/tone and does **not** reproduce the Japanese review MP4.

## Research, reference and limitations

- Consulted available prior summaries of `TikTok市場分析` and `TikTok動画研究`: strong first 1.5 seconds, purposeful cuts, real operation, Before/After, readable Japanese captions and manual posting. Full original task/chat transcripts not accessible.
- Inspected user's `ChatGPT×Excel時短術16コマ絵コンテ.png` via file library. Original reference v33 MP4 unavailable in this run; no direct comparison. The 16-panel reference has cinematic lighting, character acting, rich imagery and more scene variety; this 8-scene review still falls short.
- Verified latest main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open unmerged PRs #200/#201 and earlier, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, previous cycle856 code and MP4.
- Independent Japanese speech transcription, voice naturalness, semantic caption alignment, inherited media rights, smartphone playback, employee approval and actual Actions billing are not verified.

## Next priority

Audit Japanese narration vs subtitles independently; replace more generic graphics with approved high-quality imagery and increase genuine visual variety, not cosmetic frame-only changes.