"""Synthetic, review-only Japanese vertical video; no audio means never publish."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('AIの回答、\nそのまま使う？','まず「出典」を確かめる'),('STEP 01','出典は本当に存在する？'),('STEP 02','情報の日付は新しい？'),('STEP 03','最後は人が判断する')]
def render():
    OUT.mkdir(parents=True,exist_ok=True)
    clips=[]
    for i,(head,sub) in enumerate(SCENES):
        im=Image.new('RGB',(1080,1920),(9,17,34));d=ImageDraw.Draw(im)
        d.rounded_rectangle((66,260,1014,1580),radius=48,fill=(22,36,61),outline=(58,104,145),width=3)
        d.rounded_rectangle((100,310,980,325),radius=7,fill=(47,209,191))
        d.text((110,425),head,font=ImageFont.truetype(BOLD,85),fill='white',spacing=20)
        d.text((110,780),sub,font=ImageFont.truetype(FONT,48),fill=(190,235,237))
        d.text((110,1390),f'{i+1:02d} / 04   •   REVIEW ONLY',font=ImageFont.truetype(FONT,34),fill=(159,174,192))
        png=OUT/f'scene{i}.png';im.save(png)
        mp4=OUT/f'scene{i}.mp4'
        subprocess.run(['ffmpeg','-loglevel','error','-y','-loop','1','-framerate','15','-i',str(png),'-t','3','-vf','format=yuv420p','-c:v','libx264','-preset','ultrafast',str(mp4)],check=True)
        clips.append(mp4)
    (OUT/'captions.srt').write_text('\n\n'.join(f'{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{s}\n' for i,(_,s) in enumerate(SCENES)),encoding='utf8')
    (OUT/'concat.txt').write_text('\n'.join("file '"+str(p)+"'" for p in clips))
    target=OUT/'cycle1292_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-loglevel','error','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-c','copy','-movflags','+faststart',str(target)],check=True)
    return target
if __name__=='__main__':
    print('REVIEW_ONLY; audio absent; not publication approved:',render())
