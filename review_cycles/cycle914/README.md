# cycle914 — original paper-report image slide (HUMAN REVIEW ONLY)

## Change and baseline
The newest available actual MP4 for this branch was cycle912 **repetition-calendar** (PR #289). A separate cycle912 Calc variant (PR #290) and cycle913 guided-Calc PR #291 were also inspected. This branch is a different improvement, not a rerun of their Calc annotation: replace scene03, **5.8–8.7s**, with an original high-resolution textured paper-report slide and three animated focus underlines. The content is a fictional example, not a customer record or measured performance. Ten genre-specific title/section/color presets are included; only **ai_work** was rendered as a full MP4.

## Reproduce locally with private input
Requirements: Python 3, Pillow, numpy, FFmpeg, Noto Sans CJK; source MP4 must be supplied separately. No media is committed to this public repository.

```bash
python3 -m unittest discover -s review_cycles/cycle914 -p 'test_policy.py' -v
python3 review_cycles/cycle914/paper_report.py --out /private/cycle914_frames --genre ai_work
ffmpeg -i /private/cycle912_REPETITION_CALENDAR_JP_HUMAN_REVIEW.mp4 \
  -itsoffset 5.8 -framerate 30 -i /private/cycle914_frames/%03d.png \
  -filter_complex "[0:v][1:v]overlay=x=0:y=300:enable='between(t,5.8,8.6667)':eof_action=pass:shortest=0:format=auto[v]" \
  -map "[v]" -map 0:a:0 -c:v libx264 -preset veryfast -crf 19 \
  -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart \
  /private/cycle914_PAPER_REPORT_FOCUS_JP_HUMAN_REVIEW.mp4
```

## Verified local result (2026-10-28 JST)
- Input SHA256: `acf735a060896d584b3b02b8a2e3c6aaa31bc22c24a415c663db730f9d829925`
- Output SHA256: `44ae4f6712db1207e2f805242a9830a4f41fae1cb5b24fff47bc499b35535502`
- 1080×1920 H.264, 30fps, 691 frames, 23.033333s, AAC 48kHz.
- Audio ADTS SHA256 identical before/after: `c2cf7807e183573d74fa7c3f1a719cfb05ccdcb0790ef8d28c2c902640bc197d`.
- Full video/audio decode PASS; 15/15 local QA checks PASS; 11/11 renderer tests PASS.
- Edited scene MAE 50.03 at 1/4 resolution; non-target scene MAE 0.288; caption-band MAE 0.150.
- Actual MP4 is a private ChatGPT review attachment, **not a GitHub CI artifact**. CI verifies source and policy only.

## Research and limitations
Prior accessible summaries of `TikTok市場分析` and `TikTok動画研究`: early hook, purposeful scene changes, legible Japanese captions, real UI/Before-After when appropriate, human approval before manual posting. User's 16-panel storyboard and v33 were inspected in older cycles, but the original v33 file and full original research chats were not directly accessible for this run.

Independent Japanese ASR/caption meaning and timing, inherited media rights, actual phone playback, employee approval, and GitHub Actions billing remain unverified. The new slide imagery is generated entirely from code; inherited video/audio rights are NOT established.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**. No merge, paid services, public MP4 upload, or automatic posting.
