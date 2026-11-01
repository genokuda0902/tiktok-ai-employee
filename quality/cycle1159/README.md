# Cycle1159 — Spreadsheet-style teaching demo (HUMAN_REVIEW)

**Change vs cycle1157:** Chapter 03 replaces a static illustrative chart with a
high-contrast, animated spreadsheet-style example. Cells, formula-bar text,
selection movement, independently computed totals and completion rate are
rendered at full 1080×1920 output. The overlay is restricted to source frames
168–249 and pixels x=80..999, y=540..1169, away from the title and narration.

**This is a fictional UI reconstruction, NOT an actual Excel capture.**
All numbers are explicitly fictional: 12+18+24=54 cases,
9+14+21=44 completed, 10 remaining, 81.5% completion.
No personal data is used.

Run `python -m unittest discover -s quality/cycle1159/tests -v`.
The accompanying workflow renders a synthetic 9s 1080×1920 H264/AAC
sample, fully decodes it, verifies 270 frames and exact AAC stream copy.

The private 22.5s review MP4 is not committed to GitHub. It is delivered
separately to the user; its local QA checks 675 frames, audio ADTS SHA equality,
protected narration pixels, and unchanged later scenes. The source video
comes from cycle1157; no unapproved merge or automated posting occurs.

**Unverified:** independent Japanese ASR, semantic/timing match of narration
and subtitles, original reference v33 comparison, source media rights,
phone playback, employee approval, and GitHub Actions billing. Do not publish
without employee approval and manual posting.
