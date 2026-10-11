"""Synthetic vertical chat slides; 3 reveal phases per scene."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'storyboard.json').read_text())
SCENES=DATA['scenes']
def font(size,bold=False):
    name='NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'
    return ImageFont.truetype('/usr/share/fonts/opentype/noto/'+name,size)
def slide(i,phase=2):
    title,sub,customer,reply,caption=SCENES[i]
    im=Image.new('RGB',(1080,1920),'#0B2133')
    d=ImageDraw.Draw(im)
    def rr(box,fill,r=24,outline=None):
        d.rounded_rectangle(box,radius=r,fill=fill,outline=outline,width=4)
    def tx(pos,s,sz=38,color='#FFFFFF'):
        d.text(pos,s,font=font(sz,True),fill=color)
    d.ellipse((690,-260,1480,510),fill='#133F4B')
    rr((60,65,1018,162),'#17354A')
    tx((91,87),'AI時短ラボ / SALES LAB',35)
    tx((825,95),f'{i+1:02d} / 06',30,'#65E7C7')
    for j in range(6):
        rr((70+j*155,180,203+j*155,192),'#4DE0B7' if j<=i else '#355263',6)
    tx((76,260),'SALES / CONVERSATION',30,'#5CE5C5')
    tx((70,350),title,70)
    tx((70,461),sub,70)
    rr((70,652,907,1380),'#17394C',35)
    tx((103,690),'CONVERSATION FLOW',32,'#B5E2E4')
    rr((108,795,866,994),'#F6EEE7')
    rr((131,814,257,866),'#DF8B64',15)
    tx((150,824),'お客様',26)
    tx((139,899),customer,42,'#152D40')
    rr((108,1023,866,1224),'#E8F7F3' if phase else '#294D5F')
    if phase:
        rr((131,1041,257,1094),'#1DAA8E',15)
        tx((149,1051),'担当者',26)
        tx((138,1129),reply,40,'#152D40')
    else:tx((144,1113),'次の会話を考える…',38,'#B5C9D4')
    if phase==2:rr((102,1017,872,1230),None,34,'#58E3C3')
    rr((108,1270,868,1342),'#285D52')
    tx((139,1287),'質問 → 理解 → 提案',34,'#E7FFF6')
    rr((75,1438,901,1604),'#E9F4F0')
    tx((107,1462),'JAPANESE CAPTION',25,'#167963')
    tx((103,1515),caption,35,'#163346')
    tx((78,1658),'架空の会話・社員確認前・投稿未承認',24,'#B5C8D3')
    return im
