# Cycle 1221 — evidence-panel overlap repair (REVIEW ONLY)

## Distinct improvement
Cycle 1219 shortened trailing near-silence by 0.263 s. Cycle 1221 instead corrects a visual defect: the scene-3 spreadsheet footer displayed overlapping, hard-to-read Japanese text. A clean, independently typed label "計算の確認" and checked arithmetic "9 + 14 + 21 = 44" replace only the footer ROI during chapter 3 (5.600–8.233s). The numbers match the visible source table: 9, 14, 21, total 44. Original narration subtitle and disclosure footer are not intentionally altered.

## Real MP4 (local review package; NOT uploaded to public GitHub)
Input cycle1219: 22.237 s, 667 frames, 1080x1920, 8 chapters, H.264/AAC. Output cycle1221: same duration/frames/chapters, AAC encoded audio packet data byte-identical, repaired visible panel, full decode verified. The H.264 video is re-encoded CRF18, so other pixels are not byte-identical. Local 8/8 unit tests and 3s synthetic smoke passed. Private video and reference v33 were NOT uploaded to this public repo.

## Common basis
Patch(genre,scene,label,expression,x,y,width,height) supports 10 genre keys and any reviewed scene. Guards reject unsupported genres, missing or overflowing text, invalid geometry and overlays touching the subtitle/footer protected region. Uses local Noto CJK font, Pillow, FFmpeg. CI only creates synthetic 1080x1920 video.

## Limits and publication gate
This is a localized evidence correction, not an independent ASR/transcription audit. Japanese pronunciation, caption meaning/timing, source rights, smartphone hardware playback, user v33 original direct comparison, employee approval and actual Actions billing remain unverified. No paid subscription, merge, automated TikTok post or public upload of the real video. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED**.
