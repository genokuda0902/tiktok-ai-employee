# Cycle 1403

Baseline: cycle1402, 1080x1920, 20 seconds, 5 SRT scene captions, no speech.

Change: burn scene captions into H.264 frames and animate a bottom progress bar. Local MP4 decoded successfully, 1080x1920, 20s. No narration; not speech synchronized; review-only. No confidential assets: synthetic spreadsheet scene. Original v33 not accessed. No posting or merge.

Run: `python tools/cycle1403_caption_burn.py input.mp4 captions.srt output.mp4`; requires FFmpeg with libass and Japanese font. CI should test fail-closed behavior.
