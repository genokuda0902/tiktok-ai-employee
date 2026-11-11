"""Cross-genre, fail-closed review gate for generated MP4 metadata."""
def publication_allowed(manifest):
    required = ("narration_verified", "caption_sync_verified", "asset_rights_approved", "privacy_review_passed", "employee_approved", "manual_post_only")
    return all(manifest.get(key) is True for key in required) and manifest.get("posting_allowed") is True

def scene_checks(scenes):
    if not scenes or len(scenes) < 3:
        return False
    return all(isinstance(s.get("duration"), (int,float)) and s["duration"] > 0 and s.get("caption") for s in scenes)
