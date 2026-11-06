"""Cycle1253 reproducible synthetic visual storyboard. Review-only; no narration."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('まだ手作業で集計？','毎日の集計、時間がかかっていませんか','BEFORE','120 + 180 = ?'),('式をひとつ入力','SUM関数で数字を自動集計','ACTION','=SUM(B2:B3)'),('結果がすぐ見える','120 + 180 = 300','AFTER','合計 300')]
def render():
 for i,(title,sub,tag,proof) in enumerate(SCENES):
  im=Image.new('RGB',(1080,1920),'#0a1224'); d=ImageDraw.Draw(im)
  d.rounded_rectangle((62,210,1018,1540),radius=48,fill='#15243b',outline='#2c4965',width=3)
  d.rounded_rectangle((110,340,970,490),radius=24,fill='#245b72')
  d.text((138,365),tag,font=ImageFont.truetype(BOLD,55),fill='white')
  d.text((108,570),title,font=ImageFont.truetype(BOLD,65),fill='#ffffff')
  d.text((110,730),sub,font=ImageFont.truetype(FONT,39),fill='#c9d6e5')
  d.rounded_rectangle((115,910,965,1220),radius=26,fill='#edf4fa')
  d.text((160,1000),proof,font=ImageFont.truetype(BOLD,62),fill='#142b42')
  d.text((110,1630),'架空データによる操作イメージ',font=ImageFont.truetype(FONT,35),fill='#b5c6d8')
  d.text((110,1730),'REVIEW ONLY  |  投稿未承認',font=ImageFont.truetype(BOLD,36),fill='#ffc0a4')
  im.save(OUT/f'scene{i}.png')
 with (OUT/'concat.txt').open('w') as f:
  for i in range(3): f.write(f"file '{OUT}/scene{i}.png'\\nduration 4\\n".replace('\\n','\n'))
  f.write(f"file '{OUT}/scene2.png'\n")
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-vf','fps=30,format=yuv420p','-t','12','-c:v','libx264','-preset','ultrafast','-crf','25','-movflags','+faststart',str(OUT/'cycle1253_REVIEW_ONLY.mp4')],check=True)
if __name__=='__main__': render()
