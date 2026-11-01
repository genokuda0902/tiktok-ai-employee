# cycle1118 — verified local result (2026-11-02 JST)

- **Source cycle1116** SHA256 `36c940b02ebf5818477c04ee51329a0efac3fb51534ab2a836af17e0e78945e6`.
- **New review MP4** SHA256 `0bad2e8a6940458a98e13aa6c5e38208145aef53580ab194d8f4193861c7eb22` (private ChatGPT artifact only).
- **Scene-caption SRT** SHA256 `124eb227de0803fc771919566eca459a2f7499a95bc779ed4c39ad9622034177` (private review only).
- **Delta**: eight on-screen Japanese scene captions transcribed into selectable mov_text track (ffprobe default=1; duplicate-caption risk); video pixels and H264 stream identical; AAC stream identical. No new spoken narration and no claims of speech alignment.
- **Format**: H.264 1080×1920, 30fps, 691 frames, 23.033333 seconds; AAC 48kHz stereo; mov_text Japanese subtitle stream (default flag=1, player may show duplicate captions).
- **Checks**: all-stream ffprobe, full A/V decode PASS; H264 and AAC stream SHA256 match source; eight subtitles round-trip through ffmpeg; six local unittest methods PASS; ten genre identifiers covered; synthetic 3s integration PASS.
- **References**: prior research summaries, user's 16-panel storyboard, repo main, unmerged PR #518, PROJECT_HANDOFF.md and recovery/v33. Original full research chats and reference v33 MP4 unavailable.
- **Open gates**: independent Japanese ASR/semantic and exact spoken timing, phone device, media rights, employee approval, actual Actions charges. PUBLICATION_NOT_APPROVED. No merge, posting, payment or private media commit.
