"""Reproducible 20s synthetic review MP4, with required offline Japanese TTS.
This is an independent reimplementation, NOT the original v33 engine.
"""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,math,subprocess,shutil,wave
from scene_motion import scenes,ROWS,totals,row_removal_progress,speech_timing
BASE=Path(__file__).parent
OUT=BASE/"output";OUT.mkdir(exist_ok=True)
W,H,FPS=540,960,30
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def f(size):return ImageFont.truetype(FONT,size)
def txt(d,x,y,s,sz=28,color="white"):d.text((x,y),s,font=f(sz),fill=color)
def rect(d,coords,color):d.rounded_rectangle(coords,radius=14,fill=color)
def frame(t):
 i=min(7,int(t/2.5));p=(t-i*2.5)/2.5
 im=Image.new("RGB",(W,H),"#09172d");d=ImageDraw.Draw(im)
 d.ellipse((-160,150,260,600),fill="#0b3154")
 txt(d,25,35,"AI時短ラボ | 架空データ",20,"#63d6ff")
 s=scenes()[i];txt(d,34,125,s.caption,32)
 if i in (1,2,4):
  rect(d,(30,280,510,690),"#edf5ff")
  rect(d,(30,280,510,344),"#1774bd")
  txt(d,55,294,"注文一覧 / TEST DATA",24)
  txt(d,56,350,"注文ID",21,"#143450");txt(d,322,350,"金額",21,"#143450")
  for j,(key,val) in enumerate(ROWS):
   y=392+j*63
   shrink=int(438*row_removal_progress(t)) if i==4 and j==2 else 0
   if shrink>400:continue
   rect(d,(46,y,488-shrink,y+56),"#fff0a5" if j==2 and i!=1 else "#d6e7fa")
   if shrink<30:
    txt(d,62,y+9,key,22,"#163750");txt(d,313,y+9,f"{val:,}円",22,"#163750")
  txt(d,56,648,"9,000円 → 6,000円" if i==4 else "4行 / 9,000円",22,"#143450")
 elif i==0 or i==7:
  rect(d,(140,310,400,550),"#d9f2ff")
  rect(d,(157,329,383,505),"#071b33")
  for x in (215,327):d.ellipse((x-21,390,x+21,432),fill="#14caff")
  txt(d,224,570,"AI",34,"#71e6ff")
 elif i==3:
  rect(d,(36,285,504,690),"#173e60")
  for j,v in enumerate(("1. 注文IDを照合","2. 金額と日時を確認","3. 本当に重複か確認")):txt(d,54,340+j*99,v,25)
 elif i==5:
  rect(d,(25,325,251,505),"#4b263d");rect(d,(288,325,515,505),"#12483f")
  txt(d,44,347,"修正前",26);txt(d,307,347,"修正後",26)
  txt(d,44,415,"9,000円",31);txt(d,307,415,"6,000円",31)
  txt(d,118,565,"差額 3,000円",36,"#ffe48a")
 else:
  for j,v in enumerate(("1  注文ID","2  重複行","3  再集計")):
   rect(d,(42,300+j*112,498,380+j*112),"#153b5e")
   txt(d,65,316+j*112,v,29)
 rect(d,(24,775,516,843),"#020c19")
 txt(d,37,790,s.caption,25)
 txt(d,30,890,"REVIEW ONLY / PUBLICATION NOT APPROVED",16,"#9eb5c5")
 d.rectangle((0,948,int(540*t/20),954),fill="#2ccaff")
 return im

def synth():
 exe=shutil.which("open_jtalk")
 dic=list(Path("/var/lib/mecab/dic").rglob("sys.dic")) if Path("/var/lib/mecab/dic").exists() else []
 voices=list(Path("/usr/share/hts-voice").rglob("*.htsvoice")) if Path("/usr/share/hts-voice").exists() else []
 if not exe or not dic or not voices:raise RuntimeError("Japanese TTS engine or voice missing; refusing BGM-only artifact")
 paths=[];dur=[]
 for s in scenes():
  dest=OUT/f"speech_{s.index:02}.wav"
  subprocess.run([exe,"-x",str(dic[0].parent),"-m",str(voices[0]),"-r","1.18","-ow",str(dest)],input=s.speech,text=True,check=True)
  with wave.open(str(dest),"rb") as w:dur.append(w.getnframes()/w.getframerate())
  paths.append(dest)
 timing=speech_timing(dur)
 (OUT/"speech_timings.json").write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding="utf8")
 return paths

def main():
 voice=synth()
 silent=OUT/"silent.mp4"
 p=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size","540x960","-framerate","30","-i","-","-vf","scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","ultrafast","-crf","21","-pix_fmt","yuv420p",str(silent)],stdin=subprocess.PIPE)
 try:
  for n in range(600):p.stdin.write(frame(n/30).tobytes())
 finally:p.stdin.close();ret=p.wait()
 if ret:raise RuntimeError("ffmpeg video failed")
 music=OUT/"music.wav"
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i","sine=frequency=140:sample_rate=32000:duration=20","-filter:a","volume=0.025",str(music)],check=True)
 inputs=["-i",str(silent),"-i",str(music)]
 for wav in voice:inputs.extend(["-i",str(wav)])
 filt=["[1:a]volume=0.2[bg]"]
 for i in range(8):filt.append(f"[{i+2}:a]adelay={i*2500}|{i*2500}[v{i}]")
 filt.append("[bg]"+ "".join(f"[v{i}]" for i in range(8))+"amix=inputs=9:duration=first:normalize=0[a]")
 dest=OUT/"cycle699_JA_REVIEW_ONLY.mp4"
 subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",*inputs,"-filter_complex",";".join(filt),"-map","0:v","-map","[a]","-c:v","copy","-c:a","aac","-t","20","-movflags","+faststart",str(dest)],check=True)
 print(dest)
if __name__=="__main__":main()
