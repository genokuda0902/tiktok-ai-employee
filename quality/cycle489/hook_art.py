"""Review-only animated evidence hook: 45 frames at 30fps."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from contract import validate, VALUES
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def draw(i):
    validate()
    im=Image.new('RGB',(1080,1920),'#0C223B')
    d=ImageDraw.Draw(im)
    f=ImageFont.truetype(FONT,72)
    d.text((80,170),'4つの数字、まだ手作業？',font=f,fill='white')
    for j,v in enumerate(VALUES):
        x=90+j*240
        h=round(v*1.5*i/44)
        d.rectangle((x,1250-h,x+160,1250),fill='#4AC3E7')
        d.text((x,1310),str(v),font=f,fill='white')
    d.text((100,1540),'合計 720（架空データ）',font=f,fill='#FFE08A')
    return im
def frames(folder):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for i in range(45):draw(i).save(folder/f'{i:03d}.png')
    return folder
