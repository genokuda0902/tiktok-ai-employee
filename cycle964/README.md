# cycle964 — cross-scene arithmetic continuity (REVIEW ONLY)

**Not original v33.** Distinct from cycle963's five original audio cues: replace only the 11.60–14.50s verification scene with a legible three-stage *fictional* source-table arithmetic check. The prior review clip displayed the consistent 46/29 totals in its opening but a different in-progress total within the middle verification scene. The new three-stage graphic uses the same source rows, explicitly labels itself a constructed illustration, and never represents an actual Excel/ChatGPT recording.

- Rows: Apr (12,8), May (16,9), Jun (18,12).
- Verified arithmetic: 12+16+18=46 and 8+9+12=29.
- Three beats: inspect source rows → recompute → show both totals.
- Overlay occupies y=0..1449 only; original burned Japanese captions below y=1490 remain. Original Japanese AAC is **stream-copied**.
- Ten genre validation policies; **only ai_work** has been rendered for private review. Others fail closed.

## Reproduce with locally authorized source

~~~bash
python -m pip install 'Pillow>=10,<13' opencv-python numpy
python -m unittest discover -s cycle964 -p 'test_*.py' -v
python cycle964/verified_totals.py --source /private/cycle963_ORIGINAL_SYNC_CUES_JP_REVIEW_ONLY.mp4 --output /private/cycle964_ARITHMETIC_CONTINUITY_JP_REVIEW_ONLY.mp4 --report /private/render_report.json
python cycle964/verify_review.py /private/cycle963_ORIGINAL_SYNC_CUES_JP_REVIEW_ONLY.mp4 /private/cycle964_ARITHMETIC_CONTINUITY_JP_REVIEW_ONLY.mp4 /private/qa.json
~~~

Source SHA-256 must match 5df3b08c7ec6d18d3de52616939bc5b36fd1d1f3d790b5caf0e50d5c8cf54c6f. Requires FFmpeg/FFprobe and Noto CJK font. **Never commit the source MP4, new MP4, source stills, audio, or other private media.** GitHub CI checks synthetic frame/encode and unit tests only; it does not prove the completed private MP4.

Accessible research summaries recommend fast hook, readable text, real app proof, Before/After, manual CTA. User's 16-panel / ~36s ChatGPT×Excel storyboard was visually inspected; original v33 reference MP4 and full market/video research chats remain unavailable. This is still an 8-scene / 23s reimplementation, not cinematic reference equivalence.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** Independent Japanese speech transcription and semantic caption timing, inherited media rights, smartphone playback, employee approval, and actual Actions billing are unverified. No merge, auto-post, paid service, or private-media publication.
