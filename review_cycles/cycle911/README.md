# cycle911 | platform-UI-safe CTA | HUMAN_REVIEW

Compared with cycle910's opening BEFORE/AFTER hook, this cycle improves the **last 2.733 seconds** of the existing private review video (source frames 609–690). The final CTA has 3 larger readable action cards, sequential highlights, a 10-genre palette, and a defined content area that stays left of x=900 and above y=1460. The narration and burned-in subtitle band are not replaced.

Local MP4: `cycle911_SAFE_AREA_CTA_JP_HUMAN_REVIEW.mp4`, 1080×1920, 30fps, 691 frames, 23.033s, H.264 + AAC 48kHz. The private video and inherited audio are **not** committed to public GitHub. CI only compiles source, checks review policy, and confirms no media files. It does not verify the completed MP4, rights, independent Japanese ASR, smartphone playback, or publication quality.

Run locally with Pillow, NumPy, Noto CJK fonts and ffmpeg:
```bash
python review_cycles/cycle911/safe_cta.py --out /tmp/cycle911_frames --genre ai_work
ffmpeg -i source_cycle910.mp4 -framerate 30 -i /tmp/cycle911_frames/%03d.png \
  -filter_complex '[1:v]setpts=PTS-STARTPTS+20.3/TB[cta];[0:v][cta]overlay=x=0:y=300:eof_action=pass:shortest=0:format=auto[v]' \
  -map '[v]' -map 0:a:0 -c:v libx264 -preset veryfast -crf 18 \
  -pix_fmt yuv420p -r 30 -c:a copy -movflags +faststart review.mp4
```

Reference research summaries: strong first 1–1.5s hook, short purposeful scenes, real UI evidence, high-contrast Japanese captions, mobile safe area, human review. The original v33 reference video was not accessible for direct comparison.

**PUBLICATION_NOT_APPROVED.** No paid service, no posting, no merge, no claim of reference-quality parity. Commercial rights for inherited assets remain unverified.
