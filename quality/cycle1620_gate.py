"""Cross-genre publication gate: missing evidence must fail closed."""
REQUIRED = ("audio_present", "speech_synced_captions", "asset_rights_approved", "privacy_approved", "employee_approved")
def publication_ready(qa):
    return (qa.get("video_decode") == "PASS"
            and qa.get("width", 0) >= 720 and qa.get("height", 0) >= 1280
            and all(qa.get(k) is True for k in REQUIRED))
