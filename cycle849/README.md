# cycle849 — Actual LibreOffice Calc operation inset (REVIEW ONLY)

**Baseline:** cycle848 PR #185, unmerged; local source MP4 SHA256 `86863e799d14b73dacd3524194d8f26ede7f42fa74925e73d89409d0e5bb8de2`.

## New quality issue
The existing scene 05/08, "AIの回答を確認する", used a **static and relatively small Calc screenshot**. A real locally captured LibreOffice Calc GUI recording with a **fictional** three-month A/B dataset replaces the scene's visual inset. A visible cell selection progresses through the rows to the formula results. The original title, burnt-in Japanese subtitle region and AAC bitstream remain unchanged. No real customer/employee information, commercial stock footage or purchased services were used.

**Video difference:** 86 frames (source frames 336–421 inclusive, 11.20–14.07s) contain the new Calc operation footage. All eight scenes remain; 691 frames, 23.033s, 1080x1920, H264/AAC. This is not a claim of reference-level photorealism or improved retention.

## Reproduction
1. Generate the entirely fictional workbook: `python cycle849/create_fictional_workbook.py --output /tmp/fictional_calc_demo.xlsx` (openpyxl).
2. Open it **locally** in LibreOffice Calc in a 1440×900 X display, and record a short 30fps video while selecting rows and the total cells. On Linux, `ffmpeg -f x11grab -video_size 1440x900 -framerate 30 -i "$DISPLAY" -t 3.3 -c:v libx264 -pix_fmt yuv420p /tmp/fictional_calc_capture.mp4`. Do not record real user data.
3. Render with `python cycle849/calc_inset.py --source /path/to/rights-reviewed-local-baseline.mp4 --capture /tmp/fictional_calc_capture.mp4 --output /tmp/cycle849_review.mp4 --report /tmp/cycle849_qa.json`.
4. `PYTHONPATH=cycle849 python -m unittest discover -s cycle849 -p 'test_*.py' -v`.

Requires Python, OpenCV, Pillow, NumPy, FFmpeg/FFprobe and Noto Sans CJK font. The CLI uses a strict source/capture SHA manifest and refuses overwrites or approved/auto-posting flags. This is a **10-genre reusable visual-composition module**, but only `ai_work` has a locally produced Japanese review MP4.

## Provenance and CI limitations
Previously confirmed TikTok市場分析 and TikTok動画研究 **summaries** were consulted; full chat/task transcripts were unavailable. User's 16-panel ChatGPT×Excel storyboard was located, but the original v33 MP4 was not accessible. The reference includes a 3D robot, expressive people, photoreal lighting, real PC UI, a richer 16-shot sequence and strong CTA; this cycle improves **only one actual UI-operation shot**.

The local review MP4 was fully decoded with FFmpeg and is delivered in the ChatGPT sandbox, **not uploaded to GitHub** pending rights review. GitHub CI tests the exact checked-in renderer using **synthetic** video/audio, not the finished Japanese review MP4. Speech transcription/naturalness, Japanese word-level subtitle alignment, source rights, reference parity, smartphone playback, employee approval and actual Actions billing remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, automatic TikTok posting, media upload, purchase, or paid subscription.
