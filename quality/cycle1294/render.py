from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('AIの回答、','そのまま使う？','まず確認する3つのこと'),('01  出典','情報源を確認','根拠のない断定に注意'),('02  日付','いつの情報？','古い情報を見落とさない'),('03  判断','最後は自分で確認','重要な決定は一次情報へ')]
def render():
    for i,(a,b,c) in enumerate(SCENES):
        im=Image.new('RGB',(1080,1920),(9,17,32));d=ImageDraw.Draw(im)
        d.rounded_rectangle((64,175,1016,1720),radius=48,fill=(20,34,56),outline=(54,91,123),width=3)
        d.rounded_rectangle((110,250,970,900),radius=36,fill=(25+i*8,69,91+i*9))
        for k in range(6):
            x=155+k*127
            d.rounded_rectangle((x,370+(k%2)*45,x+85,700-(k%3)*40),radius=25,fill=(34+k*9,132+k*8,159))
        d.text((112,100),'AI  /  QUALITY CHECK',font=ImageFont.truetype(REG,35),fill='#70DCE3')
        d.text((112,1010),a,font=ImageFont.truetype(FONT,91),fill='white')
        d.text((112,1160),b,font=ImageFont.truetype(FONT,67),fill='#B8F2F3')
        d.text((112,1335),c,font=ImageFont.truetype(REG,42),fill='#D0DDE9')
        d.rounded_rectangle((112,1580,968,1600),radius=10,fill='#3A5367')
        d.rounded_rectangle((112,1580,112+(i+1)*214,1600),radius=10,fill='#6DE4DA')
        d.text((112,1780),'REVIEW ONLY  /  音声未実装',font=ImageFont.truetype(REG,29),fill='#9FB2C4')
        im.save(P/f'scene{i}.png')
    with (P/'concat.txt').open('w') as f:
        for i in range(4): f.write(f"file 'scene{i}.png'\\nduration 3\\n".replace('\\n','\n'))
        f.write("file 'scene3.png'\n")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','24','-t','12','-movflags','+faststart',str(P/'cycle1294_REVIEW_ONLY.mp4')],check=True)
    (P/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\n{b}\n\n' for i,(_,b,_) in enumerate(SCENES)),encoding='utf-8')
if __name__=='__main__': render()
