"""Review-only synthetic vertical video. No external assets or private data."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('毎月の集計、まだ手作業？','3秒で見直す表計算の基本'),('売上を入力する','架空データ：4月 120 / 5月 150'),('合計セルに入力','=SUM(B2:B3)'),('計算結果を確認','合計 270｜入力範囲を確認')]
def main():
    clips=[]
    for i,(head,body) in enumerate(SCENES):
        im=Image.new('RGB',(1080,1920),'#0b1224');d=ImageDraw.Draw(im)
        d.rounded_rectangle((70,240,1010,1550),radius=40,fill='#18263b')
        d.rounded_rectangle((110,550,970,1090),radius=18,fill='#f8fafc')
        d.rectangle((110,550,970,660),fill='#c9e6dc')
        f=ImageFont.truetype(FONT,58);small=ImageFont.truetype(FONT,40)
        d.text((110,330),head,font=f,fill='white');d.text((150,580),'月       売上',font=small,fill='#122d31')
        for j,line in enumerate(['4月        120','5月        150','合計       '+('270' if i==3 else '---')]):
            d.text((155,710+j*115),line,font=small,fill='#18263b')
        d.text((105,1220),body,font=small,fill='#e0f2fe')
        d.text((110,1630),'架空データ / REVIEW ONLY',font=small,fill='#fda4af')
        png=OUT/f'frame{i}.png';im.save(png)
        clip=OUT/f'clip{i}.mp4'
        subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-framerate','15','-i',str(png),'-t','2.5','-c:v','libx264','-pix_fmt','yuv420p','-vf','scale=1080:1920','-an',str(clip)],check=True)
        clips.append(clip)
    lst=OUT/'concat.txt';lst.write_text(''.join(f"file '{p}'\\n" for p in clips).replace('\\n','\n'))
    dest=OUT/'cycle1369_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-f','lavfi','-i','sine=frequency=440:sample_rate=44100:duration=10','-filter_complex','[1:a]volume=0.012,afade=t=out:st=9.4:d=0.6[a]','-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-shortest','-movflags','+faststart',str(dest)],check=True)
    return dest
if __name__=='__main__':print(main())
