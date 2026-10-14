"""Reusable three-stage synthetic UI action cue; review-only, no network/posting."""
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_productivity','beauty','relationships','finance','sales',
          'career','health','science','travel','products')
SIZE = (1080, 1920)
FPS = 30
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STAGES = ('input','submit','ack')

@dataclass(frozen=True)
class ActionTrace:
    genre: str
    message: str
    stage_times: tuple = (0.0, 1.85, 2.40, 3.0)
    def validate(self):
        if self.genre not in GENRES:
            raise ValueError('unknown genre')
        if not (self.message and len(self.message) <= 54 and '\n' not in self.message):
            raise ValueError('message must be one line and <=54 chars')
        if len(self.stage_times) != 4 or self.stage_times[0] != 0 or self.stage_times[-1] != 3:
            raise ValueError('expected 3-second action trace')
        if not all(a < b for a,b in zip(self.stage_times,self.stage_times[1:])):
            raise ValueError('invalid stage order')
        return True


def stage_at(trace, seconds):
    trace.validate()
    if not 0 <= seconds < 3:
        raise ValueError('time out of range')
    return STAGES[0 if seconds < trace.stage_times[1] else 1 if seconds < trace.stage_times[2] else 2]


def frame(base, trace, idx):
    trace.validate()
    if base.size != SIZE or not 0 <= idx < FPS*3:
        raise ValueError('invalid frame')
    t = idx/FPS
    stage = stage_at(trace,t)
    im = base.copy().convert('RGB')
    d = ImageDraw.Draw(im)
    # Only the synthetic prompt card is redrawn. Existing headline, data and burned captions remain.
    d.rounded_rectangle((79,1207,1005,1603),radius=22,fill='#f0f6fd',outline='#54d7d0',width=5)
    f = ImageFont.truetype(BOLD,42)
    small = ImageFont.truetype(FONT,27)
    title = ImageFont.truetype(BOLD,31)
    d.text((112,1226),'入力内容（架空の操作再現）',font=title,fill='#152d43')
    # The reveal is an action trace, not a claim that an AI model was actually invoked.
    visible = max(0,min(len(trace.message),round(len(trace.message)*min(t/1.75,1))))
    line1 = trace.message[:visible][:22]
    line2 = trace.message[:visible][22:]
    d.text((112,1302),line1,font=f,fill='#102c40')
    d.text((112,1363),line2,font=f,fill='#102c40')
    if stage == 'input' and idx % 24 < 16:
        cursor_x = 112 + int(d.textlength(line2 if len(trace.message[:visible])>22 else line1,font=f))
        cursor_y = 1363 if len(trace.message[:visible])>22 else 1302
        d.rectangle((min(cursor_x,920),cursor_y+5,min(cursor_x+5,925),cursor_y+47),fill='#00a99d')
    d.text((112,1470),'01 入力   →   02 送信   →   03 確認',font=small,fill='#376578')
    active = {'input':0,'submit':1,'ack':2}[stage]
    for k in range(3):
        d.rounded_rectangle((113+145*k,1520,242+145*k,1532),radius=6,
                            fill='#008e87' if k<=active else '#a7c4cc')
    color = '#087e7b' if stage != 'submit' else '#f1b44c'
    d.rounded_rectangle((691,1492,964,1578),radius=22,fill=color)
    label = '入力中' if stage=='input' else '送信操作' if stage=='submit' else '送信済み（再現）'
    d.text((714,1511),label,font=title,fill='white' if stage!='submit' else '#13283c')
    # Pointer + expanding click ring. Confined to content area, away from caption safe zone.
    if stage != 'input':
        px,py = (884,1532)
        d.polygon([(px,py),(px+6,py+39),(px+16,py+28),(px+32,py+49),
                   (px+44,py+43),(px+29,py+20),(px+48,py+20)],fill='#ffffff',outline='#15314a')
        if stage == 'submit':
            r = int(13+35*(t-trace.stage_times[1])/(trace.stage_times[2]-trace.stage_times[1]))
            d.ellipse((px-r,py-r,px+r,py+r),outline='#ffe4a5',width=5)
    return im

DEFAULT = ActionTrace('ai_productivity','4か月の売上120・150・200・250を合計し、式と結果を表示')
