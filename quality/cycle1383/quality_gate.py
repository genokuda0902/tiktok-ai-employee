"""Fail-closed publication gate for review-only MP4 across all genres."""
def publication_allowed(meta: dict) -> bool:
    return all((
        meta.get("video_decodes") is True,
        meta.get("narration_japanese_verified") is True,
        meta.get("captions_synced_verified") is True,
        meta.get("assets_rights_approved") is True,
        meta.get("privacy_review_passed") is True,
        meta.get("employee_approved") is True,
        meta.get("manual_post_only") is True,
    ))

def validate_excel_example(values, formula, expected):
    if formula != "=SUM(B2:B5)":
        return False
    return len(values) == 4 and sum(values) == expected
