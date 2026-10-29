# cycle945 — measured-audio waveform, review only

Distinct from cycle944's original ambient bed: replace the decorative waveform underneath burned Japanese subtitles with bars driven deterministically by the actual decoded soundtrack's 40ms RMS energy. 24 trailing video-frame bars show approximately 0.8 seconds of real audio activity. No arbitrary random heights. Only the existing waveform strip (x89–529, y1707–1773) is covered; Japanese caption text and progress bar remain outside it. Ten genre color profiles; only one private AI-work MP4 rendered. Audio AAC is stream-copied unchanged.

Run: python cycle945/src/voice_true_meter.py --source PRIVATE_APPROVED_FOR_REVIEW.mp4 --output REVIEW_ONLY.mp4 --genre ai_work

Test: python -m pytest -q cycle945/tests/test_voice_true_meter.py

This waveform measures audio amplitude, including quiet synthetic ambience. It does not recognize Japanese speech, prove word timing, validate meaning, or prove pronunciation. Inherited media rights, phone playback, employee approval and reference-v33 quality remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No public media upload, posting, merge, paid service or confidential assets.
