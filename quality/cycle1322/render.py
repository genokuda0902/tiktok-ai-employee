"""Review-only 1080x1920 image-first renderer; requires Pillow and ffmpeg."""
from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess
P=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('数字を見える化','毎日の集計を3秒で確認'),('BEFORE','手入力の集計はミスが起きやすい'),('操作','=SUM(B2:B5) を入力'),('AFTER','合計 128,000円を自動計算'),('確認が大切','AIや関数の結果は必ずチェック')]
def render():
 for i,(title,sub) in enumerate(SCENES):
  im=Image.new('RGB',(1080,1920),(9,17,34));d=ImageDraw.Draw(im)
  d.rounded_rectangle((70,310,1010,1530),radius=48,fill=(25,41,65));d.rectangle((70,310,86,1530),fill=(36,202,198))
  for y,t,size,color in [(460,title,78,'white'),(740,sub,42,(220,234,245)),(1370,'架空データ / REVIEW ONLY',30,(145,172,196))]:d.text((120,y),t,font=ImageFont.truetype(FONT,size),fill=color)
  im.save(P/f'scene{i}.png')
 cmd=['ffmpeg','-y']
 for i in range(5):cmd+=['-loop','1','-framerate','30','-t','3','-i',str(P/f'scene{i}.png')]
 filters=''.join(f"[{i}:v]scale=1080:1920,zoompan=z='min(zoom+0.00025,1.025)':d=90:s=1080x1920:fps=30,trim=duration=3,setpts=PTS-STARTPTS[v{i}];" for i in range(5))+''.join(f'[v{i}]' for i in range(5))+'concat=n=5:v=1:a=0[out]'
 subprocess.run(cmd+['-filter_complex',filters,'-map','[out]','-c:v','libx264','-preset','ultrafast','-crf','25','-pix_fmt','yuv420p','-movflags','+faststart',str(P/'cycle1322_REVIEW_ONLY.mp4')],check=True)
 (P/'captions.srt').write_text(''.join(f'{i+1}\\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\\n{t}。{s}\\n\\n' for i,(t,s) in enumerate(SCENES)),encoding='utf8')
if __name__=='__main__':render()
