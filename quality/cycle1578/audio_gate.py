"""Reusable fail-closed audio publication gate (review-only)."""
def audio_gate(probe, spoken_verified=False, subtitle_sync_verified=False, assets_approved=False, employee_approved=False):
    """Metadata presence alone is not proof of Japanese speech or subtitle sync."""
    has_audio = any(s.get("codec_type") == "audio" for s in probe.get("streams", []))
    return all((has_audio, spoken_verified, subtitle_sync_verified, assets_approved, employee_approved))
