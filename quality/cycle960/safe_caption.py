"""cycle960: conservative TikTok UI-safe Japanese subtitle renderer (review only).
Only the known SHA-locked AI-work MP4 can be rendered. The geometry is an
assumption pending phone playback, not a claim about TikTok's official UI.
"""
from pathlib import Path
import hashlib, subprocess
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA="37d9333effd1fd7702581be447c0820a9e44a7f5dedd1f19ce4fef4f316d51e9"
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
CUTS=(0,87,174,261,348,435,522,609,691)
SAFE_RIGHT,SAFE_BOTTOM=900,1640
ACCENTS={"ai_work":"#57E2D3","business":"#70B7FF","finance":"#F2D17A",
 "education":"#F5B96B","career":"#99C4FF","wellness":"#A7E1B0",
 "lifestyle":"#F0B4D1","technology":"#79D4E8","travel":"#FFCC8D","trivia":"#C8ACFF"}
SCENES=(
 ((("AIで仕事",1),("を早くするなら、",0)),(("最初の一歩が大事。",0),)),
 ((("まず、",0),("繰り返している作業を",1)),(("書き出す。",0),)),
 ((("次に、",0),("完成形の見本を",1)),(("用意する。",0),)),
 ((("指示は、",0),("目的と条件を",1)),(("具体的",1),("に伝える。",0))),
 ((("最初の出力は、",0),),(("必ず自分で",1),("確かめる。",0))),
 ((("違いがあれば、",0),("修正点を",1)),(("一つずつ",1),("伝える。",0))),
 ((("使える指示は、",0),),(("テンプレートに",1),("残す。",0))),
 ((("小さな時短を、",0),),(("毎日の習慣に",1),("しよう。",0))),
)
def sha256(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for chunk in iter(lambda:f.read(1048576),b""):h.update(chunk)
 return h.hexdigest()
def scene_at_frame(f):
 if not 0<=f<691:raise ValueError("frame out of range")
 return next(i for i in range(8) if CUTS[i]<=f<CUTS[i+1])
def panel_for_scene(scene,genre="ai_work"):
 if genre not in ACCENTS or not 0<=scene<8:raise ValueError("unsupported scene or genre")
 im=Image.new("RGBA",(1080,405),(0,0,0,0));d=ImageDraw.Draw(im)
 for y in range(405):
  d.line((0,y,1080,y),fill=(2,9,27,min(255,max(0,round((y-3)/92*255)))))
 d.rounded_rectangle((48,42,883,278),radius=25,fill=(4,13,32,255),outline=(68,112,142,255),width=3)
 d.rounded_rectangle((66,65,75,256),radius=4,fill=ACCENTS[genre])
 boxes=[]
 for n,line in enumerate(SCENES[scene]):
  for px in range(62,43,-1):
   font=ImageFont.truetype(FONT,px,index=0)
   width=sum(d.textlength(t,font=font) for t,_ in line)
   if width<=748:break
  else:raise ValueError("caption too wide")
  x=(48+883-width)/2;y=80 if n==0 else 164
  for t,em in line:
   w=d.textlength(t,font=font)
   d.text((x,y),t,font=font,fill="#FFE365" if em else "#F7FAFF",stroke_width=1,stroke_fill="#172137")
   boxes.append((x,1340+y,x+w,1340+y+px));x+=w
 assert all(78<=x0 and x1<=858 and y1<=SAFE_BOTTOM for x0,y0,x1,y1 in boxes)
 assert 883<=SAFE_RIGHT and 1340+278<=SAFE_BOTTOM
 return im,boxes
def render(source,output,genre="ai_work"):
 source=Path(source);output=Path(output)
 if genre!="ai_work" or sha256(source)!=SOURCE_SHA:raise PermissionError("unreviewed source or genre")
 output.parent.mkdir(parents=True,exist_ok=True)
 folder=output.parent/"overlay_frames";folder.mkdir(exist_ok=True)
 for i in range(8):panel_for_scene(i,genre)[0].save(folder/f"scene_{i+1:02}.png")
 for f in range(691):
  link=folder/f"overlay_{f+1:04}.png"
  if link.exists() or link.is_symlink():link.unlink()
  link.symlink_to(f"scene_{scene_at_frame(f)+1:02}.png")
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),
      "-framerate","30","-start_number","1","-i",str(folder/"overlay_%04d.png"),
      "-filter_complex","[0:v][1:v]overlay=x=0:y=1340:format=auto:shortest=1[v]",
      "-map","[v]","-map","0:a:0","-frames:v","691","-c:v","libx264",
      "-preset","veryfast","-crf","18","-pix_fmt","yuv420p","-c:a","copy",
      "-metadata:s:a:0","language=jpn","-movflags","+faststart",str(output)]
 subprocess.run(cmd,check=True,timeout=300)
 return {"source_sha":sha256(source),"output_sha":sha256(output),"approved":False}
