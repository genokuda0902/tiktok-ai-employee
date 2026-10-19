"""Ten-genre proof-first 0–2s hook contract. Synthetic review only."""
from dataclasses import dataclass
GENRES=('ai_productivity','trivia','cooking','beauty','finance','wellness','travel','product_demo','story','business')
FPS=30
FRAMES=60
SAFE_TOP=192
SAFE_BOTTOM=1536
@dataclass(frozen=True)
class Hook:
    genre:str
    title:str
    before:str
    after:str
    evidence:str
    synthetic:bool=True
    rights:str='ORIGINAL_SYNTHETIC_REVIEW_ONLY'
    approval:bool=False
def easing(x):
    x=max(0.,min(1.,float(x)))
    return x*x*(3.-2.*x)
def state(index,total=FRAMES):
    if total<2 or not isinstance(index,int) or not 0<=index<total: raise ValueError('invalid frame')
    p=easing(index/(total-1))
    return {'progress':p,'before_offset':round(-45*p),'after_offset':round(50*(1-p))}
def validate(hook):
    if hook.genre not in GENRES: raise ValueError('unsupported genre')
    if not hook.synthetic or hook.rights!='ORIGINAL_SYNTHETIC_REVIEW_ONLY' or hook.approval: raise ValueError('unsafe media')
    if any(not isinstance(v,str) or not v.strip() for v in (hook.title,hook.before,hook.after,hook.evidence)): raise ValueError('missing evidence')
    if any(t in hook.title+hook.after for t in ('必ず','100%正確','10分→1分','数秒で完了')): raise ValueError('unmeasured claim')
    return True
def publication_gate(*,rights_approved=False,native_ja=False,subtitles_synced=False,staff_approved=False,phone_playback_verified=False):
    return all((rights_approved,native_ja,subtitles_synced,staff_approved,phone_playback_verified))
