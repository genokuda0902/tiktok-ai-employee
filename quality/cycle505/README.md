# cycle505 — Japanese caption rhythm (REVIEW ONLY)

Scope: eight scene-specific Japanese captions on original synthetic 1080x1920 20s AI/Excel demonstration. This is a new reimplementation, not original v33 source. Native Japanese narration is **NOT_AVAILABLE**, and no speech/caption synchronization is claimed. Human approval and rights review required before manual posting; automatic posting prohibited.

Research: prior summaries of TikTok市場分析/TikTok動画研究 (full transcripts inaccessible), and the original 16-panel storyboard inspected; reference v33 MP4 raw bytes unavailable. Changes vs cycle504: readable 2.5s caption rhythm; visuals and SFX preserved. No fake timing, time-savings or engagement claims.

Local commands: `python -m unittest -v test_caption_timeline.py`; `python caption_timeline.py --input cycle504_evidence_focus_REVIEW_ONLY.mp4 --output cycle505_REVIEW_ONLY.mp4 --manifest captions.json --ass captions.ass`.

Requires Python 3.11, FFmpeg with libass, Noto Sans CJK JP, and separately provided original/synthetic cycle504 MP4. This branch does not include the previous video and cannot independently reproduce the complete MP4 without that input. Source file and QA evidence are in the local ZIP; CI not claimed unless a run is verified.

Gates: rights=original_procedural, human_review=HUMAN_REVIEW, publication=NOT_APPROVED, auto_post=false, narration_status=NOT_AVAILABLE.
