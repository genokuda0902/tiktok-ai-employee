# cycle813 — real LibreOffice Calc goal-entry demonstration (REVIEW ONLY)

## Delta from cycle812
Cycle812 scene 02/08 (3.00–5.97 s) showed a fabricated static goal-entry UI.
Cycle813 replaces frames 90–179 with an actual local LibreOffice Calc GUI
recording using fictional values: enter 20 contracts, show actual 12, and
evaluate =B2-C2 to 8. A fully opaque 850×600 card and large labels avoid
ghosting and preserve the existing lower subtitle region. All ten genre
accent presets share the renderer.

## Private reproduction
Requires FFmpeg, ffprobe, Pillow and Noto Japanese font. Make a local
1280×800, approximately 5.4-second Calc screen recording using fictional
values only. Verify no customer or private information appears.

Run tests:
PYTHONPATH=quality/cycle813 python -m unittest discover -s quality/cycle813 -p 'test_*.py' -v

Render:
python quality/cycle813/calc_screen_insert.py --source cycle812_KINETIC_QUESTION_REVIEW_ONLY.mp4 --capture real_calc_capture_final.mp4 --output cycle813_REAL_CALC_GOAL_REVIEW_ONLY.mp4 --genre sales_business --target 20 --actual 12 --fictional-data

The private source video, GUI recording and inherited Japanese narration are
not committed to public GitHub. CI uses synthetic color/tone and screen
patterns only, never the private footage or audio.

## Local verification (2026-10-24)
- Input cycle812 SHA256: 22852b9ded6616de421097e9d9dd139d88662c5e430290d7864edb9ca94e03a9
- Calc capture SHA256: eede9ed60a6da387f31c5a65007699547d64d82434a00e1508d80497bd412d82
- Review MP4 SHA256: ac4aee47e6f82af1e0630bbd51669c3e3dd838e389c05689fd22f5d6d29db3e1
- 1080×1920 H.264 30fps 718 frames 23.933 s, AAC 48kHz.
- Full video/audio decode PASS; AAC elementary stream identical to cycle812.
- Eleven unit tests PASS; ten genre configurations validated.
- At 4.5s, mean full-frame RGB pixel difference vs cycle812 is 27.507.
- At untouched 7.2s, mean difference is 1.338 (re-encoding).
- Speech semantics, Japanese caption alignment, naturalness, phone playback,
  rights and employee approval remain UNVERIFIED.

## GitHub CI
- Draft PR: https://github.com/genokuda0902/tiktok-ai-employee/pull/120
- Push CI success: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40080537329
- PR CI success: https://github.com/genokuda0902/tiktok-ai-employee/actions/runs/40080545741
- Synthetic-only artifact ID: 12554649213.
- Artifact is NOT the Japanese-narrated private review MP4.

## Provenance
Previous summaries from TikTok市場分析 and TikTok動画研究 were consulted:
strong opening, genuine operation, Before/After, Japanese captions, human
review. Complete task/chat transcripts unavailable. User's 16-panel
ChatGPT/Excel storyboard was visually inspected, especially panels 4–8.
Original v33 reference MP4 unavailable for direct side-by-side comparison.

Repo main checked at 18e084c38db0dc55db7dfc0532b9451b1167f2aa.
PROJECT_HANDOFF.md, recovery/v33/RECOVERY_STATUS.md and unmerged
PRs #116/#117 inspected. This work builds on #117 without merging it.

## Publication gate
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.
No automatic TikTok posting, employee delivery, merge, or paid services.
Next: independent Japanese ASR/caption verification, reference v33 direct
comparison, approved image-first visual assets.
