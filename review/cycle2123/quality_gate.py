"""Cycle2123: block release when narration is inherited or unverified."""

def release_allowed(meta: dict) -> bool:
    required = ('japanese_voice_verified', 'caption_audio_sync_verified', 'rights_cleared', 'employee_approved')
    return all(meta.get(key) is True for key in required) and meta.get('audio_source') == 'same_script_tts'


def test_inherited_audio_is_blocked():
    assert not release_allowed({'audio_source': 'cycle2121_inherited', 'japanese_voice_verified': False})


def test_fully_verified_audio_can_pass():
    assert release_allowed({'audio_source':'same_script_tts', 'japanese_voice_verified':True, 'caption_audio_sync_verified':True, 'rights_cleared':True, 'employee_approved':True})
