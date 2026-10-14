"""Cycle582 original synthetic result-first hook, no third-party assets."""
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont

FPS = 30
SIZE = (1080, 1920)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = ('ai_productivity','beauty','relationships','finance','sales',
          'career','health','science','travel','products')

@dataclass(frozen=True)
class Hook:
    genre: str
    question: str
    answer: str
    label: str
    sample: str
    verified: bool = False

    def validate(self):
        if self.genre not in GENRES:
            raise ValueError('unsupported genre')
        if not self.verified:
            raise ValueError('result-first claim must be verified against sample')
        for item in (self.question, self.answer, self.label, self.sample):
            if not item or len(item) > 32 or '\n' in item:
                raise ValueError('missing, long, or multiline hook text')
        return True

DEFAULT = Hook('ai_productivity', 'その合計、まだ手計算？', '答えは 720',
               '120＋150＋200＋250', '架空データの計算例', True)

def _font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else FONT, size)

def _center(d, y, msg, font, color):
    w = d.textlength(msg, font=font)
    d.text(((1080-w)/2, y), msg, font=font, fill=color)

def render_frame(spec: Hook, frame_index: int) -> Image.Image:
    spec.validate()
    if not 0 <= frame_index < 2*FPS:
        raise ValueError('frame outside 2s hook')
    t = frame_index/FPS
    im = Image.new('RGB', SIZE)
    d = ImageDraw.Draw(im)
    for y in range(1920):
        p = y/1920
        d.line([(0,y),(1080,y)],fill=(int(9+7*p),int(25+19*p),int(46+26*p)))
    d.rounded_rectangle((66,78,1014,184),radius=26,fill='#073c52',outline='#19d2c9',width=4)
    _center(d,104,'AI時短ラボ  |  検証デモ',_font(42,True),'#f2ffff')
    _center(d,290,spec.question,_font(66,True),'#ffffff')
    d.rounded_rectangle((64,515,1016,1270),radius=42,fill='#071e35',outline='#35647b',width=4)
    d.rounded_rectangle((100,575,980,755),radius=24,fill='#173d53')
    _center(d,603,'入力した4つの数字',_font(38),'#cde6ef')
    _center(d,660,'120   150   200   250',_font(52,True),'#ffffff')
    d.rounded_rectangle((100,810,980,1170),radius=28,fill='#0a585a',outline='#1ae1ce',width=5)
    val = round(720*min(1,max(0,(t-.25)/.65)))
    _center(d,837,spec.answer if t>=.92 else '合計を検算中…',_font(44,True),'#e2ffff')
    _center(d,909,str(val),_font(120,True),'#ffffff')
    _center(d,1090,'=SUM(B2:B5)',_font(43,True),'#bcfff6')
    d.rounded_rectangle((68,1370,1012,1530),radius=30,fill='#123f52')
    _center(d,1401,'手入力と関数で、同じ結果を確認',_font(41,True),'#e5f9ff')
    d.rounded_rectangle((68,1662,1012,1762),radius=20,fill='#096b70')
    _center(d,1682,'手計算の前に、合計720を確認',_font(42,True),'#ffffff')
    _center(d,1810,spec.sample+'  |  REVIEW ONLY',_font(26),'#afcad5')
    return im
