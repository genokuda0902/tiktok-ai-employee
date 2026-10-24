"""Cycle822: first non-sales genre end-to-end (AI work), original diagrams,
offline Japanese voice, 24-state captions. Review only; no publishing.
"""
from pathlib import Path
import argparse, importlib.util, json, sys
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
def module(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

catalog=module("catalog822",ROOT/"cycle821/genre_catalog821.py")
art=module("art822",ROOT/"cycle820/make_art820.py")
rend=module("render822",ROOT/"cycle821/render821.py")
LINES=catalog.GENRES["ai_work"][2]
HEADS=[
 ("01 / THE HOOK","AIに頼む前に","最初の準備で、仕上がりが変わる"),
 ("02 / FIND","繰り返しを探す","毎日の作業を見つけよう"),
 ("03 / EXAMPLE","完成形を見せる","見本を用意して伝える"),
 ("04 / PROMPT","目的と条件を書く","指示を具体的にする"),
 ("05 / VERIFY","人の目で確認","出力は必ずチェック"),
 ("06 / REFINE","一つずつ直す","修正点を整理する"),
 ("07 / SAVE","使える指示を保存","次回も再利用できる"),
 ("08 / HABIT","小さな時短を積む","続けられる仕組みへ")]
def diagram(im,i,accent):
 d=art.shadow_box(im,(64,482,1016,1130),r=46)
 ink="#143449";muted="#678395"
 def label(x,y,s,size=41):
  art.center(d,(x,y),s,art.font(size),ink)
 if i==0:
  for j,s in enumerate(("資料","メール","表計算")):
   x=160+j*260;art.rect(d,(x,660,x+220,880),24,"#EDF6FA")
   label(x+110,730,s,38)
   for k in range(3):d.line((x+40,795+k*25,x+170,795+k*25),fill="#A9C7D7",width=7)
  label(540,1020,"まず、仕事を整理する",46)
 elif i==1:
  for j,s in enumerate(("毎日の集計","定型メール","議事録整理")):
   y=568+j*158;art.rect(d,(145,y,935,y+125),23,"#EDF6FA")
   art.rect(d,(170,y+29,235,y+95),15,accent)
   label(203,y+61,"✓",41);label(550,y+62,s,49)
 elif i==2:
  art.rect(d,(154,562,926,1042),30,"#F1F8FC")
  label(540,640,"完成イメージ",50)
  for j,w in enumerate((540,620,500,610)):
   y=734+j*68;art.rect(d,(240,y,240+w,y+32),10,accent if j==1 else "#B5CEDC")
  label(540,1058,"見本があると伝わる",39)
 elif i==3:
  for j,(key,val) in enumerate((("目的","何を作る？"),("条件","長さ・形式"),("見本","完成例"))):
   y=573+j*160;art.rect(d,(150,y,920,y+127),22,"#EDF6FA")
   art.rect(d,(175,y+30,315,y+96),14,accent)
   label(245,y+62,key,38);label(620,y+62,val,44)
 elif i==4:
  label(540,605,"AIの回答を確認",52)
  for j in range(5):d.line((230,705+j*66,770,705+j*66),fill="#B4CCDB",width=17)
  d.ellipse((680,817,905,1042),fill=accent)
  label(791,930,"✓",120)
 elif i==5:
  for j,(name,c) in enumerate((("初稿","#F9B3AB"),("修正","#FAD18E"),("完成",accent))):
   x=133+j*282;art.rect(d,(x,671,x+252,953),24,"#EEF6FA")
   art.rect(d,(x+18,698,x+234,779),16,c)
   label(x+126,738,name,42)
   for k in range(3):d.line((x+45,829+k*34,x+205,829+k*34),fill="#AAC4D3",width=8)
 elif i==6:
  art.rect(d,(227,565,855,1044),30,"#EDF6FA")
  art.rect(d,(267,616,815,732),22,accent)
  label(540,674,"保存した指示",50)
  for j in range(4):d.line((302,798+j*59,771,798+j*59),fill="#A9C4D4",width=14)
  label(540,1068,"次回も使える",38)
 else:
  d.ellipse((326,580,754,1008),fill="#EDF6FA",outline=accent,width=18)
  d.line((540,794,540,642),fill=ink,width=17)
  d.line((540,794,661,864),fill=ink,width=17)
  label(540,1070,"小さな時短を習慣に",40)

def prepare(root):
 catalog.validate()
 art.HEADS=HEADS
 art.SPEECH=LINES
 art.diagram=diagram
 art.create(root,"ai_work")
 font=ImageFont.truetype(art.FONT,31)
 for i in range(1,9):
  path=root/"source"/f"scene_{i:02}.png"
  im=Image.open(path).convert("RGB");d=ImageDraw.Draw(im)
  d.rounded_rectangle((64,72,405,132),radius=24,fill="#143449")
  d.text((235,102),"AI × WORK",font=font,fill="#FFFFFF",anchor="mm")
  d.rectangle((55,1760,1015,1860),fill="#0A2132")
  d.text((78,1810),"AIで作業を、もっとスマートに。",font=font,fill="#8CA7B0",anchor="lm")
  im.save(path,optimize=True)
 (root/"source"/"genre_proof822.json").write_text(json.dumps({
  "genre":"ai_work","script":LINES,"visuals":"original procedural AI-specific diagrams",
  "voice_generated_in_ci":True,"approval":False},ensure_ascii=False,indent=2))
 return root

def render(root):
 # The previous renderer has a hard-coded sales script; replace it in memory.
 # No source file is modified. Exact phrase/narration equality is still checked.
 rend.base.PHRASES=[]
 for s in LINES:
  n=len(s);a=max(1,round(n/3));b=max(a+1,round(2*n/3))
  rend.base.PHRASES.append([s[:a],s[a:b],s[b:]])
 out=root/"output"/"cycle822_AI_WORK_JAPANESE_HUMAN_REVIEW.mp4"
 return rend.render(root,out,"ai_work")

def verify(root):
 import subprocess,hashlib
 mp4=root/"output"/"cycle822_AI_WORK_JAPANESE_HUMAN_REVIEW.mp4"
 p=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(mp4)]))
 v=next(x for x in p["streams"] if x["codec_type"]=="video")
 a=next(x for x in p["streams"] if x["codec_type"]=="audio")
 ass=(root/"output"/"captions817.ass").read_text()
 checks={"1080x1920":(v["width"],v["height"])==(1080,1920),
 "h264_30fps":v["codec_name"]=="h264" and v["r_frame_rate"]=="30/1",
 "775_frames":int(v.get("nb_frames",0))==775,
 "aac_48khz":a["codec_name"]=="aac" and a["sample_rate"]=="48000",
 "japanese_voice_full":float(a.get("duration",p["format"]["duration"]))>25.7,
 "24_caption_states":len([x for x in ass.splitlines() if x.startswith("Dialogue: 0,")])==24,
 "three_line_subtitles":all(x.count(r"\N")==2 for x in ass.splitlines() if x.startswith("Dialogue: 0,")),
 "8_ai_images":len(list((root/"source").glob("scene_*.png")))==8,
 "genre_script_match":json.loads((root/"source"/"voice_timing.json").read_text())["sentences"][0]["text"]==LINES[0]}
 checks["full_video_decode"]=subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(mp4),"-map","0:v:0","-f","null","-"]).returncode==0
 data={"cycle":822,"genre":"ai_work","checks":checks,"passed":sum(checks.values()),"total":len(checks),"sha256":hashlib.sha256(mp4.read_bytes()).hexdigest(),"publication_approved":False,"note":"No word-level alignment, smartphone or subjective listening test"}
 (root/"output"/"qa822.json").write_text(json.dumps(data,ensure_ascii=False,indent=2))
 print(json.dumps(data,ensure_ascii=False,indent=2))
 if not all(checks.values()):sys.exit(1)

if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--root",type=Path,required=True)
 p.add_argument("--step",choices=["prepare","render","verify"],required=True)
 args=p.parse_args();args.root.mkdir(exist_ok=True,parents=True)
 {"prepare":prepare,"render":render,"verify":verify}[args.step](args.root)
