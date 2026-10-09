def validate_evidence(rows, shown_ids, caption, manifest):
    ids = [r.get("id") for r in rows]
    if not rows or any(not x for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("invalid source rows")
    expected = [r["id"] for r in rows if r.get("status") == "未対応"]
    if not expected or sorted(expected) != sorted(shown_ids):
        raise ValueError("evidence mismatch")
    if any(x not in caption for x in expected):
        raise ValueError("caption mismatch")
    if manifest.get("rights") != "SYNTHETIC_ORIGINAL":
        raise ValueError("rights missing")
    if manifest.get("publication") != "NOT_APPROVED" or manifest.get("auto_post") is not False:
        raise ValueError("not approved for publication")
    if not manifest.get("voice_verified_japanese"):
        return "REVIEW_ONLY_NARRATION_MISSING"
    if not manifest.get("caption_voice_sync_verified"):
        return "REVIEW_ONLY_SYNC_UNVERIFIED"
    return "HUMAN_REVIEW_REQUIRED"
