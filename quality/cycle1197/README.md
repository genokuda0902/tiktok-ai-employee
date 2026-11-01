# cycle1197 audio-reactive narration meter
Prior cycle1195: animated opening hook. This cycle: replace decorative 7-bar waveform with actual decoded narration RMS, 30fps; smooth, gate silence, preserve original Japanese AAC and captions. 10 color palettes supported; coordinate template is cycle1195-specific.
Run: python quality/cycle1197/code/audio_meter.py source.mp4 output.mp4 --genre ai --overlay-dir /tmp/meter
Tests: python -m unittest discover -s quality/cycle1197/tests -v
CI uses only synthetic content. Actual user media is NOT committed. Reference v33, ASR semantic alignment, rights, phone playback, employee approval remain unverified. HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. No automatic posting.
