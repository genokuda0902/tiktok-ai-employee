"""Pure validation for synthetic proof scenes. Never grants publication approval."""
GENRES={'ai_work','beauty','relationship','money','sales','career','health','science','travel','products'}
def validate(m):
    assert m.get('genre') in GENRES
    assert m.get('rights') == 'synthetic_local_review_only'
    assert m.get('privacy_checked') is True
    assert m.get('publication') == 'NOT_APPROVED'
    assert m.get('human_review') == 'HUMAN_REVIEW'
    assert m.get('auto_post') is False
    values=m.get('values')
    assert isinstance(values,list) and len(values)==4
    assert all(type(x) is int and 0<=x<=9999 for x in values)
    return sum(values)
