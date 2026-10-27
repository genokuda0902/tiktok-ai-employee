# cycle894 — Before/After proof, review only (2026-10-27 JST)

## Prior and improvement
- Prior **cycle892**: scene 02 frames 89–169 showed three repeated monthly spreadsheet tasks; source MP4 SHA256 `2577cc9bf686a956b35e543002826d13031eb5e7be7cbc35439772b0bcff75af`.
- This cycle changes **scene 08 frames 588–690 (103 frames)** to a staged comparison: manual transfer/sum/check vs reusable instruction/organize/source-check. The effect is NOT measured; the source UI and all numbers are fictional.
- User reference is a 16-panel/36-second ChatGPT×Excel storyboard with explicit Before/After, human and robot imagery, and actual-looking UI operations. Our output is still 8 scenes/23.033s, synthetic UI, not reference-equivalent.
- Past TikTok市場分析 and TikTok動画研究 summaries consulted: hook <1.5s, one idea, real operation, Before/After, short readable captions, specific CTA. Full original chats and v33 original MP4 unavailable. User's 16-panel storyboard directly inspected in this run.

## Actual local completed MP4 (NOT in GitHub)
- `cycle894_BEFORE_AFTER_COMPARISON_JAPANESE_REVIEW_ONLY.mp4`
- SHA256 `7e423364d2865d22fa0499aa8e716af35732459f142967913e36d5b085f1e0f7`
- H264 1080×1920, 30fps, 691 frames, 23.033333s; AAC stereo 48kHz.
- Full A/V decode PASS; 103 changed target frames (minimum target MAE 29.859).
- All 691 frames caption band y1490:1840 comparison max MAE 1.228; outside-scene max MAE 1.134.
- AAC elementary stream SHA256 preserved `2c05bdc4811714429a8f32a40be6776e916653efdb2ebedae143dacfcd3900b9`.
- 12 local unit tests PASS. GitHub CI uses **synthetic 2s A/V only**, not the completed private MP4.

## Reproduce locally only after verifying source permissions
```bash
python quality/cycle894/before_after_comparison.py \
  --source /path/to/cycle892_REPEATED_TASK_WORKFLOW_JAPANESE_REVIEW_ONLY.mp4 \
  --output /private/path/cycle894_BEFORE_AFTER_COMPARISON_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest /private/path/manifest_local.json \
  --work /private/path/frames \
  --report /private/path/render_report.json
```
Manifest requires `source_sha256`, ten-genre ID, three before/after steps, and fail-closed policy fields.

## Not verified / release policy
- No independent Japanese ASR, semantic or word-level subtitle timing validation; inherited AAC bytes matching does not prove natural pronunciation.
- Rights/publication approval for inherited media, smartphone playback, employee sign-off, original v33 video comparison, and Actions actual billing remain unverified.
- **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, auto-post, public/private-media upload, paid API, or contract. Final MP4 is supplied only in the private ChatGPT conversation, not GitHub.
