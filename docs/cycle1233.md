# cycle1233 — review-only chapter progress
Previous cycle1232: added a disclosure that audio/subtitle synchronization was unverified.
This cycle: adds a visible 3-chapter progress indicator to an existing 23.033s review-only MP4. Existing AAC audio is copied unchanged. This is not synchronized narration.
Render: ffmpeg -i INPUT.mp4 -vf "$(python -c 'from src.cycle1233_chapter_progress import ffmpeg_filter; print(ffmpeg_filter())')" -c:v libx264 -c:a copy OUTPUT.mp4
Local FFmpeg decode passed; output 1080x1920 H.264 + AAC, 23.033s. Speech content, caption alignment, source rights, phone playback and visual quality remain unverified. DO NOT POST. No confidential assets committed.
