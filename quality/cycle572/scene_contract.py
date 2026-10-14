"""Cycle572: review-only 10-genre before/after evidence contract.

Scene renderer source and MP4 are separately archived in the cycle572 QA bundle.
No publication approval or real-world time-savings claim is implied.
"""
VALUES=(120,150,200,250)
GENRES=('ai_productivity','business','education','science','technology','finance','lifestyle','travel','food','entertainment')
SCENE_START=16.0
SCENE_END=18.5

def proof(values=VALUES):
    if not values or any(not isinstance(v,int) or v<0 for v in values):
        raise ValueError('invalid synthetic values')
    return sum(values)

def gate(meta):
    if meta.get('publication')!='NOT_APPROVED' or meta.get('auto_post') is not False:
        raise ValueError('Fail closed: review-only video')
    if not meta.get('synthetic') or not meta.get('rights_checked'):
        raise ValueError('Fail closed: provenance required')
    return True

def scene_config(genre='ai_productivity'):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    return dict(genre=genre,scene='before_after_evidence',
                start=SCENE_START,end=SCENE_END,
                synthetic_values=VALUES,verified_sum=proof(),
                narration='ABSENT',publication='NOT_APPROVED')
