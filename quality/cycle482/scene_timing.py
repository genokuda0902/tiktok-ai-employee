"""Scene timing validation for review-only video edits."""

def validate_timeline(items, duration):
    if not items or items[0][0] != 0:
        raise ValueError('missing first scene')
    if abs(items[-1][1] - duration) > 0.08:
        raise ValueError('missing end scene')
    for i, (start, end) in enumerate(items):
        if end <= start:
            raise ValueError('invalid scene duration')
        if i and abs(start - items[i - 1][1]) > 0.05:
            raise ValueError('scene gap or overlap')
    return True
