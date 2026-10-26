# cycle858 — caption-beat-aligned detail shots (review only)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** This is an original reimplementation, not recovered v33 code. It is stacked on unmerged Draft PR #203 (which itself stacks on #200), **not** on main. Parallel photographic PR #202 is untouched. No merge, paid service, external private-media upload or automatic posting.

## What changed vs cycle857

- Six extra detail-focus shots inside existing scenes 02, 04, 05, 06, 07 and 08. Cut boundaries at frames **118, 276, 379, 458, 551, 634** were selected from the **second Japanese caption beat** in each scene, as recorded in the parallel PR #202 caption-timing manifest. This is an editorial alignment to supplied timing metadata, **not independent ASR or proof of speech sync**.
- **298/691 frames** have a 5.5% inset push-in within x=86..994, y=476..1234; original top heading and bottom Japanese subtitle region are not edited. The original 8 major scenes and existing real fictional Calc/Writer UI recordings are retained; **this does not create 16 unique photographic scenes**.
- H264 1080×1920 30fps 691 frames/23.033s, AAC 48kHz, full AV decode PASS. Inherited AAC elementary stream bit-identical to cycle857, SHA-256 `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`. Output private MP4 SHA-256 `26234506c260c8a60f31578a9f038e5a2f12df8d397326e5df593ad0316b04e0`.
- Six changed samples have mean picture-region pixel differences **25.725–28.866**; subtitle-region differences **0.063–0.133**; five outside-cut frame differences **0.120–0.237** (video re-encoding noise). **17 local tests PASS**, synthetic 2-second local smoke PASS. CI uses synthetic media only.
- Output MP4 and source rights-unapproved media are shared only privately in the ChatGPT sandbox, not uploaded to public GitHub. Ten genre presets and fail-closed policy are implemented; only `ai_work` rendered as a complete Japanese review MP4.

## Reproduction (private inputs only)

```bash
PYTHONPATH=cycle858 python -m unittest discover -s cycle858 -p 'test_*.py' -v
python cycle858/beat_focus.py \
  --source /private/cycle857_COHERENT_CALC_PREVIEW_JAPANESE_REVIEW_ONLY.mp4 \
  --output /private/cycle858_BEAT_ALIGNED_DETAIL_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest /private/review_manifest.json --report /private/qa858.json
ffmpeg -v error -xerror -i /private/cycle858_BEAT_ALIGNED_DETAIL_JAPANESE_REVIEW_ONLY.mp4 -f null -
```

Manifest must be exactly `POLICY` plus `source_sha256` of the source. It is private and must never be committed. CI executes a 2-second **synthetic** video, not the finished Japanese MP4.

## Reference and limitations

- Consulted available previous summaries of `TikTok市場分析` and `TikTok動画研究`: first 1.5-second hook, purposeful cuts, real UI, Before/After, readable Japanese subtitles, employee manual posting. Original task/chat full transcripts were inaccessible.
- Directly inspected user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` (16 panels, 36 seconds). Reference v33 MP4 itself was not accessible for direct comparison. Current video still has eight major scenes, less photographic/cinematic imagery and no validated character performance.
- Checked main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open unmerged PRs including #202/#203, `PROJECT_HANDOFF.md`, `recovery/v33/RECOVERY_STATUS.md`, previous code and MP4. Handoff explicitly cancels animated robot/Wan scope.
- Independent Japanese speech transcription, naturalness, word-level/semantic subtitle synchronization, inherited source rights, phone playback, employee approval and actual GitHub Actions billing **not verified**. No reference-quality or publication-quality claim.

**Next priority:** independent Japanese speech/caption audit; approved high-quality photographic assets and genuinely different shot sources, rather than more zoom-only changes.
