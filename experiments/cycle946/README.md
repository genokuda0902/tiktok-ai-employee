# cycle946 — adaptive hard-cut transition (HUMAN_REVIEW)

Distinct from cycle945's eight-band real-audio meter: this cycle detects unusually abrupt cuts and applies a seven-frame, soft-edge directional reveal **only to the central illustration**, leaving Japanese headers, burned-in subtitles and footer untouched. No ASR or word-level synchronization is claimed.

Local source: cycle945 review-only MP4, SHA256 da1f21c64f7a00e7f8d612a83a18692f60c649d04205946a5fe70fbea6596d10.
Local result: cycle946 review-only MP4, SHA256 48fda405481ac3f6544d9ef4ea957fd927b579b4ebf41b3a6b2ff4c7d045699d.
1080x1920, H264, 30fps, 691 frames, 23.033s, AAC48kHz stream copied bit-for-bit. Full A/V decode PASS. 16 local tests PASS. Three hard cuts (frames 348,435,609) first-frame pixel jumps 30.96→5.26, 24.84→3.54, 29.83→3.55. This is a technical smoothing metric, not human quality approval.

10 genre presets are defined and unit tested; one AI-productivity MP4 was actually rendered. The real MP4 is provided privately in ChatGPT, **not committed to public GitHub**. GitHub Actions runs synthetic unit tests, not real-media validation. Original reference v33, independent Japanese ASR/semantic subtitle alignment, commercial asset rights, phone playback, employee approval and actual Actions billing remain unverified.

No merge, paid service, public upload or auto-posting. Employee approval is required before manual posting.
