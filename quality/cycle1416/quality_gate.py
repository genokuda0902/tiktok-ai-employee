"""Fail-closed publication gate, reusable across all 10 content genres."""

def evaluate(video_present, japanese_voice, speech_synced_captions, asset_rights_approved, employee_approved, decoded_ok):
    checks = {
        'video_present': bool(video_present),
        'japanese_voice': bool(japanese_voice),
        'speech_synced_captions': bool(speech_synced_captions),
        'asset_rights_approved': bool(asset_rights_approved),
        'employee_approved': bool(employee_approved),
        'decoded_ok': bool(decoded_ok),
    }
    return {'publication_approved': all(checks.values()), 'checks': checks}
