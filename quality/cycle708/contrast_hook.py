"""Reusable, rights-safe, visually contrasting opening hook for 10 content genres.

Illustrative UI only; never claims a measured speed improvement. All graphics
are generated with Pillow primitives and contain no real employee/customer data.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class HookCopy:
    before: str = '手作業'
    after: str = 'AIで整理'
    footnote: str = '※効果は作業内容により異なります'

def validate_hook(copy: HookCopy):
    for label in (copy.before, copy.after):
        if not label or len(label) > 9:
            raise ValueError('Hook label must be 1–9 characters')
    if any(bad in (copy.before + copy.after + copy.footnote) for bad in ('90%削減', '一瞬で完成', '必ず', '100%改善')):
        raise ValueError('Unverified outcome claim')
    return True

def ease(v):
    v = min(1.0,max(0.0,float(v)))
    return v*v*(3-2*v)

def render_hook(d, t, *, label, panel, text, smooth, robot):
    """Draw in the parent renderer's 720x1280 authored coordinate system."""
    validate_hook(label)
    panel(d,(52,343,668,912),'#0b2542',22,outline='#58c0ea',width=3)
    panel(d,(70,365,346,844),'#203348',17)
    panel(d,(371,365,650,844),'#0b3d52',17)
    panel(d,(85,382,331,443),'#3a495c',12)
    panel(d,(387,382,635,443),'#087c82',12)
    text(d,(121,394),label.before,30,'#f4f8ff')
    text(d,(418,394),label.after,30,'#f4ffff')
    for i in range(5):
        x=104+i*16; y=662-i*19
        panel(d,(x,y,x+150,y+58),'#e6eaf0',8,outline='#afbacb',width=1)
        for j in range(3): d.line((x+15,y+16+j*11,x+111,y+16+j*11),fill='#8ca0b5',width=2)
    d.ellipse((167,486,247,566),fill='#dfb9a5')
    panel(d,(149,552,267,675),'#526d83',22)
    d.line((165,604,123,644),fill='#dfb9a5',width=15)
    d.line((250,601,286,642),fill='#dfb9a5',width=15)
    d.ellipse((113,457,170,514),fill='#0d1e31',outline='#97b0c7',width=3)
    d.line((141,485,141,466),fill='#e7f4ff',width=3)
    d.line((141,485,155,495),fill='#e7f4ff',width=3)
    values=(120,150,200,180)
    progress=ease((t-.30)/1.25)
    for j in range(4): d.line((402,760-j*67,627,760-j*67),fill='#386779',width=2)
    for i,v in enumerate(values):
        p=ease((progress*1.5-i*.16))
        height=round((v/200)*238*p)
        x=405+i*57
        if height>2: panel(d,(x,759-height,x+37,759),'#18e1d1' if i==2 else '#2aaaf3',7)
        text(d,(x+4,770),f'{i+1}月',17,'#e1f5ff')
    if t>=1.35:
        panel(d,(394,471,626,533),'#084c55',12,outline='#56ffda',width=2)
        text(d,(409,480),'3月 20万円',27,'#e9fff6')
    x=346+int(16*ease((t-.4)/.8))
    d.line((x,564,x,658),fill='#91fff2',width=9)
    d.polygon(((x-14,646),(x+14,646),(x,675)),fill='#91fff2')
    panel(d,(80,854,639,902),'#0d3952',12)
    text(d,(94,865),label.footnote,21,'#bde0ec')
    d.ellipse((604,320,622,338),fill='#50f5d4')
