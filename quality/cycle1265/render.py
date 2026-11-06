"""Review-only 1080p three-scene renderer. No audio or publication approval."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('AIの回答、\nそのまま使ってない？','まずは3秒で確認','01 / CHECK'),('事実と推測を\n分けて読む','根拠がない数字は使わない','02 / VERIFY'),('最後は自分で\n判断する','情報を確かめてから共有','03 / DECIDE')]
def render():
    OUT.mkdir(parents=True,exist_ok=True)
    for i,(head,sub,step) in enumerate(SCENES):
        im=Image.new('RGB',(1080,1920),(12,19,35)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((66,210,1014,1710),radius=50,fill=(24,36,59))
        d.rounded_rectangle((100,260,980,282),radius=10,fill=(48,207,189))
        d.text((116,360),step,font=ImageFont.truetype(BOLD,50),fill=(72,227,206))
        d.multiline_text((116,650),head,font=ImageFont.truetype(BOLD,80),fill='white',spacing=35)
        d.rounded_rectangle((105,1190,975,1410),radius=26,fill=(36,57,83))
        d.text((136,1245),sub,font=ImageFont.truetype(FONT,43),fill='white')
        d.text((116,1590),'REVIEW ONLY  /  NOT APPROVED',font=ImageFont.truetype(FONT,27),fill=(170,183,202))
        im.save(OUT/f'scene{i}.png')
    inputs=[]
    for i in range(3): inputs+=['-loop','1','-framerate','12','-t','5','-i',str(OUT/f'scene{i}.png')]
    filt=''.join(f'[{i}:v]fps=12,format=yuv420p,setsar=1[v{i}];' for i in range(3))+''.join(f'[v{i}]' for i in range(3))+'concat=n=3:v=1:a=0[out]'
    subprocess.run(['ffmpeg','-y','-loglevel','error',*inputs,'-filter_complex',filt,'-map','[out]','-c:v','libx264','-preset','ultrafast','-crf','24','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'cycle1265_REVIEW_ONLY.mp4')],check=True)
    (OUT/'captions.srt').write_text('1\n00:00:00,000 --> 00:00:05,000\nAIの回答、そのまま使ってない？\n\n2\n00:00:05,000 --> 00:00:10,000\n事実と推測を分けて読む\n\n3\n00:00:10,000 --> 00:00:15,000\n最後は自分で判断する\n',encoding='utf-8')
if __name__=='__main__': render()
