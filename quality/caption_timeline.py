"""Shared, genre-independent timeline validation for review renders."""
def validate_scenes(scenes, duration):
    if not scenes or duration <= 0:
        return False
    if scenes[0][0] != 0 or scenes[-1][1] != duration:
        return False
    return all(start < end and (i == 0 or scenes[i-1][1] == start)
               for i, (start, end) in enumerate(scenes))

def publication_approved(has_japanese_voice, synchronized_captions, rights_cleared, employee_approved):
    return all((has_japanese_voice, synchronized_captions, rights_cleared, employee_approved))
