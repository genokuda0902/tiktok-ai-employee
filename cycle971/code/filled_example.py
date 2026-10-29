"""Review-only 1080x1920 Japanese weekly-report example (cycle971).
Inherited narration and burned subtitles are not re-authored.
Ten palettes are configured; only AI-work layout is reviewed.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H=1080,1920
SAFE=(100,345,985,1270)
START,END=5.82,8.67
COLORS={
 "ai_work":"#13B9B3","business":"#4A83D7","finance":"#BB8B42",
 "education":"#D08040","career":"#687DD7","wellness":"#3A9D76",
 "lifestyle":"#BE71A6","technology":"#148EAE","travel":"#B77D42",
 "trivia":"#9465C9"}
ROWS=[
 ("今週の成果","問い合わせ対応の流れを整理"),
 ("気づき","説明が長くなりがちだった"),
 ("次の行動","冒頭の案内を短く伝える")]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

def label(draw,xy,s,size,color,bold=False,maxwidth=700):
 f=ImageFont.truetype(BOLD if bold else FONT,size)
 bb=draw.textbbox((0,0),s,font=f)
 if bb[2]-bb[0]>maxwidth: raise ValueError("Japanese text overflow")
 draw.text(xy,s,font=f,fill=color)

def overlay(active=1,genre="ai_work"):
 if genre not in COLORS: raise ValueError("Unknown genre")
 if genre!="ai_work": raise PermissionError("Unreviewed genre: fail closed")
 if active not in (0,1,2): raise ValueError("Invalid row")
 im=Image.new("RGBA",(W,H),(0,0,0,0))
 sh=Image.new("RGBA",(W,H),(0,0,0,0))
 ImageDraw.Draw(sh).rounded_rectangle((137,384,943,1219),radius=36,fill=(0,0,0,125))
 im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(14)))
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((128,370,935,1204),radius=32,fill="#F9FAF6",outline="#D8E3DF",width=3)
 d.rounded_rectangle((161,403,492,450),radius=13,fill="#E6F4F2")
 label(d,(180,408),"架空の記入例 / SAMPLE",24,"#176C70",True,300)
 label(d,(162,474),"週次報告",78,"#172C34",True,620)
 label(d,(167,581),"成果 → 気づき → 次の行動",30,"#60757B")
 d.line((166,646,896,646),fill="#CFDAD7",width=3)
 for i,(heading,detail) in enumerate(ROWS):
  top=672+i*158; selected=i==active
  d.rounded_rectangle((163,top,898,top+139),radius=22,
   fill="#E5F8F6" if selected else "#FFFFFF",
   outline=COLORS[genre] if selected else "#D7E1DE",width=5 if selected else 2)
  d.rounded_rectangle((185,top+21,246,top+82),radius=15,
   fill=COLORS[genre] if selected else "#E8EDEC")
  label(d,(204,top+23),str(i+1),36,"#FFFFFF" if selected else "#6E7E80",True,35)
  label(d,(266,top+11),heading,41,"#142A31",True,600)
  label(d,(267,top+78),detail,31,"#455D61",False,615)
 label(d,(163,1160),"※実績ではありません・個人情報なし",24,"#687B7E",False,680)
 x0,y0,x1,y1=im.getchannel("A").getbbox()
 a,b,c,e=SAFE
 if not(a<=x0 and b<=y0 and x1<=c and y1<=e):
  raise RuntimeError("Overlay outside safe area")
 return im

def probe(path):
 p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)],
  capture_output=True,check=True,text=True)
 return json.loads(p.stdout)

def validate(info,synthetic=False):
 v=next((s for s in info["streams"] if s["codec_type"]=="video"),None)
 a=next((s for s in info["streams"] if s["codec_type"]=="audio"),None)
 if not v or (v["codec_name"],v["width"],v["height"],v["r_frame_rate"])!=("h264",W,H,"30/1"):
  raise ValueError("Requires H264 1080x1920 30fps")
 if not a or a["codec_name"]!="aac" or int(a["sample_rate"])!=48000:
  raise ValueError("Requires AAC 48kHz")
 if not synthetic and not 22.9<=float(info["format"]["duration"])<=23.1:
  raise ValueError("Unexpected duration")

def render(source,dest,genre="ai_work",synthetic=False):
 if genre!="ai_work": raise PermissionError("Unreviewed genre")
 validate(probe(source),synthetic)
 dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
 img=dest.parent/"filled_example_overlay.png"
 overlay(1,genre).crop(SAFE).save(img)
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
  "-loop","1","-framerate","30","-i",str(img),
  "-filter_complex",f"[0:v][1:v]overlay=x={SAFE[0]}:y={SAFE[1]}:format=auto:enable='gte(t,{START})*lt(t,{END})'[v]",
  "-map","[v]","-map","0:a:0","-c:v","libx264","-preset","ultrafast",
  "-crf","18","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(dest)]
 subprocess.run(cmd,check=True,timeout=900)
 subprocess.run(["ffmpeg","-v","error","-i",str(dest),"-f","null","-"],check=True,timeout=900)
 validate(probe(dest),synthetic)

if __name__=="__main__":
 ap=argparse.ArgumentParser()
 ap.add_argument("source");ap.add_argument("output")
 ap.add_argument("--genre",default="ai_work");ap.add_argument("--synthetic",action="store_true")
 a=ap.parse_args()
 render(a.source,a.output,a.genre,a.synthetic)
