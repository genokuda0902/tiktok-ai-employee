"""Fail-closed quality gate for any of the 10 TikTok genres."""
def publication_allowed(meta):
    required = ("asset_rights_approved", "privacy_approved", "employee_approved",
                "japanese_narration_verified", "captions_synced_verified",
                "visual_review_approved", "recipient_file_verified")
    return all(meta.get(k) is True for k in required)
def review_report(meta):
    return {"posting_allowed": publication_allowed(meta),
            "missing": [k for k in ("asset_rights_approved","privacy_approved",
                "employee_approved","japanese_narration_verified",
                "captions_synced_verified","visual_review_approved",
                "recipient_file_verified") if meta.get(k) is not True]}
