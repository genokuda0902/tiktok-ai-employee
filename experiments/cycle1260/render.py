from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('その作業、毎日15分？','AIに任せる前に、まず手順を整理','BEFORE'),('入力を3つに絞る','目的・条件・出力形式を伝える','ACTION'),('最後は人が確認','AIの回答を検証して完成','AFTER')]
def render():
    clips=[]
    for i,(heading,body,tag) in enumerate(SCENES):
        im=Image.new('RGB',(720,1280),(9,18,35)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((40,170,680,1090),radius=38,fill=(22,37,62))
        d.rectangle((40,170,52,1090),fill=(60,213,200))
        d.text((76,235),tag,font=ImageFont.truetype(BOLD,38),fill=(74,225,207))
        d.text((75,420),heading,font=ImageFont.truetype(BOLD,44),fill='white')
        d.text((75,610),body,font=ImageFont.truetype(FONT,28),fill=(215,225,240))
        d.rounded_rectangle((75,825,645,915),radius=20,fill=(35,64,90))
        d.text((100,842),f'STEP 0{i+1} / 03',font=ImageFont.truetype(BOLD,35),fill='white')
        d.text((76,1160),'DEMO  /  HUMAN REVIEW ONLY',font=ImageFont.truetype(FONT,22),fill=(170,184,199))
        png=ROOT/f'scene{i}.png'; im.save(png)
        clip=ROOT/f'clip{i}.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','25','-i',str(png),'-t','5','-vf',"zoompan=z='min(zoom+0.0006,1.06)':d=1:s=720x1280:fps=25,format=yuv420p",'-c:v','libx264','-preset','ultrafast','-crf','27',str(clip)],check=True)
        clips.append(clip)
    (ROOT/'concat.txt').write_text(''.join(f"file '{p}'\n" for p in clips))
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(ROOT/'concat.txt'),'-c','copy','-movflags','+faststart',str(ROOT/'cycle1260_REVIEW_ONLY.mp4')],check=True)
if __name__=='__main__':render()
