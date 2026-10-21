"""Reusable, offline, 1080x1920 three-stage end-card generator."""
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
W,H=1080,1920
@dataclass(frozen=True)
class Card:
    category:str
    title:str
    subtitle:str
    example:str
    result:str
    captions:tuple[str,str]
SCIENCE=Card("15秒でわかる","今日の1行、保存。","次は自分の手で、結果を出そう。",
             "print(2 + 3)","5",("保存して、","あとで試そう。"))
def font(size,bold=True):
    for path in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
                 "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc"):
        if Path(path).exists():return ImageFont.truetype(path,size)
    return ImageFont.truetype("DejaVuSans.ttf",size)
def text(d,xy,s,size,fill="#F5FAFB"):
    d.text(xy,s,font=font(size),fill=fill)
def box(d,coords,r=24,fill="#092536",outline="#65EBD1",width=3):
    d.rounded_rectangle(coords,radius=r,fill=fill,outline=outline,width=width)
def centered(d,area,s,size,color="#F5FAFB"):
    a,b,c,e=area; f=font(size);bounds=d.textbbox((0,0),s,font=f)
    w=bounds[2]-bounds[0];h=bounds[3]-bounds[1]
    d.text((a+(c-a-w)/2,b+(e-b-h)/2-bounds[1]),s,font=f,fill=color)
def draw(card,stage,path):
    if stage not in (0,1,2):raise ValueError("stage must be 0,1,2")
    im=Image.new("RGB",(W,H),"#061422");d=ImageDraw.Draw(im)
    for y in range(H):
        t=y/H;d.line((0,y,W,y),fill=(int(6+5*t),int(20+11*t),int(34+12*t)))
    for x in range(70,1080,160):d.line((x,245,x,1480),fill="#0D313D",width=2)
    box(d,(58,68,404,156),24,"#05474E")
    centered(d,(58,68,404,156),card.category,40)
    text(d,(825,87),"08 / 08",32,"#AAC4CD")
    box(d,(58,192,1022,208),8,"#65EBD1","#65EBD1")
    text(d,(68,278),card.title,88)
    text(d,(70,405),card.subtitle,37,"#AAC4CD")
    box(d,(57,548,1023,1447),40,"#04202E","#3AADAD",4)
    text(d,(100,594),"FIRST STEP / TRY IT YOURSELF",27,"#65EBD1")
    box(d,(96,776,986,1078),27,"#03111F","#4D7387",3)
    box(d,(96,776,986,851),27,"#0F2E3C","#0F2E3C")
    d.rectangle((97,828,985,851),fill="#0F2E3C")
    for i,c in enumerate(("#FF7887","#FFD36E","#60E6CA")):
        d.ellipse((129+38*i,800,147+38*i,818),fill=c)
    text(d,(300,795),"first_step.py",27,"#AAC4CD")
    centered(d,(105,858,977,1046),card.example,70 if len(card.example)<18 else 52)
    box(d,(108,1120,970,1360),30,"#0A3F48","#47BFB1")
    if stage==0:
        text(d,(157,1152),"STEP 01 / SAVE",31,"#65EBD1")
        centered(d,(136,1210,942,1324),"この1行を保存",66)
    elif stage==1:
        text(d,(157,1152),"STEP 02 / RUN",31,"#65EBD1")
        centered(d,(136,1210,942,1324),"実行してみる",66)
    else:
        text(d,(157,1152),"STEP 03 / RESULT",31,"#65EBD1")
        text(d,(366,1215),"結果",50,"#AAC4CD")
        text(d,(605,1144),card.result,150,"#FFC877")
    box(d,(58,1531,1022,1754),30,"#022937","#5EE9D6",4)
    text(d,(97,1551),"VOICE / JP",27,"#65EBD1")
    centered(d,(85,1604,994,1720),card.captions[0] if stage==0 else card.captions[1],79)
    box(d,(100,1726,979,1736),5,"#105B61","#105B61")
    box(d,(100,1726,100+int(879*(stage+1)/3),1736),5,"#65EBD1","#65EBD1")
    text(d,(64,1811),"機種のOS・接続手順を確認してください",26,"#AAC4CD")
    text(d,(64,1856),"HUMAN REVIEW / NOT FOR PUBLICATION",20,"#AAC4CD")
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);im.save(path)
    return path
if __name__=="__main__":
    root=Path(__file__).resolve().parent
    for stage in range(3):print(draw(SCIENCE,stage,root/"assets"/f"endcard_stage{stage}.png"))
