"""Fail-closed publication gate shared by ten genres."""
REQUIRED = ("video_decodes", "japanese_narration_verified", "speech_caption_sync_verified", "asset_rights_approved", "privacy_review_passed", "employee_approved")
def evaluate(meta):
    missing = [key for key in REQUIRED if meta.get(key) is not True]
    return {"publication_approved": not missing, "missing": missing}
