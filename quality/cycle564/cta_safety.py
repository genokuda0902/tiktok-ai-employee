GENRES = ('AI・仕事効率化', '営業・ビジネス')

def validate_review(genre, approved):
    if genre not in GENRES or approved:
        raise ValueError('human review required')
    return True
