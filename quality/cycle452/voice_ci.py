#!/usr/bin/env python3
"""Free CI narration experiment; review-only, not the approved local master."""
import json, math, subprocess, pathlib, hashlib
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

R=pathlib.Path(__file__).resolve().parent
O=R/"ci_output"; O.mkdir(exist_ok=True)
D=[2,2.5,2.5,3,3,3,3,3]
C=["自己紹介、長すぎませんか？","経歴を全部話すと、伝わりません。","最初に結論を言いましょう。","順番は、結論、実績、貢献。","まず、何をしてきたか。","次に、具体的な経験。","最後に、どう役立てるか。","この順番で、30秒練習。"]
T=["その自己紹介、","NG｜全部話さない","OK｜順番を変える","この3つだけ","STEP 01｜結論","STEP 02｜実績","STEP 03｜貢献","面接前に30秒"]
EX=["長すぎるかも。","職歴を全部話す","課題整理から提案まで担当","結論 → 実績 → 貢献","何をしてきたか","具体的な経験","強みの活かし方","30秒で練習しよう"]
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def run(*x):
 p=subprocess.run(x,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-2000:])
 return p.stdout
def font(s):return ImageFont.truetype(FONT,s)
def image(i,text=None):
 im=Image.new("RGB",(1080,1920),"#F6F7F2");d=ImageDraw.Draw(im)
 d.text((65,78),"CAREER LAB  /  ORIGINAL GRAPHICS",font=font(29),fill="#17233A")
 d.line((65,150,1015,150),fill="#DDE2DA",width=3)
 d.text((65,235),T[i],font=font(68),fill="#17233A")
 d.rounded_rectangle((65,480,1015,1290),radius=46,fill="#FFFFFF")
 d.rounded_rectangle((110,555,240,680),radius=24,fill=["#C6F36E","#FC826C","#C6F36E","#8D72EF","#8D72EF","#FC826C","#4DB3A5","#C6F36E"][i])
 d.text((141,581),str(i+1).zfill(2),font=font(55),fill="#17233A")
 for n,line in enumerate(([text or EX[i]] if i!=3 else ["01  結論","02  実績","03  貢献"])):
  d.text((113,755+n*155),line,font=font(45 if len(line)>15 else 55),fill="#17233A")
 d.rounded_rectangle((55,1505,1025,1690),radius=30,fill="#17233A")
 d.text((88,1530),"JAPANESE CAPTION",font=font(26),fill="#C6F36E")
 d.text((88,1600),C[i],font=font(41),fill="#FFFFFF")
 for k in range(8):d.rounded_rectangle((60+k*122,1770,166+k*122,1785),radius=6,fill="#C6F36E" if k<=i else "#D8DDD5")
 d.text((60,1820),"HUMAN REVIEW ONLY  /  NOT APPROVED",font=font(24),fill="#697383")
 return im
items=[]
for i,dur in enumerate(D):
 if i==2:
  for k in range(5):
   s=EX[i][:math.ceil(len(EX[i])*(k+1)/5)]
   p=O/f"frame_{i}_{k}.png";image(i,s+"▍").save(p);items.append((p,dur/5))
 else:
  p=O/f"frame_{i}.png";image(i).save(p);items.append((p,dur))
lst=O/"concat.txt"
lst.write_text("".join(f"file '{p.resolve()}'\\nduration {t}\\n" for p,t in items)+f"file '{items[-1][0].resolve()}'\\n")
# Unescape only the file-list separators generated above.
lst.write_text(lst.read_text().replace("\\n","\n"))
silent=O/"silent.mp4"
run("ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(lst),"-vf","fps=30,format=yuv420p","-t","22","-c:v","libx264","-preset","veryfast","-crf","20",str(silent))
voices=[]
for i,(caption,dur) in enumerate(zip(C,D)):
 mp3=O/f"ja_{i}.mp3";gTTS(text=caption,lang="ja",slow=False).save(str(mp3))
 sec=float(json.loads(run("ffprobe","-v","error","-show_entries","format=duration","-of","json",str(mp3)))["format"]["duration"])
 speed=max(1,sec/(dur-.25))
 if speed>1.8:raise RuntimeError(f"VOICE_TOO_LONG scene={i}, speed={speed:.2f}")
 wav=O/f"ja_{i}.wav"
 run("ffmpeg","-y","-v","error","-i",str(mp3),"-af",f"atempo={speed:.4f},apad,atrim=0:{dur}", "-ar","48000","-ac","1",str(wav))
 voices.append(wav)
alist=O/"voices.txt";alist.write_text("".join(f"file '{v.resolve()}'\n" for v in voices))
audio=O/"voice.wav"
run("ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(alist),"-t","22","-ar","48000",str(audio))
out=O/"cycle452_CI_JAPANESE_VOICE_REVIEW_ONLY.mp4"
run("ffmpeg","-y","-v","error","-i",str(silent),"-i",str(audio),"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","160k","-t","22","-movflags","+faststart",str(out))
run("ffmpeg","-v","error","-i",str(out),"-f","null","-")
p=json.loads(run("ffprobe","-v","error","-show_entries","stream=codec_name,codec_type,width,height,nb_frames:format=duration","-of","json",str(out)))
v=next(s for s in p["streams"] if s["codec_type"]=="video")
assert (v["width"],v["height"],int(v["nb_frames"]))==(1080,1920,660)
assert any(s["codec_type"]=="audio" and s["codec_name"]=="aac" for s in p["streams"])
(O/"qa.json").write_text(json.dumps({"cycle":452,"voice":"gTTS Japanese speech generated; scene-level sync only, not word-level verified","approval":"NOT_APPROVED","cost_jpy":0,"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"probe":p},ensure_ascii=False,indent=2))
print("PASS",out)
