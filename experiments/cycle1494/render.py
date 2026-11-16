from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import subprocess
ROOT=Path(__file__).parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('AIへの指示、変えるだけ','目的を一文で伝える'),('悪い例','「資料を作って」だけ'),('良い例','「新人向けに3項目で」'),('最後に確認','数字と根拠は人が確認')]
def draw(i,headline,subtitle):
 im=Image.new('RGB',(720,1280),(11,20,38));d=ImageDraw.Draw(im)
 d.rounded_rectangle((44,140,676,1100),radius=35,fill=(23,39,63))
 d.rectangle((44,140,55,1100),fill=(54,202,218))
 d.text((72,190),'AI 仕事術 / REVIEW',font=ImageFont.truetype(BOLD,30),fill=(92,226,237))
 d.text((72,410),headline,font=ImageFont.truetype(BOLD,48),fill='white')
 d.rounded_rectangle((70,670,650,810),radius=20,fill=(43,62,89))
 d.text((88,700),subtitle,font=ImageFont.truetype(FONT,32),fill='white')
 d.rounded_rectangle((72,1040,648,1050),radius=5,fill=(60,82,109))
 # Captions are baked into the video and use the exact same scene timeline.
 d.rounded_rectangle((48,865,672,982),radius=16,fill=(4,12,25))
 d.text((70,891),subtitle,font=ImageFont.truetype(BOLD,31),fill=(255,255,255))
 d.rounded_rectangle((72,1040,72+int(576*(i+1)/4),1050),radius=5,fill=(54,202,218))
 d.text((75,1150),'REVIEW ONLY / 投稿未承認',font=ImageFont.truetype(FONT,25),fill=(178,192,209))
 im.save(ROOT/f'frame{i}.png')
def main():
 for i,(a,b) in enumerate(SCENES):draw(i,a,b)
 # No synthetic cue is represented as Japanese narration. Audio intentionally absent and QA fails closed.
 files=[]
 for i in range(len(SCENES)):
  p=ROOT/f's{i}.mp4';files.append(p)
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','24','-i',str(ROOT/f'frame{i}.png'),'-t','2','-c:v','libx264','-pix_fmt','yuv420p',str(p)],check=True)
 lst=ROOT/'concat.txt';lst.write_text(''.join("file '"+str(p)+"'\n" for p in files))
 out=ROOT/'cycle1494_REVIEW_ONLY.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(out)],check=True)
 (ROOT/'captions.srt').write_text(''.join(f'{i+1}\n00:00:{2*i:02d},000 --> 00:00:{2*i+2:02d},000\n{a}。{b}\n\n' for i,(a,b) in enumerate(SCENES)),encoding='utf-8')
 return out
if __name__=='__main__':print(main())
