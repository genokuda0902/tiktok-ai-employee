# cycle840 | human review only

## Improvement over cycle839
Restore 7 **photo-only** dissolves from the cycle838 design on the cycle839 repaired 23-second Japanese narration. Previous cycle839 output had abrupt scene cuts because cycle838's private MP4 was unavailable. New transition boundaries are recalculated after seven 12-frame silence trims: 89,170,249,336,422,511,588.

## Local evidence (not stored in GitHub)
- Output: 1080x1920 H.264 30fps, 691 decoded frames, 23.033s; AAC 48kHz, 23.000s.
- Source and output AAC elementary streams SHA256 identical.
- 7 transitions visibly change photo pixels; subtitle region differences due to re-encoding are < 2 mean absolute pixel values.
- Local quality checks: 13/13; Python tests: 6/6.
- Full review MP4 and QA images delivered separately in ChatGPT artifacts. The GitHub CI only checks code; it does not recreate this Japanese MP4.
- Reuses existing AI-generated fictional photo slides. No new independent high-resolution photo assets.

## Safety
Human review / publication not approved. No automatic posting, no merges, no paid services. Final rights review, reference-video comparison, voice naturalness and phone playback remain open.
