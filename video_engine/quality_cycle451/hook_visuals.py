"""Self-drawn evidence-first frame renderer for 1080x1920 review hook.
Use with hook_proof.ProofHook. No user/private media is accessed.
"""
import math
from PIL import Image, ImageDraw, ImageFont
from .hook_proof import ProofHook, hook_state

FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def render_frame(t, plan=None):
    p=plan or ProofHook()
    s=hook_state(p,t)
    im=Image.new("RGB",(p.width,p.height),"#09182d")
    d=ImageDraw.Draw(im)
    f=lambda size,bold=False:ImageFont.truetype(BOLD if bold else FONT,size)
    d.rounded_rectangle((62,72,1018,158),radius=25,fill="#09354d",outline="#31c3e1",width=3)
    d.text((93,87),"AI時短ラボ / DEMO",font=f(38,True),fill="#b2efff")
    d.text((84,205),f"{s['total']}件の記録。",font=f(94,True),fill="#f5fcff")
    d.text((84,323),"見落としはどこ？",font=f(74,True),fill="#f5fcff")
    for i,(ident,flag) in enumerate(p.rows):
        start=525+i*124
        if flag:
            order=s["selected"].index(i)
            y=int(start*(1-s["move"])+(720+order*164)*s["move"])
            x=int(115+40*math.sin(math.pi*s["move"]))
        else:
            y=start;x=int(115+1030*s["move"])
        if x>=1080:continue
        fill="#5c203a" if flag else "#123f53"
        edge="#ff6b99" if flag else "#438ea8"
        d.rounded_rectangle((x,y,x+860,y+84),radius=19,fill=fill,outline=edge,width=4)
        d.text((x+30,y+16),ident,font=f(42,True),fill="#eaf9ff")
        d.text((x+550,y+17),"未対応" if flag else "対応済",font=f(39,True),fill="#ff9ab4" if flag else "#a8f2da")
    if s["reveal"]>0.5:
        d.rounded_rectangle((128,1178,952,1450),radius=54,fill="#07314b",outline="#4ceffb",width=6)
        d.text((540,1216),f"{s['total']}件 → {s['count']}件",font=f(105,True),anchor="mt",fill="#ffd872")
        d.text((540,1348),"未対応だけを抽出",font=f(47,True),anchor="mt",fill="#ecf9ff")
    d.text((80,1735),s["subtitle"],font=f(35),fill="#b1d4e4")
    d.text((80,1817),"SELF-DRAWN / HUMAN REVIEW / NOT APPROVED",font=f(23),fill="#8eafc4")
    return im
