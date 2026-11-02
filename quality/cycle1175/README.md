# cycle1175 — source-true UI magnification (review only)

Reimplementation, not recovered v33 code. This cycle makes the real UI **already present in the source video** easier to inspect. Three short focus lenses show the existing formula bar, fictional totals and human-review status in chapter 3 (6.16–8.73 s). It crops the live input stream, not a fabricated or externally obtained screenshot. The lens stays above y=1270; original Japanese burnt-in captions and AAC are preserved (audio elementary stream bit-identical).

Run: `python quality/cycle1175/ui_focus_lens.py --source INPUT.mp4 --output OUTPUT.mp4 --manifest MANIFEST.json --report QA.json`.

Manifest: `{"policy":"HUMAN_REVIEW/PUBLICATION_NOT_APPROVED","asset_approval":"review_only_no_publication","manual_post_only":true,"roi_reviewed":true,"genre":"ai","caption_safe_y":1270,"source_sha256":"<sha256 of input>"}`. The source is never uploaded/committed. Ten genre palettes are available, but ROIs must be re-reviewed for each new source and genre. A generic palette does **not** make the ROI coordinates universal.

Research: accessible summaries of `TikTok市場分析` / `TikTok動画研究` prioritize readable Japanese captions, short purposeful cuts, clear real UI, Before/After and manual posting. The user's 16-panel / ~36-second storyboard was visually inspected; the original v33 MP4 and complete prior chats were not available. This output remains 8 scenes / 23 seconds and does not match cinematic robot/person footage or 16-shot variety.

Limits: Japanese speech semantic accuracy and caption synchronization have **not** been independently transcribed; no local ASR model available. Underlying asset rights, employee approval, smartphone playback, and Actions billing remain unverified. No posting, merge, paid services or public private-media upload.
