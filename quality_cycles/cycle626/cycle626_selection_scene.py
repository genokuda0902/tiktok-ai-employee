"""cycle626: 10-genre reusable four-cell range selection component (review only)."""
import math
from PIL import Image,ImageDraw,ImageFont
GENRES=('ai_work','beauty','relationships','money','sales_business','career','health_lifestyle','science_trivia','travel_food','product_lifestyle')
ROW_TOP,ROW_HEIGHT,FRAMES=371,91,75
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def validate(values=(120,150,200,250),genre='ai_work',rights='SYNTHETIC_REVIEW_ONLY'):
    if genre not in GENRES:raise ValueError('unknown genre')
    if len(values)!=4 or any(type(x) is not int or x<0 for x in values):
        raise ValueError('four nonnegative integer values required')
    if rights!='SYNTHETIC_REVIEW_ONLY':raise ValueError('rights not approved')
    return {'sum':sum(values),'range':'B2:B5','publication':'NOT_APPROVED','new_japanese_voice':False}
def selection_rect():
    return (173,ROW_TOP,350,ROW_TOP+4*ROW_HEIGHT)
def selected_rows(t):
    return max(0,min(4,math.floor((t-.22)/.30)+1))
def frame(i,values=(120,150,200,250),genre='ai_work'):
    validate(values,genre)
    if not 0<=i<FRAMES:raise ValueError('invalid frame')
    im=Image.new('RGB',(540,960),'#041422');d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,26)
    d.text((30,140),'B2:B5  /  4件の範囲を選択',font=f,fill='white')
    n=selected_rows(i/30)
    for j,v in enumerate(values):
        y=ROW_TOP+j*ROW_HEIGHT
        d.rectangle((40,y,500,y+ROW_HEIGHT-3),fill='#bbf7e1' if j<n else '#eff7f8')
        d.text((80,y+22),str(v),font=f,fill='#065341')
    if n:
        d.rectangle((173,ROW_TOP,350,ROW_TOP+n*ROW_HEIGHT),outline='#0ca474',width=5)
    d.text((30,815),'※架空データ／投稿未承認',font=f,fill='#a9cbd7')
    return im
