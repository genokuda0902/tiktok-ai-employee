"""10-genre-safe overlay geometry and scene-aligned visual cues. NOT voice subtitles."""
from dataclasses import dataclass
WIDTH,HEIGHT=540,960
SAFE_TOP,SAFE_BOTTOM=112,748
@dataclass(frozen=True)
class TextRegion:
    name:str
    x1:int
    y1:int
    x2:int
    y2:int
    def safe(self):
        return 20<=self.x1<self.x2<=WIDTH-20 and SAFE_TOP<=self.y1<self.y2<=SAFE_BOTTOM
    def overlaps(self,other):
        return self.x1<other.x2 and other.x1<self.x2 and self.y1<other.y2 and other.y1<self.y2
PRIMARY_TITLE=TextRegion('headline',35,139,505,193)
FORMULA_UI=TextRegion('formula',79,620,464,694)
FOCUS_STRIP=TextRegion('focus_steps',82,716,465,747)
def validate_layout():
    assert PRIMARY_TITLE.safe() and FORMULA_UI.safe() and FOCUS_STRIP.safe()
    assert not PRIMARY_TITLE.overlaps(FORMULA_UI)
    assert not PRIMARY_TITLE.overlaps(FOCUS_STRIP)
    assert not FORMULA_UI.overlaps(FOCUS_STRIP)
    return True
def cue_file(scenes,fps=30):
    """SRT-style visual text cues; speech alignment NOT verified."""
    def stamp(frame):
        ms=round(frame*1000/fps)
        h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
        return f'{h:02}:{m:02}:{s:02},{ms:03}'
    lines=[]
    for index,(start,end,caption,kind) in enumerate(scenes,1):
        if start>=end or not caption or len(caption)>20:raise ValueError('invalid cue')
        lines.extend([str(index),f'{stamp(start)} --> {stamp(end)}',caption,''])
    return '\n'.join(lines)
