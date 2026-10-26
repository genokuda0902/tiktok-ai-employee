"""Genre-independent browser-motion planning for review-only TikTok slideshows.
No external API, personal data, auto-posting, or paid service.
"""
from __future__ import annotations

PALETTES = {
    'ai_productivity':'#28D7BE', 'career':'#FFBB68', 'money':'#82DBAA',
    'health':'#87CFFB', 'learning':'#BEA7FF', 'beauty':'#F4A4C5',
    'travel':'#78C6FA', 'food':'#F6B778', 'home':'#A5DC8E',
    'business':'#82A9FF'
}
VIDEO_SIZE=(1080,1920)
VIDEO_FPS=30
OLD_CAPTURE_FPS=5
NEW_CAPTURE_FPS=15
DEMO_START=8.5
DEMO_END=17.3
ACTIONS=((0.4,'purpose','進捗報告を作成'),(1.2,'condition','4件を集計'),
         (1.8,'t0',None),(2.2,'t1',None),(2.6,'t2',None),
         (3.5,'generate',None),(5.9,'revise',None))

def smoothstep(x:float)->float:
    x=max(0.0,min(1.0,float(x)))
    return x*x*(3.0-2.0*x)

def interpolate(start:tuple[float,float],end:tuple[float,float],fraction:float)->tuple[float,float]:
    f=smoothstep(fraction)
    return (start[0]+(end[0]-start[0])*f,
            start[1]+(end[1]-start[1])*f)

def pointer_at(t:float,targets:list[tuple[float,float]],lead:float=0.52)->tuple[float,float]:
    """C1-continuous cursor path; arrives at each target before click."""
    if len(targets)!=len(ACTIONS): raise ValueError('target count must equal action count')
    current=(60.0,80.0)
    previous_time=0.0
    for (action_time,_,_),target in zip(ACTIONS,targets):
        start=max(previous_time,action_time-lead)
        end=action_time-0.06
        if t<start:return current
        if t<end:return interpolate(current,target,(t-start)/(end-start))
        current=target
        previous_time=action_time
    return current

def validate_genre(name:str)->str:
    if name not in PALETTES:raise ValueError('unsupported genre')
    return PALETTES[name]

def expected_frames(fps:int=NEW_CAPTURE_FPS)->int:
    if fps<=0 or VIDEO_FPS%fps!=0:raise ValueError('capture fps must divide output fps')
    return round((DEMO_END-DEMO_START)*fps)

def report_stats(done:int,total:int=4)->dict:
    if total<=0 or done<0 or done>total:raise ValueError('invalid completion')
    return {'done':done,'total':total,'pending':total-done,'percent':round(100*done/total)}

def progress_monotonic(states:list[dict])->bool:
    p=[s['percent'] for s in states]
    return all(a<=b for a,b in zip(p,p[1:]))
