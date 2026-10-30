# cycle1009 — remove duplicate subtitle track (review only)

2026-10-30 JST — HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.

## Why
cycle1007 MP4 already has Japanese subtitles burned into the video. Its selectable mov_text subtitle was still reported as default=1 by ffprobe, despite -disposition:s:0 0. Some players therefore display duplicate text.

## Change
- Stream-copy the original H264 and Japanese AAC while removing the embedded soft subtitle track.
- Preserve all 8 native MP4 chapters.
- Export the optional on-screen-text SRT and WebVTT as separate sidecar files.
- Validate 1080x1920, 30fps, 48kHz AAC, full video/audio decode, unchanged elementary video/audio data, chapter count and no embedded subtitle.
- Support 10 genre identifiers. Each genre must provide its own approved caption content; never copy AI-work captions into other genres.
- GitHub CI uses synthetic 2-second footage, NOT the private 23-second review video. No private video, screenshot or audio uploaded.

## Baseline and limits
Previous cycle1007: embedded Japanese mov_text subtitles + 8 chapters, no independent ASR. This cycle: fixes duplicate-subtitle player compatibility, **not** image pixels or audio. The original 23.033s review MP4 was locally decoded and its elementary video/audio packets matched source. Nine local unit tests and synthetic integration passed.

Accessible summaries of TikTok市場分析 / TikTok動画研究 favor first 1.5-second hook, purposeful cuts, clear Japanese captions, actual UI, Before/After and employee approval. Original v33 reference video was not directly accessible; user storyboard accessible only through prior summaries.

No independent Japanese ASR; spoken-word semantic caption sync NOT VERIFIED. Original reference side-by-side, source rights, phone playback, employee approval and GitHub Actions actual billing NOT VERIFIED.

No auto-post, merge, paid subscription or unauthorized publication. Manual post only after employee approval.
