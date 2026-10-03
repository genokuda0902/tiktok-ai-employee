"""Zero-cost reusable timing layer for cycle302.
Decode narration to 16 kHz mono PCM, estimate noise floor, detect RMS rises/peaks,
and derive visual emphasis timestamps. No genre-specific hard-coded timestamps.
""" 
SAMPLE_RATE=16000
WINDOW_SECONDS=0.12
HOP_SECONDS=0.06
MICRO_ZOOM=1.010
