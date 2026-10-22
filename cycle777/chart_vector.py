"""Original vector storyboard scene. Review-only, no external assets."""
from PIL import Image,ImageDraw,ImageFont
from chart_contract import GENRES,MONTHS,phase,START
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def draw(genre,frame):
    if genre not in GENRES:raise ValueError("genre")
    status=phase(frame)
    accent=GENRES[genre]
    im=Image.new("RGB",(1080,1920),"#0A2035")
    d=ImageDraw.Draw(im)
    f=lambda n:ImageFont.truetype(FONT,n)
    d.text((80,290),"Excelに貼って、",font=f(70),fill="white")
    d.text((80,390),"変化を見せる。",font=f(70),fill=accent)
    d.rounded_rectangle((70,600,1010,1460),radius=30,fill="#F4F8FC")
    d.rounded_rectangle((85,620,995,710),radius=20,fill="#155E49")
    d.text((115,642),"月別売上 / 架空データ",font=f(36),fill="white")
    count=4 if status=="verify" else max(1,min(4,int(((frame-START)/30+.02)/.43)+1))
    for i,(month,value) in enumerate(MONTHS.items()):
        y=770+i*70
        if i<count:
            d.text((145,y),month,font=f(35),fill="#1C4357")
            d.text((490,y),f"{value:,} 円",font=f(35),fill="#1C4357")
        d.line((135,y+60,940,y+60),fill="#DCE8EC",width=2)
    for i,(month,value) in enumerate(MONTHS.items()):
        x=260+i*166
        h=int(160*value/200000) if status=="verify" else int(160*value/200000*min(1,max(0,((frame-START)/30-.5)*1.3-i*.25)))
        if h:d.rounded_rectangle((x,1350-h,x+85,1350),radius=8,fill=accent)
        d.text((x+12,1360),month,font=f(28),fill="#244A61")
    if status=="verify":
        d.rounded_rectangle((460,1080,930,1150),radius=15,fill="#126B5C")
        d.text((480,1092),"合計 650,000円",font=f(38),fill="white")
    d.text((85,1560),"表 → グラフ → 合計を確認",font=f(42),fill="white")
    d.text((85,1700),"※ 架空データ / 操作の再現イメージ",font=f(29),fill="#C0D6E2")
    return im
