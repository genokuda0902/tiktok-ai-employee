"""Review-only timed Japanese caption validation, reusable across genres."""
def validate_captions(captions, duration):
    if not captions or captions[0][0] != 0:
        raise ValueError("captions must start at zero")
    end = 0
    for start, stop, text in captions:
        if start != end or stop <= start or stop > duration or not text.strip():
            raise ValueError("caption gap, overlap, invalid text, or duration")
        end = stop
    if end != duration:
        raise ValueError("captions must cover entire clip")
    return True

def publication_gate(manifest):
    """Speech must be independently verified; captions are not speech."""
    return (manifest.get("narration_verified") is True
            and manifest.get("caption_sync_verified") is True
            and manifest.get("asset_rights_approved") is True
            and manifest.get("human_approved") is True)
