"""Zero-cost, original image-first TikTok preview. Review only: no Japanese TTS.
Python 3.11+, Pillow, ffmpeg/ffprobe, Noto Sans CJK. No network or external assets.
"""
import argparse, hashlib, json, math, subprocess, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

SIZE=(1080,1920); FPS=30; DATA=[120,150,200,250]
SCENES=[
 ('hook','これ、まだ手で集計？','4か月の数字を、目で確認',2.5),
 ('pain','毎回、同じ集計作業','転記 → 計算 → グラフ作成',2.5),
 ('solution','AIで手順を整理','入力データと計算式は確認する',2.5),
 ('prompt','指示は具体的に','合計・月別グラフ・計算式を依頼',2.5),
 ('formula','SUM関数で検算','120 + 150 + 200 + 250',2.5),
 ('chart','同じ数値で可視化','合計 720 ／ 架空データ',2.5),
 ('compare','Before → After','手作業の整理 → 手順の標準化',2.5),
 ('cta','保存して試してみよう','数値の確認は最後まで忘れずに',2.5),
]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def f(sz,bold=False):
 p=Path(BOLD if bold else FONT)
 if not p.exists(): p=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
 return ImageFont.truetype(str(p),sz)

def txt(d,xy,s,sz=48,color='#f6fbff',bold=False):d.text(xy,s,font=f(sz,bold),fill=color,stroke_width=0)

def bg(i):
 w,h=SIZE; yy,xx=np.mgrid[0:h,0:w]
 a=np.empty((h,w,3),dtype=np.uint8)
 a[:,:,0]=(7+xx/w*12+yy/h*8).astype('uint8')
 a[:,:,1]=(19+xx/w*25+yy/h*12).astype('uint8')
 a[:,:,2]=(42+xx/w*34+yy/h*22).astype('uint8')
 im=Image.fromarray(a,'RGB')
 light=Image.new('RGBA',SIZE);d=ImageDraw.Draw(light)
 for j in range(9):
  x=90+((i*139+j*229)%1100);y=80+((j*331+i*97)%1400)
  rad=25+j*6;d.ellipse((x-rad,y-rad,x+rad,y+rad),fill=(25,167,250,20+j*3))
 light=light.filter(ImageFilter.GaussianBlur(65))
 im=Image.alpha_composite(im.convert('RGBA'),light).convert('RGB')
 d=ImageDraw.Draw(im)
 txt(d,(68,75),'AI時短ラボ  /  ORIGINAL DEMO',29,'#68dcff',True)
 txt(d,(810,77),f'{i+1:02d} / 08',30,'#b3d1e5',True)
 d.line((68,134,920,134),fill='#376a91',width=3)
 d.rounded_rectangle((70,1690,900,1698),radius=4,fill='#284e71')
 d.rounded_rectangle((70,1690,70+int(830*(i+1)/8),1698),radius=4,fill='#32e5d4')
 txt(d,(70,1730),'再現映像  /  架空データ  /  投稿未承認',28,'#b7c9dc')
 return im

def panel(d,box,fill='#122b45',stroke='#39739b',r=38):
 x0,y0,x1,y1=box
 d.rounded_rectangle((x0+10,y0+17,x1+10,y1+17),radius=r,fill='#061321')
 d.rounded_rectangle(box,radius=r,fill=fill,outline=stroke,width=4)

def orb(im,x=480,y=840,r=230):
 # An original abstract AI assistant sphere, not a copied mascot or logo.
 gl=Image.new('RGBA',SIZE);gd=ImageDraw.Draw(gl)
 for k in range(4,0,-1):
  rr=r+60*k;gd.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(29,163,255,8))
 im.paste(Image.alpha_composite(im.convert('RGBA'),gl.filter(ImageFilter.GaussianBlur(45))).convert('RGB'))
 d=ImageDraw.Draw(im)
 for rr in range(r,0,-1):
  q=rr/r;d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=(int(15+25*(1-q)),int(55+70*(1-q)),int(97+95*(1-q))))
 d.ellipse((x-r*.83,y-r*.77,x+r*.83,y+r*.67),fill='#071629',outline='#58d7ff',width=7)
 for ex in (-76,76):
  d.ellipse((x+ex-35,y-26,x+ex+35,y+35),fill='#51dfff')
  d.ellipse((x+ex-17,y-14,x+ex+17,y+18),fill='#e8ffff')
 d.arc((x-76,y-12,x+76,y+107),start=25,end=155,fill='#6cf4f5',width=8)
 d.arc((x-r*.65,y-r*.9,x+r*.25,y-r*.45),start=190,end=310,fill='#d2f9ff',width=13)

def draw_scene(i,out):
 key,title,cap,_=SCENES[i]
 im=bg(i);d=ImageDraw.Draw(im)
 txt(d,(72,210),title,65,'#ffffff',True)
 if key=='hook':
  orb(im,490,880,218);d=ImageDraw.Draw(im)
  panel(d,(85,1210,885,1470),'#102e48','#3da7d8')
  txt(d,(120,1260),'4か月の売上',45,'#d8f6ff',True)
  txt(d,(120,1335),'120 + 150 + 200 + 250',40,'#ffe283',True)
 elif key=='pain':
  panel(d,(95,480,875,1370),'#182c43','#537a9a')
  for j,(lab,desc) in enumerate([('01','データを転記'),('02','合計を計算'),('03','グラフを作成')]):
   y=555+j*255;d.rounded_rectangle((140,y,820,y+205),radius=28,fill='#2b4058')
   txt(d,(175,y+38),lab,75,'#f3aa88',True);txt(d,(310,y+65),desc,47,'#f7faff',True)
 elif key=='solution':
  orb(im,490,835,210);d=ImageDraw.Draw(im)
  panel(d,(105,1230,885,1480),'#123d4c','#37c9c2')
  txt(d,(143,1270),'入力 → 検算 → 結果',53,'#ddffef',True)
  txt(d,(145,1370),'AIは補助、確認は人間',36,'#c3e4f1')
 elif key=='prompt':
  panel(d,(80,470,905,1420),'#eaf4fa','#6bc7ec')
  d.rounded_rectangle((115,510,865,610),radius=25,fill='#12587e')
  txt(d,(145,530),'AIへの指示（再現）',44,'#ffffff',True)
  for j,line in enumerate(['この4か月の売上を','合計してください。','月別グラフと計算式も','あわせて示してください。']):
   txt(d,(138,705+j*116),line,47,'#163449',j==0)
  d.rounded_rectangle((610,1260,840,1360),radius=27,fill='#1379b4')
  txt(d,(665,1274),'送信',53,'#ffffff',True)
 elif key=='formula':
  panel(d,(82,480,895,1400),'#edf7fa','#6dc3df')
  txt(d,(122,545),'月別売上（架空）',47,'#134b63',True)
  for j,n in enumerate(DATA):
   y=660+j*115;d.rounded_rectangle((122,y,850,y+100),radius=17,fill='#d3eaf2' if j%2==0 else '#f7fdff')
   txt(d,(165,y+18),f'{j+1}月',43,'#14384e',True);txt(d,(655,y+18),str(n),47,'#14384e',True)
  d.rounded_rectangle((125,1155,850,1340),radius=24,fill='#0b695f')
  txt(d,(170,1193),'=SUM(B2:B5)  →  720',48,'#ffffff',True)
 elif key=='chart':
  panel(d,(85,475,895,1400),'#edf7fa','#78c7e2')
  txt(d,(128,535),'月別売上  /  単位なし',42,'#214a63',True)
  d.line((148,1180,840,1180),fill='#456f86',width=5)
  for j,n in enumerate(DATA):
   x=182+j*165;ht=int(n/250*455)
   d.rounded_rectangle((x,1180-ht,x+110,1180),radius=16,fill=['#30a5e2','#2ab4db','#20c3d2','#23cda9'][j])
   txt(d,(x+10,1132-ht),str(n),40,'#204d61',True);txt(d,(x+20,1210),f'{j+1}月',39,'#204d61',True)
  txt(d,(210,1325),'合計 720',57,'#0b776d',True)
 elif key=='compare':
  panel(d,(83,490,470,1390),'#452c42','#a7657b')
  panel(d,(505,490,895,1390),'#174c4b','#46bba4')
  txt(d,(123,550),'BEFORE',51,'#ffd2d5',True);txt(d,(530,550),'AFTER',51,'#bcffe4',True)
  for j,(a,b) in enumerate([('転記','条件整理'),('手計算','SUM検算'),('手で作図','数値照合')]):
   txt(d,(123,745+j*180),a,45,'#fff1f3',True)
   txt(d,(525,745+j*180),b,43,'#eafff4',True)
  txt(d,(107,1460),'※時短効果は測定していません',34,'#c4d7e6')
 elif key=='cta':
  orb(im,495,825,200);d=ImageDraw.Draw(im)
  panel(d,(112,1235,870,1490),'#0a5363','#50d4c6')
  txt(d,(165,1278),'① データ確認',46,'#ffffff',True)
  txt(d,(165,1363),'② 検算して保存',46,'#ffffff',True)
 txt(d,(76,1570),cap,38,'#d9eafa',True)
 im.save(out,optimize=True)

def make_sfx(path):
 sr=44100;n=sr*20;signal=np.zeros(n,dtype=np.float32)
 for i in range(len(SCENES)):
  start=int(i*2.5*sr);m=int(.13*sr);t=np.arange(m)/sr
  signal[start:start+m]+=(.11*np.sin(2*np.pi*(480+i*70)*t)*np.exp(-t*26)).astype(np.float32)
 with wave.open(str(path),'wb') as w:
  w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((signal*32767).astype('<i2').tobytes())

def run(args):
 out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 for i in range(8):draw_scene(i,out.parent/f'scene_{i+1:02}.png')
 wav=out.parent/'original_sfx.wav';make_sfx(wav)
 clips=[]
 for i in range(8):
  p=out.parent/f'clip_{i+1:02}.mp4';clips.append(p)
  # Native-resolution scene images; 1.5% slow camera push, constant 30fps.
  filt="zoompan=z='min(zoom+0.0002,1.015)':d=75:s=1080x1920:fps=30,format=yuv420p"
  cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-loop','1','-i',str(out.parent/f'scene_{i+1:02}.png'),'-vf',filt,'-frames:v','75','-an','-c:v','libx264','-preset','ultrafast','-crf','23','-pix_fmt','yuv420p',str(p)]
  subprocess.run(cmd,check=True)
 listing=out.parent/'clips.txt';listing.write_text(''.join("file '"+str(p.resolve())+"'\n" for p in clips))
 video=out.parent/'visual_only.mp4'
 subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(listing),'-c','copy',str(video)],check=True)
 subprocess.run(['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-y','-i',str(video),'-i',str(wav),'-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','96k','-t','20','-movflags','+faststart',str(out)],check=True)
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,nb_frames:format=duration','-of','json',str(out)]))
 full=subprocess.run(['ffmpeg','-nostdin','-v','error','-i',str(out),'-f','null','-'],capture_output=True,text=True)
 report={'cycle':495,'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'probe':probe,'full_decode':'PASS' if full.returncode==0 else 'FAIL','decode_error':full.stderr,'captions':'8 Japanese on-screen scene descriptions; not speech transcripts','native_japanese_voice':'NOT_GENERATED','audio':'ORIGINAL_SYNTHETIC_SFX_ONLY','rights':'ORIGINAL_PROCEDURAL','reference':'User storyboard inspected; reference MP4 raw bytes inaccessible','human_review':'PENDING','publication':'NOT_APPROVED','auto_post':False,'scenes':SCENES}
 (out.parent/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps({'sha256':report['sha256'],'full_decode':report['full_decode'],'probe':probe},ensure_ascii=False))
 if full.returncode:raise RuntimeError(full.stderr)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='cycle495_cinematic_imagefirst_SFX_ONLY_REVIEW.mp4');run(ap.parse_args())
