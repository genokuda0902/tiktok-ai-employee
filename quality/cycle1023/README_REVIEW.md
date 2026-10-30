# cycle1023 — first-scene readability redesign (HUMAN_REVIEW)

## Different from cycle1021
cycle1021 improved an audio-reactive top VOICE meter. cycle1023 instead removes overlapping Japanese text/graphics from the first 2.633 seconds by replacing only the center slide area with an original clean infographic. The existing 8-scene video, Japanese AAC narration, original burned subtitles, top header, and chapter timing are retained.

## Local full-length evidence
Source SHA256 d4fadc3911cf8d67d87e43155cdf5f4fe4ded3b2a75271ef38e84b2b6e241bae.
Output SHA256 fc68cf399a1780a90cf20b9cdadf6e437c66e52599cc7984bcef3cf913535f9a.
22.500s, 1080x1920 H264 30fps, 675 frames, AAC 48kHz, 8 chapters. Full A/V decode PASS. Audio bitstream copied identically. First scene changed-content ROI MAE 63.409/255; remaining 7 scenes <1.1/255; burned subtitle ROI across 8 scenes max 0.55/255. Five local tests and 4-second synthetic render PASS.

## Reuse and restrictions
10 genre palettes supported; only ai_work rendered as a full-length real MP4. Uses local Pillow, FFmpeg, system Noto CJK fonts, no paid APIs or third-party images. Full private MP4 stays in conversation artifacts, never uploaded to public GitHub. CI only tests synthetic media.

Independent Japanese ASR, narration/subtitle semantic sync, original v33 reference, rights clearance, smartphone playback, employee approval, and Actions billing are NOT verified.

**HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No merge, automatic posting, or purchases.**
