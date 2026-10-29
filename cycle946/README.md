# cycle946 — narration presence / scene-boundary energy audit (review only)

Distinct from cycle945's **visual waveform**: process the actual soundtrack with a conservative 95Hz high-pass, 2.6kHz +1.8dB voice-presence equalizer and 12kHz low-pass. Stream-copy the H.264 video so Japanese burned captions and visual cuts are **bitstream identical**. Report before/after presence-to-bass power ratio, and flag possible scene-cut timing issues using only an energy threshold. This is **not ASR**, Japanese word alignment, a pronunciation test or proof of intelligibility improvement.

10 genre IDs share the same filter, but only AI-work private review MP4 is rendered. Reproduce with \`python cycle946/src/voice_presence.py --source PRIVATE_REVIEW_SOURCE.mp4 --output REVIEW_ONLY.mp4 --genre ai_work\`. Requires FFmpeg, numpy. Tests: \`python -m pytest -q cycle946/tests/test_voice_presence.py\`.

Original \`AI_Jitan_v33_REAL_SPREADSHEET(1).mp4\` and full research transcripts inaccessible. User's 16-panel storyboard and available TikTok market/video research summaries reviewed; reference's human/robot visuals and 16 cuts remain unmatched. Prior source rights, employee approval, phone playback, independent Japanese ASR, and billing unverified. No auto-posting, public private-media upload, paid services or merges. **HUMAN_REVIEW / PUBLICATION_NOT_APPROVED.**
