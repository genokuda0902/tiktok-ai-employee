"""Fail-closed review gate for 10-category TikTok renderers."""
def publication_ready(evidence):
    required = ("video_decodes", "japanese_speech_verified", "speech_caption_sync_verified", "assets_approved", "employee_approved")
    return all(evidence.get(key) is True for key in required)
