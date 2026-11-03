# Cycle1183 — review-only
Baseline: cycle1182 (23.033s), no visual change in cycle1182.
Change: dark translucent lower 24.5% overlay, opacity 0.16, intended to improve subtitle contrast.
Local render command: ffmpeg -i cycle1182_VOICE_DYNAMICS_REVIEW_ONLY.mp4 -vf 'drawbox=x=0:y=1450:w=iw:h=470:color=black@0.16:t=fill' -c:v libx264 -preset ultrafast -crf 19 -c:a copy -movflags +faststart cycle1183_CAPTION_BACKDROP_REVIEW_ONLY.mp4
Local ffprobe: H.264 1080x1920 30fps, AAC, duration 23.033333s, size 12,160,549 bytes; ffmpeg full decode succeeded.
Limitations: actual local render uses fixed 1450px and ultrafast; reusable script uses relative 75.5% and medium preset. Visual meaning/sync, audible quality, phone playback, privacy/rights, v33 comparison unverified. The MP4 is NOT committed to GitHub. Do not publish.
Prior cycle1182 had audio compression; this cycle changes subtitle-background region only.
