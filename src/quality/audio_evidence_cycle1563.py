"""Reusable fail-closed audio evidence gate for review videos (cycle1563)."""

def narration_ready(probe, transcript_verified=False, caption_sync_verified=False):
    streams = probe.get("streams", [])
    audio = [s for s in streams if s.get("codec_type") == "audio"]
    # AAC presence, duration or signal level do not prove Japanese speech.
    return bool(audio and transcript_verified and caption_sync_verified)

def publication_ready(probe, evidence):
    return bool(narration_ready(probe, evidence.get("transcript_verified"), evidence.get("caption_sync_verified")) and evidence.get("asset_rights_approved") and evidence.get("employee_approved"))
