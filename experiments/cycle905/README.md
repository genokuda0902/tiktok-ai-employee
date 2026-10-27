# cycle905 | Kinetic before/after instruction clarity (REVIEW ONLY)

**Difference:** cycle903 focused on mobile-readable scene07 lens; concurrent cycle904 introduced upper-scene microcamera/audio QA. This separate route rebuilds **scene06 (14.5–17.4 s)** as a three-stage teaching sequence: vague NG → specific OK → split into two verified changes. Uses 87 native 1080px transparent overlays, six-frame crossfades, a small vertical entrance motion, and ten configurable genre text sets. Only ai_work was rendered into the finished MP4.

**Research/reference:** accessible TikTok市場分析/TikTok動画研究 summaries recommend strong first 1.5s, short purposeful scenes, readable Japanese, actual UI, Before/After. User's 16-panel storyboard description consulted. Original v33 video and full research transcripts were not accessible in this run. cycle904 finished MP4 was not mounted; local baseline is the mounted cycle903 video.

**Local output:** 1080x1920, 30fps, 691 frames, 23.033s, H.264 + original AAC 48kHz bitstream. Full audio/video decode PASS. Source SHA256: 7140b12341f707fe868b71fbb485494dada936d9d7cf8f359308b198576630f8. Output SHA256: 53223a34d5edaa22919250890bb2431258ea3688f090a280c3226533f4cf788c. AAC ADTS SHA256: c2cf7807e183573d74fa7c3f1a719cfb05ccdcb0790ef8d28c2c902640bc197d (unchanged). Outside-scene sampled MAE max 0.320; lower subtitle-band sampled MAE max 0.130; three stage target MAEs 32.435/36.256/47.831. 14/14 local QA checks PASS. CI only validates code/synthetic PNGs, **not** the private finished MP4.

**Render with private local input (do not upload it):**

1. Install free Pillow, FFmpeg and Noto Sans CJK Japanese fonts.
2. Run: python experiments/cycle905/kinetic_before_after.py --genre ai_work --output /tmp/cycle905-overlays
3. Run:
   ffmpeg -i INPUT_PRIVATE.mp4 -framerate 30 -start_number 0 -i /tmp/cycle905-overlays/frame_%03d.png -filter_complex "[1:v]format=yuva420p,setpts=PTS-STARTPTS+14.5/TB[ov];[0:v][ov]overlay=x=0:y=300:eof_action=pass:repeatlast=0:format=yuv420,format=yuv420p[v]" -map "[v]" -map "0:a:0" -c:v libx264 -threads 2 -preset ultrafast -crf 21 -pix_fmt yuv420p -c:a copy -movflags +faststart OUTPUT_REVIEW.mp4

**Safety gate:** HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. Inherited visual/audio asset rights and commercial permission unverified. No independent Japanese ASR semantic match, original v33 direct comparison, smartphone playback, employee approval, or actual GitHub Actions billing audit. No merge, paid service, auto-posting, or public upload of private media. Employee approval required before manual posting.
