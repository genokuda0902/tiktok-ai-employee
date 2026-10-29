# cycle966 — actual LibreOffice Calc formula export in the finished-sample scene

**Review-only reimplementation, not original v33.** New improvement versus cycle964's drawn arithmetic check: scene03 (5.80–8.70s, 87 frames) now uses a real LibreOffice Calc CSV import and **SUM-formula calculation**, exported to PDF, visually cropped into three beats: table → monthly comparison → verified totals 46 / 29. The chart bars are drawn from the same fictional CSV rows; the PDF table is an actual Calc export. This is **not a live Excel/ChatGPT screen recording** and is labeled accordingly in-video.

## Reproduce with locally authorized source
Install Python Pillow, LibreOffice, poppler-utils, ffmpeg, Noto CJK fonts. For full local QA additionally install OpenCV and NumPy.

~~~bash
python -m unittest discover -s cycle966 -p 'test_*.py' -v
python cycle966/calc_proof.py --workdir /tmp/cycle966-synthetic
python cycle966/calc_proof.py --source /private/cycle964_ARITHMETIC_CONTINUITY_JP_REVIEW_ONLY.mp4 --output /private/cycle966_REAL_CALC_PROOF_JP_REVIEW_ONLY.mp4 --workdir /private/calc --report /private/render_report.json
python cycle966/verify_review.py /private/cycle964_ARITHMETIC_CONTINUITY_JP_REVIEW_ONLY.mp4 /private/cycle966_REAL_CALC_PROOF_JP_REVIEW_ONLY.mp4 /private/qa.json
~~~

The private source SHA256 must be independently checked against \`cb8d504b95c7e06f1b3acb216a7f283e83a2b6276b22e83fb82f5b73e2e557cc\`. Never upload source or output MP4, audio, PDF images or private media to this public repository. CI uses synthetic fictional data only.

Ten genre palettes are declared; only \`ai_work\` has been rendered/reviewed. Nine other genres are blocked. Full original TikTok market/video-study chats and original v33 reference MP4 were unavailable; the 16-panel storyboard was visually inspected. This clip remains 8 scenes / 23.033s, versus reference 16 panels / ~36s. Japanese ASR / semantic subtitle sync, smartphone playback, source commercial rights, employee approval and actual Actions billing remain unverified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, no auto-post, no paid services.
