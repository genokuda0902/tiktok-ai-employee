# cycle860 — evidence-based animated chart scene (REVIEW ONLY)

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Original reimplementation; not recovered v33. Stacked on unmerged PR #204, not merged to main. Parallel PR #205 remains unmerged.

## Change vs cycle858

- Replace picture inset **frames 170–250 (81/691, 5.667–8.367 s)** with a NEW animated data visualization: sales A values `12,16,18`, sales B values `8,9,12` for April–June; animated two-series bars and factual totals **A=46, B=29**. These are the same fictional numbers visibly present in the later real Calc scene, not actual employee results.
- Source had a largely static screenshot of the same table. The new visual demonstrates a possible **completed-output example** and is a distinct visual type, not another zoom, progress bar or cut-transition adjustment.
- 10-genre reusable palette and fail-closed SHA-pinned source manifest. Original 1080×1920 picture region x=86..993/y=476..1233 only. Headline and burned-in Japanese subtitles remain outside this region. Source Japanese AAC elementary stream copied losslessly; the content and semantic alignment are **not** independently transcribed or approved.
- Private finished MP4 is available **only** in the ChatGPT review sandbox, not on GitHub. CI runs unit tests and synthetic FFmpeg only; it never fetches or generates the private Japanese video.

## Private local reproduction

```bash
python -m pip install 'Pillow>=10,<13'
PYTHONPATH=cycle860 python -m unittest discover -s cycle860 -p 'test_*.py' -v
python cycle860/chart_story.py \
  --source /private/cycle858_BEAT_ALIGNED_DETAIL_JAPANESE_REVIEW_ONLY.mp4 \
  --output /private/cycle860_CHART_STORY_JAPANESE_REVIEW_ONLY.mp4 \
  --manifest /private/manifest.private.json \
  --report /private/qa860.json
```

`manifest.private.json` must contain `POLICY` from the script plus the exact `source_sha256`. The input MP4, finished MP4, extracted audio, private manifest, frames, and source rights evidence must not be committed.

## Research and unresolved gates

- Consulted accessible summaries of `TikTok市場分析` and `TikTok動画研究`: 0–1.5 s hook, purposeful beats, real software demonstrations, Before/After, readable Japanese captions and employee-reviewed manual posting. Original research task/chat full text inaccessible.
- The user-supplied `ChatGPT×Excel時短術16コマ絵コンテ.png` was **directly opened and inspected** this run. Panels 7–8 illustrate spreadsheet-to-chart storytelling. Original v33 MP4 was unavailable for direct comparison. Both are unverified as actual side-by-side references in this cycle.
- Confirmed main `18e084c38db0dc55db7dfc0532b9451b1167f2aa`, open unmerged PRs, `PROJECT_HANDOFF.md` and `recovery/v33/RECOVERY_STATUS.md`. Original v33 generation code remains unlocated.
- Remaining gaps: cinematic people/lighting, 16 unique reference panels, independent Japanese speech-to-caption semantic QA, inherited media/voice rights, mobile playback, employee sign-off and actual Actions billing. No claim of equivalent reference quality, retention uplift or publication readiness. No merge, paid service, confidential asset upload or auto-post.
**Local completed MP4 SHA256:** `ae3966da37aebaa243f201bbbcdf967db1167e650fbfb3b2eac6bde704b501c0` (not uploaded to GitHub).
