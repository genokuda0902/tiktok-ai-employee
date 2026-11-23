"""Fail-closed media QA: audio track is not proof of Japanese narration."""
def publication_allowed(q):
    return bool(q.get("width")==1080 and q.get("height")==1920 and q.get("audio_streams",0)>0 and all(q.get(k,False) for k in ("japanese_speech_verified","caption_speech_sync_verified","asset_rights_approved","employee_approved")))
