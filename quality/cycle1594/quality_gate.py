"""Fail-closed publication gate shared across ten genres."""
def evaluate(evidence):
    required = ("video_decodes", "japanese_narration_verified", "caption_sync_verified", "assets_licensed", "privacy_reviewed", "employee_approved")
    missing = [key for key in required if evidence.get(key) is not True]
    return {"approved": not missing, "missing": missing}
