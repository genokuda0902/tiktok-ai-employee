"""Zero-cost mobile speech-presence finishing for image-slide videos.

This is deliberately subtle: it improves narration intelligibility on phone speakers
without changing timing, captions, geometry, publishing state, or rights policy.
"""


def speech_presence_filter(width=1080, height=1920, sample_rate=48000):
    if (width, height) != (1080, 1920):
        raise ValueError("delivery geometry must be 1080x1920")
    if sample_rate != 48000:
        raise ValueError("audio must be 48 kHz")
    # Remove sub-bass rumble and add a bounded +1.5 dB presence lift around 2.8 kHz.
    # Limiter is safety-only; timing is unchanged.
    return "highpass=f=90,equalizer=f=2800:t=q:w=1.2:g=1.5,alimiter=limit=0.93"


def safety_contract():
    return {
        "zero_cost": True,
        "preserve_timing": True,
        "preserve_caption_copy": True,
        "human_approval_required": True,
        "auto_post": False,
        "presence_gain_db": 1.5,
        "max_presence_gain_db": 2.0,
    }
