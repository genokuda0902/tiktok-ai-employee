"""Standalone synthetic review-only 1080x1920 renderer. No external assets."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('改善対象：日本語音声','音声合成の接続に失敗','音声なしの動画は公開しません'),('字幕は音声に合わせる','文字表示だけでは同期未達成','音声取得後に区間を再調整'),('10ジャンル共通の検査','映像・音声・字幕・権利を確認','社員承認まで投稿禁止')]
def frame(i):
    im=Image.new('RGB',(1080,1920),(12,21,37)); d=ImageDraw.Draw(im)
    f1=ImageFont.truetype(BOLD,65);f2=ImageFont.truetype(FONT,43);f3=ImageFont.truetype(FONT,30)
    d.rounded_rectangle((70,210,1010,1620),radius=50,fill=(24,40,65))
    d.rectangle((70,210,84,1620),fill=(38,198,195))
    d.text((110,300),'品質改善 / REVIEW',font=f3,fill=(67,210,210))
    for j,line in enumerate(SCENES[i]):d.text((110,520+j*230),line,font=f1 if j==0 else f2,fill='white' if j==0 else (207,220,235))
    d.text((110,1540),f'{i+1} / 3',font=f3,fill=(210,210,220))
    d.text((90,1760),'PUBLICATION NOT APPROVED',font=f3,fill=(255,190,95))
    return im
def render():
    clips=[]
    for i in range(len(SCENES)):
        png=ROOT/f'scene{i}.png'; frame(i).save(png)
        mp4=ROOT/f'scene{i}.mp4'
        subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-loop','1','-framerate','24','-i',str(png),'-t','2','-vf','format=yuv420p','-an','-c:v','libx264','-preset','ultrafast','-crf','25',str(mp4)],check=True)
        clips.append(mp4)
    concat=ROOT/'concat.txt';concat.write_text(''.join("file '"+str(x)+"'\n" for x in clips))
    out=ROOT/'cycle1363_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error','-f','concat','-safe','0','-i',str(concat),'-c','copy','-movflags','+faststart',str(out)],check=True)
    return out
if __name__=='__main__':print(render())
