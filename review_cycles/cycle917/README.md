# cycle917 — readable prompt template / review only

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.** No automatic TikTok posting, merge, paid services or public private-media upload.

## Distinct improvement
Previous cycle916 PR #295 showed a fictional source/draft discrepancy in scene06, and parallel PR #296 illustrated a cinematic prompt editor in scene04. This cycle replaces the small, blurry scene07 (17.0–19.6s, frames 510–587) with a bright, readable **reusable prompt template**: purpose → constraints → output. The existing Japanese caption says to keep reusable instructions as templates, so the visual directly supports that line. The animation highlights each field for 26 frames. It uses original Pillow-drawn shapes and 10 genre-specific copy presets; only ai_work was rendered as a full video.

## Local reproduction — private inputs only
Requires Python 3, Pillow, Noto CJK, FFmpeg. Generate 78 overlay frames:
python3 review_cycles/cycle917/template_story.py --genre ai_work --out /private/cycle917_frames

Overlay at x=0, y=150 during video frames 510–587, preserving inherited Japanese AAC and subtitles below y1490. Example:
ffmpeg -framerate 30 -start_number 0 -i /private/cycle917_frames/%03d.png -i /private/previous.mp4 -filter_complex "[0:v]format=yuva420p,setpts=PTS-STARTPTS+17/TB[fg];[1:v][fg]overlay=x=0:y=150:eof_action=pass:enable='between(n,510,587)',format=yuv420p[v]" -map "[v]" -map 1:a:0 -c:v libx264 -preset veryfast -crf 18 -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart /private/cycle917.mp4

Run offline CI tests:
python3 -m unittest discover -s review_cycles/cycle917 -p test_policy.py -v

Local Pillow tests:
PYTHONPATH=review_cycles/cycle917 python3 -m unittest discover -s review_cycles/cycle917 -p test_renderer.py -v

The private completed MP4, inherited video/audio and image previews are intentionally **not in this public GitHub repository**. CI checks source and policy, **not** the private completed MP4.

## Reference and unverified items
Reviewed accessible TikTok市場分析 / TikTok動画研究 summaries and the user-provided 16-panel ChatGPT×Excel storyboard. Original v33 MP4 and full original chat transcripts were not available. The 23-second eight-scene output still differs from the 36-second sixteen-panel cinematic reference. Independent Japanese speech recognition, semantic subtitle alignment, smartphone playback, inherited asset rights, employee approval, viewer retention and actual Actions billing remain unverified. Manual posting only after employee approval.
