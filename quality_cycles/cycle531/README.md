# cycle531 — footer-safe stage navigation (review-only)
Source for local render: cycle529 synthetic pre-ribbon MP4 (not in repository).
Reason: cycle530's chapter ribbon at y=147..190 overlapped the spreadsheet header at t=12 seconds.
Fix: four-stage ribbon at y=1604..1664, outside declared content and review badge rectangles.
Local result: 20.00s H.264/AAC 1080x1920, 600 frames, 12/12 offline tests PASS, full decode PASS.
Top UI ROI at 12s (x=0..1080, y=95..225) MAD vs pre-ribbon master: cycle530=4.12, cycle531=0.16.
Japanese narration is NOT generated; spoken-caption sync NOT verified.
No publication; HUMAN_REVIEW / NOT_APPROVED.
Render command: python safe_stage_nav.py --source path/to/cycle529_clean_loop_REVIEW_ONLY.mp4 --output out.mp4 --manifest manifest.json --qa qa.json
Manifest must include the source SHA-256 and explicitly cleared synthetic or owner-approved assets.
