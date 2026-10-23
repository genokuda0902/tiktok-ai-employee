# cycle793 — caption collision guard (review only)

Observed: cycle792 at 17.30–20.80s displays a redundant summary caption directly over the large **650,000円** figure. The caption was introduced in cycle791 and is a regression separate from cycle786's opening caption deduplication.

Fix: restore only the caption band (y=1290–1589) from a LOCAL pre-caption master (cycle790), leaving the cycle792 chart (9–11s) and all other content unchanged. Config requires overlapping caption/protected rectangles, valid timing, ten-genre keys, and fail-closed rights/publication flags. This is NOT generic OCR or transcription.

Reproduce locally (Python 3.11, FFmpeg/FFprobe):
```sh
python quality/cycle793/repair_caption_collision.py --config quality/cycle793/config.json --input /local/cycle792.mp4 --clean /local/cycle790.mp4 --output /tmp/cycle793_NUMBER_UNOBSTRUCTED_REVIEW_ONLY.mp4 --report /tmp/cycle793.json
python quality/cycle793/verify_repair.py --input /local/cycle792.mp4 --clean /local/cycle790.mp4 --output /tmp/cycle793_NUMBER_UNOBSTRUCTED_REVIEW_ONLY.mp4 --report /tmp/cycle793_verify.json
```

CI generates its own 23.843s **SYNTHETIC-TONE** test videos, not the user media or Japanese voice. User video/audio remain local, never committed. Previous TikTok市場分析/TikTok動画研究 summaries and user 16-frame storyboard consulted; full research texts and v33 original MP4 unavailable. Read PROJECT_HANDOFF.md and recovery/v33/RECOVERY_STATUS.md. This is an original reimplementation, NOT recovered v33. Human audio/caption semantic review, rights and phone testing still pending. No merge, paid services or automatic posting.
