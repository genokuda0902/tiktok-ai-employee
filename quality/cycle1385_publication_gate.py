"""Cycle 1385: fail-closed publication gate, independent of genre."""
def publication_allowed(meta):
    required = ("asset_rights_approved", "privacy_review_passed", "narration_verified", "captions_synced", "visual_review_passed", "recipient_file_verified", "employee_approved")
    return all(meta.get(k) is True for k in required) and meta.get("manual_post_only") is True

def test_silent_video_rejected():
    m = dict.fromkeys(("asset_rights_approved", "privacy_review_passed", "narration_verified", "captions_synced", "visual_review_passed", "recipient_file_verified", "employee_approved"), True)
    m["manual_post_only"] = True
    m["narration_verified"] = False
    assert not publication_allowed(m)

def test_missing_approval_rejected():
    assert not publication_allowed({"manual_post_only": True})
