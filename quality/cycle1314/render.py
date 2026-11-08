"""Review-only synthetic spreadsheet demo; original reimplementation, not v33."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('集計、まだ手入力？','3秒でわかるSUM関数','BEFORE'),('売上データを選択','架空の表を使って説明','STEP 01'),('合計セルに入力','=SUM(B2:B5)','STEP 02'),('Enterで結果を表示','1200 + 800 + 1500 + 500','STEP 03'),('合計は 4,000','計算ミスを減らす基本操作','AFTER')]
def frame(i):
 im=Image.new('RGB',(1080,1920),'#0b1223'); d=ImageDraw.Draw(im)
 f=lambda n,b=False:ImageFont.truetype(BOLD if b else FONT,n)
 d.rounded_rectangle((55,135,1025,1770),radius=42,fill='#17243b')
 d.text((105,210),SCENES[i][2],font=f(42,True),fill='#48e0c5')
 d.text((105,325),SCENES[i][0],font=f(67,True),fill='white')
 d.text((105,445),SCENES[i][1],font=f(40),fill='#b5c8df')
 d.rounded_rectangle((100,620,980,1390),radius=28,fill='#f4f7fc')
 d.rectangle((100,620,980,730),fill='#167b67')
 d.text((145,645),'架空の売上表',font=f(42,True),fill='white')
 for j,(name,num) in enumerate([('商品A','1,200'),('商品B','800'),('商品C','1,500'),('商品D','500')]):
  y=770+j*110; d.text((160,y),name,font=f(43),fill='#152a44');d.text((660,y),num,font=f(43),fill='#152a44')
 d.rounded_rectangle((140,1250,940,1355),radius=12,fill='#d6eee9' if i>=3 else '#e3eaf4')
 d.text((170,1270),'合計  4,000' if i>=3 else ('=SUM(B2:B5)' if i==2 else '合計  ?'),font=f(45,True),fill='#154f45')
 d.text((105,1490),'実演イメージ｜架空データ',font=f(38),fill='#b5c8df')
 d.rounded_rectangle((105,1610,975,1626),radius=8,fill='#33425d')
 d.rounded_rectangle((105,1610,105+174*(i+1),1626),radius=8,fill='#48e0c5')
 p=OUT/f'scene{i}.png';im.save(p)
 return p
def run():
 clips=[]
 for i in range(len(SCENES)):
  p=frame(i);clip=OUT/f'clip{i}.mp4'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','30','-i',str(p),'-t','3','-vf','scale=1080:1920,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','26','-an',str(clip)],check=True)
  clips.append(clip)
 (OUT/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in clips))
 target=OUT/'cycle1314_REVIEW_ONLY.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy','-movflags','+faststart',str(target)],check=True)
 (OUT/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{i*3:02},000 --> 00:00:{(i+1)*3:02},000\n{s[0]}\n\n' for i,s in enumerate(SCENES)),encoding='utf-8')
 return target
if __name__=='__main__':print(run())
