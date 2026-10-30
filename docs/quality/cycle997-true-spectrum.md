# cycle997 — true 8-band spectrum overlay (human review only)

Source: local cycle993 review MP4 (not committed), compared against cycle995.
Change: prior cycle995 bar meter used one RMS amplitude and synthetic sine variation. This implementation uses eight genuine FFT audio-frequency bands (100–5400 Hz), band-wise p95 normalization, near-silence gate, and capped attack/release smoothing. Ten color presets are supported; only the AI-work genre was rendered end-to-end.

## Local real MP4 QA (2026-10-30 JST)
- Output: cycle997_TRUE_SPECTRUM_JP_HUMAN_REVIEW.mp4, SHA256 f18d8951e526e5edbcf0f0603487d3fc1724cc66a13ca2541d105a35dd1a1348
- H264 1080x1920 / 30fps / 691 frames / 23.033333s; full A/V decode PASS.
- AAC 48kHz ADTS packet SHA256 matches cycles 993 and 995.
- Eight sample frame mean absolute differences: meter ROI 11.564/255, caption ROI 0.071/255, main image ROI 0.331/255.
- 10 local tests PASS. CI renders **synthetic one-second** media only; real MP4 remains local and is not uploaded to this public repository.
- Research: accessible TikTok market/video research summaries and user 16-panel ChatGPT×Excel storyboard. Original v33 MP4 not available in this run.

## Open gates
No independent Japanese ASR, no semantic subtitle timing verification, no v33 original comparison, no confirmed commercial rights, no smartphone playback, no employee approval, no billing audit. The VOICE meter measures mixed audio, not isolated speech. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No posting, paid services, or merge.
