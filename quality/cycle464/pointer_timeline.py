"""Synthetic cursor focus. Never draw in the subtitle band."""
from PIL import ImageDraw
PATHS={
 'before':[(380,542),(380,716),(380,890)],
 'data':[(550,554),(550,669),(550,787)],
 'formula':[(118,440),(440,441),(610,441)],
 'proof':[(320,541),(320,655),(320,771)],
 'result':[(180,500),(320,735)],
 'compare':[(188,645),(523,645)],
 'cta':[(347,607)],
}
def location(kind,progress):
    if kind not in PATHS:return None
    if not 0<=progress<=1:raise ValueError('invalid progress')
    points=PATHS[kind]
    i=min(len(points)-1,int(progress*len(points)))
    return points[i]
def render_pointer(image,kind,progress):
    p=location(kind,progress)
    if p is None:return False
    x,y=p
    if not (60<=x<=660 and 345<=y<=970):raise ValueError('unsafe pointer')
    d=ImageDraw.Draw(image,'RGBA')
    d.ellipse((x-22,y-22,x+22,y+22),outline=(100,240,225,180),width=3)
    d.polygon([(x,y),(x+3,y+38),(x+13,y+27),(x+25,y+48),(x+33,y+43),(x+23,y+23),(x+36,y+22)],fill='white',outline='#163044',width=3)
    return True
