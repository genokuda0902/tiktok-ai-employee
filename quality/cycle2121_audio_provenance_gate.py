"""Cycle 2121: publishing requires verified script-aligned Japanese narration."""

def can_publish(*, narration_origin, japanese_verified, subtitle_synced, approved):
    return (narration_origin == 'generated_from_current_script'
            and japanese_verified and subtitle_synced and approved)

def test_inherited_audio_blocked():
    assert not can_publish(narration_origin='inherited', japanese_verified=False,
                           subtitle_synced=False, approved=False)

def test_verified_audio_still_needs_approval():
    assert not can_publish(narration_origin='generated_from_current_script',
                           japanese_verified=True, subtitle_synced=True, approved=False)
