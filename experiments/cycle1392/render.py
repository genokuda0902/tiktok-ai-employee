from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
OUT=Path(__file__).parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
scenes=[('毎月の集計、まだ手作業？','4件の売上を一瞬で合計'),('売上データを入力','2,400 / 3,100 / 2,900 / 4,000'),('合計セルに入力','=SUM(B2:B5)'),('Enterで計算完了','合計 12,400円'),('まずは4件で試そう','保存してあとで実践')]
W,H=720,1280; fps=24; duration=12
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(fps),'-i','-','-an','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'cycle1392_base.mp4')],stdin=subprocess.PIPE)
f1=ImageFont.truetype(BOLD,43);f2=ImageFont.truetype(FONT,28);f3=ImageFont.truetype(FONT,31)
for n in range(duration*fps):
 t=n/fps; i=min(4,int(t/(duration/5)))
 im=Image.new('RGB',(W,H),(8,17,36));d=ImageDraw.Draw(im)
 d.rounded_rectangle((36,90,684,1120),radius=30,fill=(21,35,59))
 d.rounded_rectangle((62,145,658,215),radius=15,fill=(34,63,92))
 d.text((85,158),'EXCEL  /  仕事の時短',font=f2,fill=(165,231,246))
 d.text((65,280),scenes[i][0],font=f1,fill='white')
 d.rounded_rectangle((65,405,655,870),radius=12,fill=(245,248,251))
 for row in range(7):d.line((75,460+row*58,645,460+row*58),fill=(203,215,224),width=2)
 d.line((330,460,330,808),fill=(203,215,224),width=2)
 for row,(a1,b1) in enumerate([('項目','売上'),('A','2,400'),('B','3,100'),('C','2,900'),('D','4,000'),('合計','12,400')]):
  y=420+row*58; d.text((90,y),a1,font=f2,fill=(23,46,61));d.text((355,y),b1 if i>=3 or row!=5 else '---',font=f2,fill=(14,90,76) if row==5 else (23,46,61))
 if i==2:d.rounded_rectangle((345,900,645,967),radius=8,fill=(11,96,83));d.text((360,910),'=SUM(B2:B5)',font=f3,fill='white')
 d.rounded_rectangle((60,1005,660,1090),radius=15,fill=(15,95,111))
 d.text((80,1024),scenes[i][1],font=f2,fill='white')
 d.rounded_rectangle((65,1155,655,1167),radius=6,fill=(65,82,105))
 d.rounded_rectangle((65,1155,65+int(590*t/duration),1167),radius=6,fill=(63,213,205))
 d.text((65,1200),'架空データ｜レビュー用｜音声未実装',font=ImageFont.truetype(FONT,20),fill=(187,200,218))
 p.stdin.write(im.tobytes())
p.stdin.close();assert p.wait()==0
(OUT/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{i*2.4:06.3f} --> 00:00:{(i+1)*2.4:06.3f}\n{x[0]}\n\n' for i,x in enumerate(scenes)),encoding='utf8')
