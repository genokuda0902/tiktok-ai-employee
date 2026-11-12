"""Reproducible, non-publishable, synthetic Excel explainer. Requires Pillow, FFmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
scenes=[('その合計、間違ってない？','Excelの確認を10秒で整理'),('STEP 1｜数字を入力','3,200円 + 4,100円 + 5,100円'),('STEP 2｜計算を確認','=SUM(B2:B4)'),('RESULT｜12,400円','目視と計算結果を照合'),('保存してあとで試そう','架空データを使用したデモ')]
assert sum([3200,4100,5100])==12400
for i,(head,sub) in enumerate(scenes):
 im=Image.new('RGB',(1080,1920),(9,17,34));d=ImageDraw.Draw(im)
 d.rounded_rectangle((65,240,1015,1580),radius=48,fill=(22,38,61))
 d.rounded_rectangle((90,280,990,380),radius=22,fill=(20,115,132))
 d.text((120,294),'AI WORKFLOW / 01',font=ImageFont.truetype(BOLD,40),fill='white')
 d.text((105,485),head,font=ImageFont.truetype(BOLD,53),fill='white')
 d.text((105,680),sub,font=ImageFont.truetype(FONT,37),fill=(205,225,238))
 for j,v in enumerate(['A列    項目           B列   金額','01      商品A          ¥3,200','02      商品B          ¥4,100','03      商品C          ¥5,100','合計                       ¥12,400']):
  y=870+j*100;d.rounded_rectangle((105,y,975,y+86),radius=14,fill=(36,57,82) if j!=4 else (18,104,114));d.text((132,y+20),v,font=ImageFont.truetype(FONT,32),fill='white')
 d.rounded_rectangle((80,1690,1000,1820),radius=25,fill=(3,7,17));d.text((110,1720),sub,font=ImageFont.truetype(FONT,35),fill='white')
 im.save(OUT/f'frame{i}.png')
with (OUT/'concat.txt').open('w') as f:
 for i in range(len(scenes)): f.write(f"file 'frame{i}.png'\nduration 2\n")
 f.write("file 'frame4.png'\n")
subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-t','10','-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','25','-movflags','+faststart',str(OUT/'cycle1401_REVIEW_ONLY.mp4')],check=True)
(OUT/'manifest.json').write_text(json.dumps({'publication_approved':False,'japanese_narration':False,'speech_synced_captions':False,'asset_origin':'original generated graphics, synthetic data','duration_seconds':10},ensure_ascii=False,indent=2))
