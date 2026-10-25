# cycle843 — mobile-readable actual spreadsheet focus (review-only)

Reimplementation using **locally supplied, SHA-pinned, fictional** Calc footage. Source MP4, personal images and audio are never committed or uploaded. The existing scene 3 contains a full-window screen capture with small text; cycle843 replaces its image-only area for 79 frames (5.667–8.300 s) with a two-beat, ~2.0× enlargement of real captured spreadsheet cells. This avoids a fabricated UI, leaves existing Japanese captions and narration unchanged, and adds no quantitative time-saving claims. Shared GENRES and safety gates cover ten genres, but only ai_work has been rendered.

## Local usage

Requirements: Python 3.11+, opencv-python-headless, numpy, Pillow, ffmpeg, ffprobe, fonts-noto-cjk.

    PYTHONPATH=. python -m unittest discover -s cycle843 -p 'test_*.py' -v
    PYTHONPATH=. python -m cycle843.mobile_calc_focus \
      --source /local/review-only-cycle842.mp4 \
      --output /local/cycle843.mp4 \
      --manifest /local/fictional-review-manifest.json --genre ai_work

Manifest: source_sha256 of exact source plus all REQUIRED flags in module. Privacy/rights/publication approval defaults fail closed. source_rights_reviewed=false explicitly means review only, **not** permission to publish.

Source: cycle842 local output, SHA256 c8ba143e9b4d3c99a68c9a639863e7324a111e4a97fde10e42345db1c6737fa3. Output: SHA256 f3d4104989abc1e6b9fc5c4655223e9748dc2c49a8f5c93dcc1032a5e5cae712. Local tests: 8/8 PASS; 1080x1920, 30fps, 691 frames, 23.033 seconds; H264 video and AAC 48kHz mono, full decode PASS, decoded audio PCM MD5 unchanged (813f69e5c926b70c927e46e27704e267). Changes limited to the image-only region in scene 3, existing caption area protected. Full review MP4 and QA logs are shared via ChatGPT sandbox, **not** uploaded to GitHub.

No original v33 source/MP4 accessible in this cycle; original v33 is not reproduced. TikTok市場分析 / TikTok動画研究 full task logs unavailable; prior research summaries and user 16-panel storyboard text reviewed. Independent Japanese ASR, word-level subtitle sync, smartphone playback, reference-v33 direct visual comparison, rights approval and employee approval are still pending.

GitHub CI runs synthetic-only media, never user footage. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No merge, payment or posting.
