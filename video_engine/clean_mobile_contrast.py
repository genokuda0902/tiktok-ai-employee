"""Zero-cost mobile contrast finishing for image-slide videos.
Keeps the full frame readable on phone screens without heavy edge darkening.
Human quality/rights approval and manual posting remain mandatory.
"""
DEFAULT_CONTRAST = 1.025
DEFAULT_BRIGHTNESS = 0.004
DEFAULT_SATURATION = 1.015

def ffmpeg_filter(contrast=DEFAULT_CONTRAST, brightness=DEFAULT_BRIGHTNESS, saturation=DEFAULT_SATURATION):
    if not (1.0 <= contrast <= 1.04):
        raise ValueError("contrast outside safe range")
    if not (0.0 <= brightness <= 0.008):
        raise ValueError("brightness outside safe range")
    if not (1.0 <= saturation <= 1.03):
        raise ValueError("saturation outside safe range")
    return f"eq=contrast={contrast}:brightness={brightness}:saturation={saturation}"

def output_contract():
    return {"width":1080,"height":1920,"audio_passthrough":True,"zero_cost":True,"human_approval_required":True,"auto_post":False,"heavy_vignette_allowed":False}
