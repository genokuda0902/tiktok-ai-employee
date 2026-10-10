"""Cycle468 reusable scene timeline validator."""

def validate(scenes):
    if len(scenes) != 8:
        raise ValueError('expected eight scenes')
    cursor = 0.0
    keyframes = 0
    for scene in scenes:
        if abs(scene['start'] - cursor) > 0.001:
            raise ValueError('timeline gap')
        if scene['end'] <= scene['start']:
            raise ValueError('invalid scene length')
        if not scene['caption'] or len(scene['caption']) > 28:
            raise ValueError('caption length')
        keyframes += scene['keyframes']
        cursor = scene['end']
    if scenes[0]['end'] > 1.5 or abs(cursor - 20) > 0.001:
        raise ValueError('timing')
    if keyframes < 16:
        raise ValueError('not enough visual states')
    return True
