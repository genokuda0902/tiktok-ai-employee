"""Pure stdlib safe-frame timeline for local Chromium screenshot demos across 10 genres."""
from dataclasses import dataclass
W,H,FPS,FRAMES=1080,1920,30,691
GENRES=('ai_productivity','beauty','romance_psychology','money_saving','sales_business','career','health_lifestyle','trivia_science','travel_food','product_lifestyle')
CAPTION_TOP=1438
BROWSER_BOX=(110,520,970,1210)
STAGES={
    4:('prompt',('initial','goal','rule','style','confirmed'),(254,270,287,304,321,341)),
    5:('review',('initial','number','content','expression','approved'),(341,358,375,392,409,426)),
    7:('save',('initial','focused','saved'),(518,544,570,596)),
}
ORIGINAL={
    1:((0,24),(24,56),(56,93)),2:((93,118),(118,145),(145,176)),
    3:((176,254),),6:((426,518),),8:((596,691),),
}
@dataclass(frozen=True)
class Clip:
    scene:int
    stage:int
    start:int
    end:int
    source:str

def timeline():
    items=[]
    for scene in range(1,9):
        if scene in STAGES:
            name,steps,bounds=STAGES[scene]
            items.extend(Clip(scene,i,bounds[i],bounds[i+1],f'chromium_{name}_{step}') for i,step in enumerate(steps))
        else:
            items.extend(Clip(scene,i,a,b,f'slide_{scene:02d}_stage{i}') for i,(a,b) in enumerate(ORIGINAL[scene]))
    return tuple(items)

def validate(genre='ai_productivity',clips=None,box=BROWSER_BOX):
    if genre not in GENRES:raise ValueError('unknown genre')
    a,b,c,d=box
    if not (50<=a<c<=W-50 and 160<=b<d<CAPTION_TOP-50):raise ValueError('browser overlaps caption or margins')
    clips=timeline() if clips is None else tuple(clips)
    if not clips or clips[0].start!=0 or clips[-1].end!=FRAMES:raise ValueError('missing full duration')
    for i,clip in enumerate(clips):
        if not (1<=clip.scene<=8 and 0<=clip.start<clip.end<=FRAMES):raise ValueError('invalid clip')
        if i and clips[i-1].end!=clip.start:raise ValueError('frame gap/overlap')
        if i and clips[i-1].scene>clip.scene:raise ValueError('scene order')
        if i and clips[i-1].scene==clip.scene and clips[i-1].stage+1!=clip.stage:raise ValueError('stage order')
    if len(clips)!=22 or len({x.scene for x in clips})!=8:raise ValueError('missing scenes/states')
    if sum(x.scene in STAGES for x in clips)!=13:raise ValueError('browser screenshot count mismatch')
    return True

def safe_browser_source(url,external_requests=0,has_personal_data=False):
    """Fail closed: only in-memory local HTML, no external page or user data."""
    if url!='about:blank / page.set_content(local HTML)' or external_requests or has_personal_data:
        raise ValueError('unsafe browser recording provenance')
    return True
