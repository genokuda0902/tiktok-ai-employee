"""Review-only reproducible 1080x1920 caption-card video. No narration; never approve for posting."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('AIで仕事を時短','最初に目的を一行で伝える'),('条件を整理する','対象・期限・出力形式を指定'),('回答を確認する','数字と固有名詞は必ず検証'),('小さく試す','まず5分の作業から改善')]
W,H=1080,1920
def make_frame(i,title,sub):
 im=Image.new('RGB',(W,H),(9,19,37));d=ImageDraw.Draw(im)
 d.rounded_rectangle((65,240,1015,1600),radius=52,fill=(22,39,66))
 d.rounded_rectangle((90,270,990,293),radius=10,fill=(64,203,200))
 big=ImageFont.truetype(FONT,68);small=ImageFont.truetype(FONT,43)
 d.text((125,520),title,font=big,fill='white')
 d.text((125,820),sub,font=small,fill=(207,229,235))
 d.text((125,1300),f'{i+1:02d} / {len(SCENES):02d}',font=small,fill=(64,203,200))
 p=ROOT/f'frame_{i}.png';im.save(p);return p
def render():
 clips=[]
 for i,(title,sub) in enumerate(SCENES):
  p=make_frame(i,title,sub);out=ROOT/f'clip_{i}.mp4'
  subprocess.run(['ffmpeg','-v','error','-y','-loop','1','-framerate','24','-i',str(p),'-t','2.5','-vf','format=yuv420p','-c:v','libx264','-preset','ultrafast',str(out)],check=True)
  clips.append(out)
 playlist=ROOT/'concat.txt';playlist.write_text(''.join(f"file '{p}'\n" for p in clips))
 out=ROOT/'cycle1507_REVIEW_ONLY.mp4'
 subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(playlist),'-f','lavfi','-i','anullsrc=channel_layout=mono:sample_rate=48000','-shortest','-c:v','copy','-c:a','aac','-movflags','+faststart',str(out)],check=True)
 return out
if __name__=='__main__':print(render())
