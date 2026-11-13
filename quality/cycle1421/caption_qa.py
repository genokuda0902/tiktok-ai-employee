"""Review-only subtitle legibility and fail-closed audio QA. Standard library only."""
def assess(manifest):
    issues=[]
    if manifest.get("caption_font_px",0)<40: issues.append("caption_too_small_at_1080p")
    if not manifest.get("caption_contrast_border"): issues.append("caption_no_contrast_border")
    if not manifest.get("japanese_narration_verified"): issues.append("japanese_narration_missing")
    if not manifest.get("speech_sync_verified"): issues.append("speech_sync_missing")
    if not manifest.get("assets_approved"): issues.append("asset_approval_missing")
    if not manifest.get("employee_approved"): issues.append("employee_approval_missing")
    return {"publication_approved":not issues,"issues":issues}
