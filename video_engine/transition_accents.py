"""Plan zero-cost transition accents for image-slide videos."""

def accent_delays_ms(cut_times, duration):
    if duration <= 0:
        raise ValueError("duration must be positive")
    cuts = [float(t) for t in cut_times]
    if cuts != sorted(cuts) or len(set(cuts)) != len(cuts):
        raise ValueError("cut times must be sorted and unique")
    if any(t <= 0 or t >= duration for t in cuts):
        raise ValueError("cut times must be inside the video")
    return [round(t * 1000) for t in cuts]


def transition_accent_plan(cut_times, duration, gain=0.28):
    if not 0 < gain <= 0.35:
        raise ValueError("gain must be > 0 and <= 0.35")
    return {"gain": gain, "delays_ms": accent_delays_ms(cut_times, duration), "external_asset_required": False, "manual_publish_only": True}
