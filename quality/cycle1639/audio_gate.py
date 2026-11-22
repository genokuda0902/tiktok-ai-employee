"""Fail-closed audio gate for all genres. An audio stream alone is not Japanese narration proof."""
def publishable(qa):
    return bool(
        qa.get("video")
        and qa.get("width") == 1080
        and qa.get("height") == 1920
        and qa.get("audio_stream")
        and qa.get("japanese_narration_verified")
        and qa.get("caption_sync_verified")
        and qa.get("assets_approved")
        and qa.get("employee_approved")
    )
