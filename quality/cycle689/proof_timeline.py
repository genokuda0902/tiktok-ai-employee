"""Review-only, ten-genre proof timeline and publication fail-closed contract."""
from dataclasses import dataclass

GENRES = ('ai_productivity','trivia','cooking','beauty','finance','wellness','travel','product_demo','story','business')

@dataclass(frozen=True)
class Beat:
    start: float
    end: float
    cumulative: int
    highlighted_index: int

def proof_beats(values=(120,150,200,180), start=14.0, end=16.0):
    if not isinstance(values,(list,tuple)) or len(values)!=4 or any(type(x) is not int or x<0 for x in values):
        raise ValueError('four nonnegative integer example values required')
    if not 0<=start<end<=20: raise ValueError('invalid proof interval')
    dt=(end-start)/4
    return tuple(Beat(round(start+i*dt,3),round(start+(i+1)*dt,3),sum(values[:i+1]),i) for i in range(4))

def validate_release(meta, genre):
    if genre not in GENRES: raise ValueError('unsupported genre')
    if meta.get('synthetic') is not True or meta.get('rights')!='ORIGINAL_SYNTHETIC_REVIEW_ONLY':
        raise ValueError('asset rights not proven')
    if meta.get('human_approved') is not False or meta.get('auto_post') is not False:
        raise ValueError('review gate bypass')
    if meta.get('voice') not in ('MISSING','NATIVE_JA_UNREVIEWED'):
        raise ValueError('unverified/foreign-language voice is not Japanese')
    if meta.get('voice')=='NATIVE_JA_UNREVIEWED' and not meta.get('voice_proof_sha256'):
        raise ValueError('native voice requires evidence')
    return True
