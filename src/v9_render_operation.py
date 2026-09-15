#!/usr/bin/env python3
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import math
W,H=1080,1920; FPS=15; DUR=16; N=FPS*DUR
O=Path('output/v9_operation_frames');O.mkdir(parents=True,exist_ok=True)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def F(n): return ImageFont.truetype(font,n)
def rr(d,box,r,fill,outline=None,w=1): d.rounded_rectangle(box,r,fill,outline,width=w)
def txt(d,xy,s,n,fill='#111827'): d.text(xy,s,font=F(n),fill=fill)
rows=[('山田 太郎','090-0000-1111','yamada@example.jp','10/1 14:00'),('佐藤 花子','080-2222-3333','sato@example.jp','10/2 10:00'),('鈴木 健','070-4444-5555','suzuki@example.jp','10/3 16:00')]
prompt='以下の顧客情報から「氏名」「電話番号」「メールアドレス」「希望日時」を抽出して、表にしてください。'
for i in range(N):
 t=i/FPS; im=Image.new('RGB',(W,H),'#f4f6f8');d=ImageDraw.Draw(im)
 # app chrome
 d.rectangle((0,0,W,118),fill='#ffffff'); txt(d,(48,34),'AI時短ラボ｜操作デモ',35,'#0f172a'); d.ellipse((980,44,1010,74),fill='#22c55e')
 if t<12:
  txt(d,(55,165),'新しいチャット',25,'#64748b'); rr(d,(55,250,1025,735),28,'#ffffff','#dbe2ea',2)
  shown=prompt[:max(0,min(len(prompt),int((t-.2)*16)))] if t<3.6 else prompt
  # wrap
  lines=[shown[j:j+22] for j in range(0,len(shown),22)]
  for k,line in enumerate(lines): txt(d,(105,320+k*75),line,42,'#111827')
  rr(d,(790,625,965,700),22,'#2563eb');txt(d,(837,642),'送信',31,'white')
  # cursor motion and click pulse
  cx=int(160+(835-160)*min(1,max(0,(t-2.4)/1.1)));cy=int(530+(662-530)*min(1,max(0,(t-2.4)/1.1)))
  d.polygon([(cx,cy),(cx+20,cy+45),(cx+29,cy+27),(cx+49,cy+48),(cx+60,cy+37),(cx+39,cy+18)],fill='#0f172a')
  if 3.45<t<3.8:d.ellipse((cx-35,cy-35,cx+35,cy+35),outline='#38bdf8',width=7)
  if t>=4.0:
   txt(d,(70,820),'回答',28,'#64748b'); rr(d,(55,875,1025,1640),28,'#ffffff','#dbe2ea',2)
   if t<5.8: txt(d,(105,950),'整理しています…',40,'#64748b')
   else:
    y=960; headers=['氏名','電話番号','メール','希望日時']; xs=[95,290,555,830]
    d.rectangle((80,y-25,995,y+60),fill='#0f766e')
    for x,h in zip(xs,headers):txt(d,(x,y),h,25,'white')
    reveal=min(3,max(0,int((t-5.6)/1.0)))
    for r,row in enumerate(rows[:reveal]):
     yy=y+105+r*125; d.rectangle((80,yy-20,995,yy+80),fill='#f8fafc' if r%2==0 else '#eef2f7')
     vals=[row[0],row[1],row[2].split('@')[0]+'@…',row[3]]
     for x,v in zip(xs,vals):txt(d,(x,yy+5),v,23,'#0f172a')
    if t>=9.2:
     rr(d,(760,1450,970,1525),20,'#10a37f');txt(d,(810,1467),'コピー',29,'white')
     if 10.0<t<10.5:d.ellipse((850,1440,940,1530),outline='#67e8f9',width=8)
 else:
  # spreadsheet proof
  d.rectangle((0,118,W,210),fill='#107c41');txt(d,(42,143),'Excel風｜顧客一覧.xlsx',34,'white')
  txt(d,(45,250),'A1',24,'#64748b'); rr(d,(95,235,1025,300),8,'white','#cbd5e1',2);txt(d,(125,250),'氏名',26)
  left=45;top=350;cw=[190,265,300,225];rh=110
  heads=['氏名','電話番号','メール','希望日時']
  x=left
  for w,h in zip(cw,heads):d.rectangle((x,top,x+w,top+rh),fill='#d9ead3',outline='#94a3b8',width=2);txt(d,(x+18,top+32),h,25);x+=w
  visible=min(3,max(0,int((t-12)*2.3)))
  for r,row in enumerate(rows[:visible]):
   x=left; yy=top+(r+1)*rh
   vals=[row[0],row[1],row[2].split('@')[0]+'@…',row[3]]
   for w,v in zip(cw,vals):d.rectangle((x,yy,x+w,yy+rh),fill='white',outline='#cbd5e1',width=2);txt(d,(x+14,yy+34),v,22);x+=w
  if t>14.2:
   rr(d,(110,980,970,1160),35,'#07111f');txt(d,(190,1020),'バラバラ文章 → 表',58,'#67e8f9');txt(d,(270,1090),'一括で完成',48,'white')
 # progress + safe-zone title
 d.rectangle((0,1880,int(W*(i+1)/N),1892),fill='#22d3ee')
 im.save(O/f'{i:04d}.jpg',quality=90)
print(f'generated {N} v9 operation frames')
