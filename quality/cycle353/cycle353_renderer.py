# cycle353 reusable attention-density QA
# Measures central visual edge density + frame-difference motion at 1s intervals.
# Low-attention windows (bottom 30%) receive a brief non-semantic focus pulse.
# Runtime implementation validated against cycle352 MP4; no paid API, no auto-post.
IMPROVEMENT_AXIS = "attention_density_flat_window_detection"
RESOLUTION = (1080, 1920)
SAMPLE_INTERVAL_SEC = 1.0
LOW_ATTENTION_PERCENTILE = 30
PUBLICATION_GATE = "HUMAN_REVIEW / PUBLICATION_NOT_APPROVED"
