"""Cycle720: review-only, original image-first Excel video with Kokoro Japanese speech.
This is an independent reimplementation, not the v33 source. Numbers are fictional.
"""
from pathlib import Path
import json, math, subprocess, shutil, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0,str(Path(__file__).parent))
import cycle719_tts as tts

OUT=Path("output/cycle720")
FPS=30
SALES=(12,15,20,18)
GENRES=("ai_work","beauty","love_psychology","saving","sales_business","career","health","science","travel_food","product_comparison")
SCENES=[
("手作業、まだ続ける？","Excelの集計、まだ手作業ですか？","before"),
("4か月の売上データ","まず、架空の四か月データを用意。","table"),
("AIにグラフ化を依頼","この表をAIに渡して、グラフを依頼。","prompt"),
("数字を見える化","AIが表を読み、グラフを表示。","chart"),
("1月12万 / 2月15万","一月十二万円、二月十五万円。","chart"),
("3月20万 / 4月18万","三月二十万円、四月十八万円。","chart"),
("合計65万円を検算","合計は六十五万円。最後は人が確認。","proof"),
("あとで試せるように保存","保存して、あとで試してみて。","end")]
def validate():
 assert len(GENRES)==10 and len(SCENES)==8
 assert sum(SALES)==65 and SALES.index(max(SALES))==2
 assert all(len(s)==3 for s in SCENES)
 return True
def font(size):
 p="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
 return ImageFont.truetype(p,size)
def write(d,x,y,s,size=24,color="#ffffff"):
 d.text((x,y),s,font=font(size),fill=color)
def card(i,path):
 im=Image.new("RGB",(540,960),"#081728");d=ImageDraw.Draw(im)
 d.ellipse((-180,-180,300,340),fill="#113452")
 d.ellipse((330,650,820,1200),fill="#102e49")
 d.rounded_rectangle((24,27,515,91),radius=20,fill="#133a50")
 write(d,39,45,"AI時短ラボ  |  EXCEL × AI",19,"#8bece6")
 write(d,33,141,SCENES[i][0],31)
 d.rounded_rectangle((26,243,515,711),radius=23,fill="#eff6ff")
 kind=SCENES[i][2]
 if kind in ("table","prompt"):
  d.rounded_rectangle((45,266,494,322),radius=12,fill="#2675b5")
  write(d,61,281,"架空データ / SAMPLE",20)
  for k,v in enumerate(SALES):
   y=339+k*64
   d.rounded_rectangle((48,y,492,y+56),radius=9,fill="#dcebf8" if k%2==0 else "#ffffff")
   write(d,67,y+13,f"{k+1}月",21,"#12354d")
   write(d,351,y+13,f"{v}万円",21,"#12354d")
  if kind=="prompt":
   d.rounded_rectangle((55,609,487,693),radius=12,fill="#0b304c")
   write(d,65,623,"AI: 売上をグラフにして",20,"#9dffe8")
   write(d,65,659,"※ AIの結果は人が確認",16,"#fff4c7")
 elif kind in ("chart","proof"):
  write(d,52,270,"売上推移（架空の例）",22,"#12354d")
  for k,v in enumerate(SALES):
   x=69+k*107;y=611-int(v/20*242)
   d.rounded_rectangle((x,y,x+60,612),radius=8,fill="#06a99f" if k==2 else "#2a78bc")
   write(d,x+4,y-35,str(v),21,"#17384e")
   write(d,x+4,625,f"{k+1}月",19,"#17384e")
  if kind=="proof":
   d.rounded_rectangle((47,664,492,701),radius=10,fill="#173b57")
   write(d,62,669,"12+15+20+18=65万円",20)
 elif kind=="before":
  d.rounded_rectangle((49,274,493,459),radius=19,fill="#fbe5d8")
  write(d,72,302,"BEFORE",34,"#b34944")
  write(d,72,379,"手入力・集計・修正",23,"#253c51")
  d.rounded_rectangle((49,485,493,686),radius=19,fill="#d3f3ec")
  write(d,72,518,"AFTER",34,"#087f79")
  write(d,72,589,"AIでグラフの下書き",23,"#253c51")
 else:
  d.rounded_rectangle((52,294,489,653),radius=22,fill="#d4f3eb")
  write(d,81,337,"SAVE THIS",38,"#07847f")
  for k,s in enumerate(("① データを用意","② AIで下書き","③ 人が最終確認")):
   write(d,79,439+k*64,s,23,"#163e4f")
 # Caption below artwork, left of TikTok's right-side controls.
 d.rounded_rectangle((25,752,476,865),radius=17,fill="#153349")
 caption=SCENES[i][1]
 write(d,41,769,caption[:16],23)
 if len(caption)>16:write(d,41,807,caption[16:],23)
 write(d,29,900,"※ 数値は架空。公開には社員承認が必要。",15,"#c3d5e3")
 d.rounded_rectangle((27,928,27+int(480*(i+1)/8),935),radius=3,fill="#65e6da")
 im.save(path)
def cmd(args):
 subprocess.run([str(x) for x in args],check=True)
def stamp(sec):
 ms=round(sec*1000)
 return f"{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}"
def main():
 validate();OUT.mkdir(parents=True,exist_ok=True)
 for exe in ("ffmpeg","ffprobe"):
  if not shutil.which(exe):raise RuntimeError(exe+" missing")
 tts.LINES=[x[1] for x in SCENES]
 voices=tts.generate(out=str(OUT/"voices"),voice="jf_alpha",speed=1.15)
 assert len(voices)==8
 clips=[];srt=[];start=0.0
 for i,voice in enumerate(voices):
  seconds=float(voice["duration_s"])
  frames=max(90,math.ceil((seconds+0.4)*FPS))
  duration=frames/FPS
  img=OUT/f"scene_{i+1:02}.png";card(i,img)
  wav=OUT/"voices"/voice["file"]
  mp4=OUT/f"segment_{i+1:02}.mp4"
  cmd(["ffmpeg","-hide_banner","-loglevel","error","-y",
       "-loop","1","-framerate","30","-t",duration,"-i",img,"-i",wav,
       "-filter_complex",f"[0:v]scale=1080:1920:flags=lanczos,zoompan=z='min(zoom+0.00018,1.04)':d=1:s=1080x1920:fps=30,format=yuv420p[v];[1:a]apad,atrim=duration={duration},asetpts=PTS-STARTPTS[a]",
       "-map","[v]","-map","[a]","-frames:v",frames,
       "-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p",
       "-c:a","aac","-b:a","128k",mp4])
  clips.append(mp4)
  srt.append(f"{i+1}\n{stamp(start)} --> {stamp(start+duration)}\n{SCENES[i][1]}\n")
  voice["start_s"]=round(start,3);voice["scene_duration_s"]=round(duration,3)
  start+=duration
 (OUT/"captions.srt").write_text("\n".join(srt),encoding="utf-8")
 (OUT/"concat.txt").write_text("".join(f"file '{p.name}'\n" for p in clips),encoding="utf-8")
 target=OUT/"cycle720_NARRATED_REVIEW_ONLY.mp4"
 cmd(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","concat","-safe","0","-i",OUT/"concat.txt","-c","copy","-movflags","+faststart",target])
 report={"video":str(target),"genre":"ai_work","fictional_data":True,
         "narration":"Japanese Kokoro jf_alpha; scene-level captions",
         "segments":voices,"expected_duration_s":round(start,3),
         "status":"HUMAN_REVIEW / PUBLICATION_NOT_APPROVED",
         "assets":"self-drawn cards; Kokoro voice rights require human verification"}
 (OUT/"report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"video":str(target),"seconds":round(start,3),"segments":len(voices)}))
if __name__=="__main__":main()
