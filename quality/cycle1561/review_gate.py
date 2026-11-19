"""Reusable QA for review-only vertical videos. Fail closed on missing narration."""
def assess(meta):
    problems = []
    if meta.get("width", 0) < 720 or meta.get("height", 0) < 1280:
        problems.append("resolution_below_review_target")
    if not meta.get("video_decodes", False):
        problems.append("video_decode_unverified")
    if not meta.get("japanese_narration_verified", False):
        problems.append("japanese_narration_missing")
    if not meta.get("speech_caption_sync_verified", False):
        problems.append("speech_caption_sync_missing")
    if not meta.get("assets_approved", False):
        problems.append("asset_approval_missing")
    if not meta.get("employee_approved", False):
        problems.append("employee_approval_missing")
    return {"publication_approved": not problems, "problems": problems}
