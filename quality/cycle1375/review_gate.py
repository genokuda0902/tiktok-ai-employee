"""Fail-closed review gate shared by all genres."""
def evaluate(manifest):
    required = ("approved_assets", "japanese_narration_verified", "captions_synced", "human_approved", "playback_verified")
    missing = [key for key in required if manifest.get(key) is not True]
    return {"posting_allowed": not missing, "missing": missing}
