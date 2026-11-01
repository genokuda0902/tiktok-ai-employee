# cycle1100 — Calc formula-to-total focus (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No confidential images, audio, source video or finished MP4 are stored in GitHub. This is an original reimplementation, not the original v33 engine.

## Change from cycle1098

Previous cycle1098 focused the Writer template's 目的→条件→形式 rows at 17.5–19.9s. This cycle instead addresses a distinct smartphone legibility problem in the **real recorded Calc demonstration** in chapter 03: the formula bar and total cells are too small to follow without a guided gaze. At frames 195–248 (6.5–8.3s), highlight the existing `=SUM(C2:C4)` formula, then the existing fictional totals `46 / 29`. A small header label explains the focus; it is positioned **above** the spreadsheet and does not cover the underlying numbers or Japanese subtitles. No invented data or changed claims.

The same renderer supports ten color presets, a SHA-pinned local source, strict review-only / fictional-data / no-private-data gates, and 14 unit tests. The complete MP4 is rendered for `ai_work` only.

## Private local proof

Source cycle1098 MP4 SHA256: `71be71788fd58ffdf17862d61c4984c6ad5637ea44d4fe277b59748dd4f82cea`.

Output cycle1100 MP4 SHA256: `739599eafb7b2150ade1aa79aeef1dbd4f0390990c6236c33a4cc7ebc8754f54`.

23.033s, 691 frames, H264 1080×1920 30fps; inherited Japanese-tagged AAC 48kHz stereo, ADTS bitstream identical. Full video/audio decode PASS. Frame-by-frame quarter-size comparison: 54 target frames, target picture mean delta 2.3312/255, outside-target maximum mean delta 1.2244/255 (re-encoding noise), subtitle-region maximum mean delta 0.8928/255. These metrics **do not verify Japanese speech/caption semantic alignment**. No smartphone physical playback test.

To render locally with the privately retained review MP4:

```bash
python3 quality/cycle1100/calc_formula_focus.py --source /private/cycle1098.mp4 --source-sha 71be71788fd58ffdf17862d61c4984c6ad5637ea44d4fe277b59748dd4f82cea --out /private/cycle1100.mp4 --manifest quality/cycle1100/manifest.json --report /private/qa.json
```

The GitHub Actions workflow uses **synthetic 9-second H264/AAC only**, not the private finished video. No user-provided media uploaded to GitHub.

## Research / references / release gates

Consulted accessible prior summaries of `TikTok市場分析` and `TikTok動画研究` (strong hook, real UI, short purposeful cuts, legible Japanese captions, manual employee approval). Full original task/chat transcripts inaccessible. Directly opened the user-provided `ChatGPT×Excel時短術16コマ絵コンテ.png` from Library; 16-panel storyboard has cinematic robot/person, real prompt/Excel screens, before-after, CTA. Original v33 MP4 not directly available this run. Current 8-scene 23s video is not v33 quality-equivalent.

Independent Japanese ASR, word-level subtitle synchronization, commercial rights of inherited media/audio, smartphone real-device playback, employee approval, retention metrics, and actual GitHub Actions charges remain unverified. **No merge, public posting, automatic upload, or paid services.**

Next: independent offline Japanese transcription and caption semantic/time alignment, then approval-cleared imagery and stronger narrative before-after. Do not keep redoing decorative UI strokes.
