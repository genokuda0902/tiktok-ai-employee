# cycle1116 — truthful provenance banner (REVIEW ONLY)

**Base:** unmerged Draft PR #515 / commit `2e012fb4318c6699ec432818d0f2422d6d4b5259`. **Main:** `18e084c38db0dc55db7dfc0532b9451b1167f2aa`.

## Distinct improvement from cycle1114
The prior scene06 displayed a small/low-contrast review warning near the bottom. The new high-contrast banner appears only at **14.300–17.333 seconds**, clearly labeling the numbers as **架空データ｜数値は人が確認** and **社内レビュー用・公開／投稿は未承認**. The 46+29=75 spreadsheet proof and the pre-existing Japanese subtitles are not covered. This improves provenance and review safety; it does not assert that AI independently verified the numbers.

10 genres share one overlay with per-genre accent colors; WCAG contrast against the dark background is checked at >=7:1. Unrecognized genres, source SHA mismatch, source overwrite, unsafe scene timing, missing audio and unexpected video formats fail closed. Japanese AAC is stream-copied without re-encoding.

## Reproduce locally with an authorized review source
```bash
python quality/cycle1116/safety_disclaimer.py \
  --source /private/cycle1114_CHAPTER_HEADER_FIX_JP_REVIEW_ONLY.mp4 \
  --source-sha b5bd9843ef0306ce5df291bfbba242267462985616e00f64d33933947f70549d \
  --out /private/cycle1116_PROVENANCE_BANNER_JP_REVIEW_ONLY.mp4 \
  --report /private/cycle1116_qa.json
python -m unittest discover -s quality/cycle1116 -p 'test_*.py' -v
```

CI creates a synthetic 18-second H.264/AAC clip and tests only synthetic content. The real Japanese MP4 remains in the private ChatGPT review artifact, never GitHub. Source v33 renderer and reference v33 MP4 were not recovered.

## Reference and publication limits
Accessible summaries of TikTok市場分析/TikTok動画研究 emphasize an immediate hook, purposeful short cuts, real UI, Before/After, readable Japanese captions, and employee-reviewed manual posting. Original chat transcripts unavailable. User's 16-panel ChatGPT×Excel storyboard directly inspected; reference has ~36s/16 panels and cinematic robot/human scenes; this review MP4 remains ~23s/8 scenes.

No independent Japanese ASR, speech-caption semantic alignment, mobile hardware playback, inherited asset/voice release-rights check, employee signoff or Actions billing verification. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, payment, auto-post or external private-media upload.
