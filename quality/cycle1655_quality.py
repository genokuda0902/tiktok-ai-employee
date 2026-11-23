"""Genre-neutral timing and safety validation for review-only TikTok clips."""

def validate_scenes(scenes, duration=12.0):
    if not scenes:
        raise ValueError("no scenes")
    previous = 0.0
    for scene in scenes:
        start, end, caption = scene["start"], scene["end"], scene["caption"]
        if start < previous or end <= start or end > duration:
            raise ValueError("invalid scene timing")
        if not caption.strip() or len(caption) > 32:
            raise ValueError("caption absent or too long")
        previous = end
    return True

def posting_allowed(*, narration_verified=False, captions_synced=False,
                    assets_approved=False, employee_approved=False):
    return all((narration_verified, captions_synced, assets_approved, employee_approved))
