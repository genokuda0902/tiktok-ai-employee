"""Fail-closed review metadata checks shared across genres."""
def review_status(metadata):
    required = ("japanese_narration", "speech_synced_captions", "approved_assets", "employee_approved", "reproducible_renderer")
    return "APPROVED_FOR_MANUAL_REVIEW" if all(metadata.get(k) is True for k in required) else "PUBLICATION_NOT_APPROVED"
