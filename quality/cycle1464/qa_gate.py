"""Fail-closed QA for review-only video assets (cycle1464)."""
def publishable(m):
    return bool(
        m.get("narration_language") == "ja"
        and m.get("speech_aligned_captions")
        and m.get("assets_approved")
        and m.get("employee_approved")
        and m.get("publication_approved")
    )
