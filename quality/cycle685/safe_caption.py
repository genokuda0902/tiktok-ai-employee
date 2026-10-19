"""Pixel-measured Japanese screen captions (NOT verified speech subtitles)."""
from dataclasses import dataclass
SAFE=(88,1365,994,1530)
GENRES=('ai_productivity','trivia','cooking','beauty','finance','wellness','travel','product_demo','story','business')
@dataclass(frozen=True)
class Layout:
    lines: tuple[str,...]
    size: int
    line_height: int
    box: tuple[int,int,int,int]
def wrap_caption(text,font_factory):
    from PIL import Image,ImageDraw
    if not isinstance(text,str) or not text.strip(): raise ValueError('empty')
    draw=ImageDraw.Draw(Image.new('RGB',(1,1)))
    for size in (40,38,36,34,32):
        f=font_factory(size); lines=[]; current=''
        for ch in text:
            candidate=current+ch
            if draw.textlength(candidate,font=f)<=820: current=candidate
            else:
                if current: lines.append(current)
                current=ch
        if current: lines.append(current)
        if len(lines)<=2:
            layout=Layout(tuple(lines),size,size+12,SAFE)
            validate(layout,font_factory)
            return layout
    raise ValueError('caption overflow')
def validate(layout,font_factory):
    from PIL import Image,ImageDraw
    d=ImageDraw.Draw(Image.new('RGB',(1,1)))
    x0,y0,x1,y1=layout.box
    if x0<60 or x1>1020 or y0<1300 or y1>1536: raise ValueError('unsafe band')
    if not 1<=len(layout.lines)<=2: raise ValueError('line count')
    if y0+12+layout.line_height*len(layout.lines)>y1: raise ValueError('vertical overflow')
    if any(d.textlength(line,font=font_factory(layout.size))>x1-x0-55 for line in layout.lines):
        raise ValueError('horizontal overflow')
    return True
