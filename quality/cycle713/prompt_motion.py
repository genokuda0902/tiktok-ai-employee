"""Offline, reusable 1080x1920 prompt-typing overlay; synthetic data only."""
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
LINES=('この月別売上を集計して','表と棒グラフを作って','検算手順も教えてください。')
W,H=1080,1920
@dataclass(frozen=True)
class PromptState:
    typed:str
    cursor_visible:bool
    sent:bool
    pointer_x:int
    pointer_y:int
def state_at(seconds,lines=LINES):
    if not 0<=seconds<=3: raise ValueError('scene time outside [0,3]')
    whole='\n'.join(lines)
    count=min(len(whole),int(len(whole)*min(1,seconds/2.25)))
    move=min(1,max(0,(seconds-2.30)/.40))
    return PromptState(whole[:count],int(seconds*6)%2==0,seconds>=2.72,
                       round(630+183*move),round(1074+85*move))
def make_frame(background,seconds,lines=LINES):
    if background.size!=(W,H): raise ValueError('native 1080x1920 required')
    st=state_at(seconds,lines)
    im=background.copy().convert('RGB');d=ImageDraw.Draw(im)
    f=lambda n:ImageFont.truetype(FONT,n)
    d.rounded_rectangle((91,561,989,1246),radius=38,fill='#f2faff',outline='#7cdcf3',width=5)
    d.rounded_rectangle((91,561,989,681),radius=36,fill='#0b527c')
    d.text((540,622),'AIへの指示例（架空）',font=f(48),fill='white',anchor='mm')
    d.rounded_rectangle((137,723,941,1060),radius=24,fill='#ffffff',outline='#b1cddd',width=3)
    for k,line in enumerate(st.typed.split('\n')):
        if k>=3: break
        d.text((174,782+k*100),line,font=f(46),fill='#123a54',anchor='lm')
    if st.cursor_visible and not st.sent:
        rows=st.typed.split('\n');row=min(2,len(rows)-1)
        x=174+int(d.textlength(rows[-1],font=f(46)))
        d.line((x+6,754+row*100,x+6,811+row*100),fill='#009ce2',width=6)
    d.rounded_rectangle((669,1096,918,1190),radius=25,fill='#0b86bd' if not st.sent else '#0aaf8b')
    d.text((793,1142),'送信 ✓' if st.sent else '送信 →',font=f(46),fill='white',anchor='mm')
    px,py=st.pointer_x,st.pointer_y
    d.polygon([(px,py),(px,py+52),(px+15,py+38),(px+28,py+61),(px+42,py+54),(px+29,py+31),(px+52,py+25)],fill='#ffffff',outline='#092c4b',width=4)
    if st.sent:d.ellipse((px-46,py-46,px+46,py+46),outline='#ffcf4b',width=8)
    d.text((540,1270),'架空データの操作イメージ',font=f(31),fill='#a5e3f1',anchor='mm')
    return im
