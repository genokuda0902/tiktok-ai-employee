from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
scenes=[('Excelの集計、まだ手入力？','毎月の作業を30秒で見直す'),('BEFORE','売上  12000円\n売上  18000円\n売上  15000円\n合計  ?????'),('STEP 1','合計セルを選択'),('STEP 2','=SUM(B2:B4) を入力'),('AFTER','合計  45,000円\n※架空データの操作例')]
for i,(head,body) in enumerate(scenes):
 im=Image.new('RGB',(720,1280),'#0a1424');d=ImageDraw.Draw(im)
 d.rounded_rectangle((42,95,678,1160),radius=28,fill='#14263b',outline='#2b6076',width=3)
 d.rounded_rectangle((75,200,645,280),radius=12,fill='#147d7b')
 d.text((90,216),head,font=ImageFont.truetype(bold,37),fill='white')
 for j,line in enumerate(body.split('\n')):d.text((93,385+j*115),line,font=ImageFont.truetype(font,36),fill='#e8f4fa')
 d.text((93,1050),'REVIEW ONLY / 未承認',font=ImageFont.truetype(font,22),fill='#ffce82')
 d.rounded_rectangle((70,1190,70+(i+1)*116,1200),radius=5,fill='#2fd3b6')
 im.save(OUT/f'scene{i}.png')
with (OUT/'frames.txt').open('w') as f:
 for i in range(5):f.write(f"file 'scene{i}.png'\nduration 3\n")
 f.write("file 'scene4.png'\n")
subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'frames.txt'),'-vf','fps=30,scale=1080:1920:flags=lanczos,format=yuv420p','-c:v','libx264','-preset','ultrafast','-movflags','+faststart',str(OUT/'cycle1318_REVIEW_ONLY.mp4')],check=True)
