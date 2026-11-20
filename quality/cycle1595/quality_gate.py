"""Fail-closed quality gate. Presence of audio is not proof of Japanese speech."""
REQUIRED = ("video_decodes", "audio_present", "japanese_speech_verified", "captions_synced", "assets_approved", "privacy_approved", "employee_approved")
def evaluate(evidence):
    missing = [k for k in REQUIRED if evidence.get(k) is not True]
    return {"publication_ready": not missing, "missing": missing}
