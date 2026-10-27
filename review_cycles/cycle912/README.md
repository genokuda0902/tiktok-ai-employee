# cycle912 — repeated-work calendar, review-only

Status: HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Distinct improvement
Compared with cycle911's final CTA safe-area revision, cycle912 replaces scene 02 (frames 87–173, 2.9–5.8 s) with an animated 3-week calendar. Repeated weekly task cards appear in sequence, become visually connected, and reveal the first task to standardize. This is visual evidence rather than another static three-item checklist.

Ten genre-specific task/CTA strings and color palettes are supported by the same renderer. Only the AI-work Japanese MP4 was rendered in this cycle. All labels are fictional. No personal information or third-party media was added.

## Local build
Requires Python, Pillow, NumPy, Noto Sans CJK JP, and FFmpeg. Input MP4 is private and must never be committed.

1. python review_cycles/cycle912/repetition_calendar.py --genre ai_work --out /private/cycle912_frames
2. ffmpeg -i /private/source_cycle911.mp4 -framerate 30 -i /private/cycle912_frames/%03d.png -filter_complex "[1:v]setpts=PTS-STARTPTS+2.9/TB[s];[0:v][s]overlay=x=0:y=300:eof_action=pass:shortest=0:enable='between(t,2.9,5.7667)'[v]" -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart /private/cycle912_review.mp4

## Verified private output
MP4: cycle912_REPETITION_CALENDAR_JP_HUMAN_REVIEW.mp4
SHA256: acf735a060896d584b3b02b8a2e3c6aaa31bc22c24a415c663db730f9d829925

Local QA: 1080x1920 H.264, 30fps, 691 frames, 23.033s, inherited Japanese AAC 48kHz with byte-identical ADTS audio SHA256 c2cf7807e183573d74fa7c3f1a719cfb05ccdcb0790ef8d28c2c902640bc197d. Full decode passed. Changed-scene mean image difference 72.44 at 1/4 resolution; outside-scene means 0.11/0.21; caption-band mean 0.085. Local runtime tests 8/8 and QA 17/17 passed.

GitHub CI is code/policy-only. It does not decode or validate the private completed MP4. Completed video is shared only as a private ChatGPT review file, not committed or posted.

## Research and limitations
Consulted accessible prior TikTok research summaries: strong hook, purposeful visuals, real UI evidence, readable Japanese, employee-reviewed manual posting. Original reference v33 MP4 and complete research transcripts were unavailable for direct comparison. Independent Japanese ASR semantic matching, inherited media rights, smartphone hardware playback, employee approval, and actual GitHub Actions charges remain unverified.

No merge, paid contract, publishing, or automatic posting.
