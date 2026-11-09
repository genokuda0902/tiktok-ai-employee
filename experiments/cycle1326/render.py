"""Review-only 1080x1920 Japanese Excel demo. Requires Pillow and ffmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('Excel集計、まだ手作業？','3ステップで合計を自動化'),('① 合計したい列を確認','架空の売上データで実演'),('② SUM関数を入力','=SUM(B2:B5)'),('③ Enterで結果を表示','12,000 + 8,000 + 6,000 + 4,000'),('合計 30,000円','元データを確認してから利用')]
def render():
    for i,(headline,detail) in enumerate(SCENES):
        im=Image.new('RGB',(1080,1920),(10,19,37)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((55,150,1025,1740),radius=38,fill=(22,38,60),outline=(50,110,140),width=4)
        d.rectangle((75,170,92,1720),fill=(25,190,206))
        d.text((145,270),f'AI仕事術 / {i+1:02d} / 05',font=ImageFont.truetype(REG,42),fill=(82,222,225))
        d.text((145,420),headline,font=ImageFont.truetype(FONT,56),fill='white')
        d.rounded_rectangle((145,650,935,1230),radius=24,fill=(241,247,250))
        for r,line in enumerate(['項目       売上','A商品    12,000','B商品      8,000','C商品      6,000','D商品      4,000']):
            d.text((205,700+r*92),line,font=ImageFont.truetype(REG,44),fill=(23,48,65))
        d.text((145,1350),detail,font=ImageFont.truetype(REG,43),fill=(229,241,248))
        d.text((145,1600),'架空データ｜レビュー専用・未承認',font=ImageFont.truetype(REG,29),fill=(172,187,199))
        im.save(OUT/f'scene{i}.png')
    with (OUT/'concat.txt').open('w') as f:
        for i in range(len(SCENES)): f.write(f"file 'scene{i}.png'\nduration 3\n")
        f.write("file 'scene4.png'\n")
    subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','23','-t','15','-movflags','+faststart',str(OUT/'cycle1326_REVIEW_ONLY.mp4')],check=True)
if __name__=='__main__': render()
