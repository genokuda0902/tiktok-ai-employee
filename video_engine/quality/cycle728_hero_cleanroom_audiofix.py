"""Cycle728 clean-room cinematic hook renderer. Internal review only; never posts."""
import argparse, math, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS,FRAMES=1080,1920,30,96
GENRE_ACCENTS={
 'ai_work':'#6cf5e9','beauty':'#ffb9d4','love_psychology':'#ffb1de',
 'saving':'#a6e8b4','sales_business':'#ffd390','career':'#a4c7ff',
 'health':'#9de6d4','science':'#b2b6ff','travel_food':'#ffc09d',
 'product_comparison':'#c3d0ff'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SALES=(12,15,20,18)
SAFE=(55,1240,1025,1520)
def font(size):return ImageFont.truetype(FONT,size)
def hexrgb(v):return tuple(int(v[i:i+2],16) for i in (1,3,5))
def validate(genre):
 if genre not in GENRE_ACCENTS:raise ValueError('Unknown genre')
 if sum(SALES)!=65:raise ValueError('Proof mismatch')
 if not (0<=SAFE[0]<SAFE[2]<=W and 192<=SAFE[1]<SAFE[3]<=1536):raise ValueError('Unsafe captions')
 return True

def make_robot(accent):
 """Original shaded mascot: no logos or third-party images."""
 w,h=520,660
 im=Image.new('RGBA',(w,h),(0,0,0,0))
 glow=Image.new('RGBA',(w,h));g=ImageDraw.Draw(glow)
 g.ellipse((20,40,505,595),fill=(*hexrgb(accent),65))
 im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(58)))
 d=ImageDraw.Draw(im)
 d.ellipse((120,572,460,655),fill=(0,6,23,100))
 d.rounded_rectangle((109,364,425,626),radius=105,fill='#194566',outline='#72b7d5',width=8)
 d.rounded_rectangle((140,381,402,598),radius=82,fill='#d9f4ff',outline='#ffffff',width=8)
 d.rounded_rectangle((174,434,369,558),radius=40,fill='#96c6e6')
 d.rounded_rectangle((216,466,329,523),radius=22,fill='#103b5d')
 d.text((242,477),'AI',font=font(34),fill=accent)
 d.rounded_rectangle((58,83,466,418),radius=137,fill='#326d99',outline='#9be4ff',width=11)
 d.rounded_rectangle((72,88,453,397),radius=130,fill='#ecfbff',outline='#ffffff',width=8)
 d.rounded_rectangle((95,130,430,362),radius=94,fill='#0b203d',outline='#66badb',width=5)
 d.arc((91,96,443,392),190,310,fill='#ffffff',width=19)
 d.arc((91,96,443,392),25,90,fill='#b2f4ff',width=12)
 for x in (200,329):
  d.ellipse((x-46,207,x+46,299),fill='#194a65')
  d.ellipse((x-34,218,x+34,286),fill=accent)
  d.ellipse((x-21,225,x-3,244),fill='#ffffff')
 d.arc((208,236,324,326),13,166,fill=accent,width=13)
 d.line((258,80,258,45),fill='#d5f9ff',width=10)
 d.ellipse((239,24,279,64),fill=accent,outline='#ffffff',width=5)
 highlight=Image.new('RGBA',(w,h));hd=ImageDraw.Draw(highlight)
 hd.ellipse((113,96,250,139),fill=(255,255,255,90))
 hd.ellipse((170,391,356,421),fill=(255,255,255,68))
 im.alpha_composite(highlight.filter(ImageFilter.GaussianBlur(11)))
 return im

def background(accent):
 y=np.linspace(0,1,H,dtype=np.float32)[:,None]
 out=np.zeros((H,W,3),dtype=np.uint8)
 for k,(top,bottom) in enumerate([(3,12),(16,39),(35,71)]):
  out[:,:,k]=(top*(1-y)+bottom*y).astype('uint8')
 im=Image.fromarray(out,'RGB').convert('RGBA')
 gl=Image.new('RGBA',(W,H));g=ImageDraw.Draw(gl)
 r,gg,b=hexrgb(accent)
 g.ellipse((430,100,1270,930),fill=(r,gg,b,65))
 g.ellipse((-410,790,600,1810),fill=(24,107,212,45))
 im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(130)))
 d=ImageDraw.Draw(im)
 for i in range(28):
  xx=(i*137+33)%W;yy=160+(i*241)%910;rad=3+(i%4)*4
  d.ellipse((xx-rad,yy-rad,xx+rad,yy+rad),fill=(80,172,220,60))
 return im

def draw_frame(bg,robot,accent,idx):
 t=idx/FPS;im=bg.copy();d=ImageDraw.Draw(im)
 d.rounded_rectangle((66,156,630,231),radius=24,fill='#153c58',outline='#32698a',width=3)
 d.text((91,168),'AI時短ラボ   /   AI × EXCEL',font=font(36),fill=accent)
 d.text((66,283),'まだ手作業？',font=font(83),fill='white')
 d.text((67,401),'数字が一目でわかる',font=font(48),fill='#e5f5ff')
 im.alpha_composite(robot,(566,242+int(9*math.sin(t*3.4))))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((61,838,1018,1205),radius=44,fill='#071c34',outline=accent,width=5)
 d.text((98,873),'架空データ  /  4か月の売上',font=font(36),fill='#a5c7d9')
 d.text((95,948),'合計',font=font(49),fill='white')
 d.text((272,923),'65万円',font=font(106),fill=accent)
 progress=min(1,max(0,(t-.2)/1.8))
 for j,val in enumerate(SALES):
  x=132+j*218;bar_h=int(113*(val/20)*min(1,max(0,(progress*4-j)*1.2)))
  d.rounded_rectangle((x,1147-bar_h,x+122,1147),radius=13,fill=accent if j==2 else '#438fbe')
  d.text((x+30,1151),f'{j+1}月',font=font(29),fill='#e5f5ff')
 d.rounded_rectangle(SAFE,radius=32,fill='#061a30',outline=accent,width=5)
 d.rounded_rectangle((78,1273,92,1483),radius=7,fill=accent)
 d.text((126,1284),'Excelの集計、',font=font(64),fill='white')
 d.text((126,1385),'まだ手作業ですか？',font=font(64),fill=accent)
 d.text((72,1565),'※数値は架空・投稿には社員承認が必要',font=font(29),fill='#b1c9dc')
 d.rounded_rectangle((66,1630,66+int(860*(idx+1)/819),1642),radius=5,fill=accent)
 return im.convert('RGB')

def build(source,output,genre='ai_work'):
 validate(genre)
 source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
 if not source.is_file():raise FileNotFoundError(source)
 accent=GENRE_ACCENTS[genre];bg=background(accent);robot=make_robot(accent)
 intro=output.parent/'intro_96frames.mp4'
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
      '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast',
      '-crf','21','-pix_fmt','yuv420p',str(intro)]
 with subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE) as proc:
  for i in range(FRAMES):proc.stdin.write(draw_frame(bg,robot,accent,i).tobytes())
  proc.stdin.close();err=proc.stderr.read();ret=proc.wait()
  if ret:raise RuntimeError(err.decode(errors='replace')[-1000:])
 filt=f"[0:v][1:v]overlay=x=0:y=0:eof_action=pass:enable='lt(n,{FRAMES})',format=yuv420p[v]"
 silent=output.parent/'silent_cycle728.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(intro),
    '-filter_complex',filt,'-map','[v]','-an','-c:v','libx264','-preset','veryfast',
    '-crf','21','-frames:v','819',str(silent)],check=True,timeout=240)
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(source),
    '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)],check=True,timeout=120)
 silent.unlink(missing_ok=True)
 return output

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--genre',default='ai_work');a=p.parse_args();print(build(a.source,a.output,a.genre))
