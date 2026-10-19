# cycle685: caption safe-zone QA (review only)
Zero-cost improvement over cycle684: screen captions use actual glyph width, wrap to two lines, and stay above the bottom 20% UI area (y <= 1536 at 1080x1920). Ten genre profiles share the same validation.
Local rendering bundle and review-only MP4 are delivered as a separate sandbox ZIP. This PR contains a standalone contract and tests, not the full render source.
Local 44 tests passed. New Japanese narration unavailable; scene text is NOT speech-aligned subtitles. Audio rights, phone playback and staff approval remain unverified.
No merge, no automatic posting.
