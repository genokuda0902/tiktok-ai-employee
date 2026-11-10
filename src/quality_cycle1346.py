"""Reject review-only videos that lack verified Japanese narration."""
def publication_gate(metadata):
    required = ("narration_language", "narration_verified", "captions_synced",
                "asset_rights_approved", "human_approved")
    missing = [k for k in required if not metadata.get(k)]
    if metadata.get("narration_language") != "ja":
        missing.append("japanese_narration")
    return {"posting_allowed": not missing, "missing": sorted(set(missing))}
