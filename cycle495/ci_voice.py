"""CI-only native Japanese voice proof for cycle495. No publication or external user data."""
import json, math, subprocess, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS
import numpy as np
import soundfile as sf
R=Path("output/cycle495");R.mkdir(parents=True,exist_ok=True)
F="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FPS=30;W=1080;H=1920;SR=48000
GENRES=["AI・仕事効率化","営業","ビジネス","心理","キャリア","美容","お金","科学","旅行","比較"]
SCENES=[
("仕事が多い日、何から始める？","忙しさだけで","優先順位を決めない","仕事が多い日、何から始めますか。",-1),
("重要 × 緊急","期限が迫る重要事項は","先に着手する","重要で緊急な仕事は、まず着手。",0),
("重要 × 緊急でない","研修や仕組みづくりに","予定を確保する","重要だけど緊急でない仕事は、予定を確保。",1),
("緊急 × 重要でない","定型業務は","仕組みに任せる","緊急でも重要でない仕事は、委任や効率化。",2),
("緊急でも重要でもない","目的のない作業を","見直す","どちらでもない仕事は、減らしましょう。",3),
("忙しさではなく重要度で選ぶ","今日の最優先を","1つだけ決めよう","今日の最優先を、一つだけ決めましょう。",-1)]
def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-900:])
 return p.stdout
def stamp(t):
 n=round(t*1000);return f"{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}"
def txt(d,xy,s,size=44,color="#ffffff"):
 d.text(xy,s,font=ImageFont.truetype(F,size),fill=color)
def slide(i,beat):
 s=SCENES[i];im=Image.new("RGB",(W,H),"#0b1425");d=ImageDraw.Draw(im)
 d.rounded_rectangle((80,170,900,255),radius=25,fill="#1c3442")
 txt(d,(105,185),"AI時短ラボ / PRIORITY",33,"#74e8d6")
 txt(d,(790,187),f"{i+1:02}/06",26,"#d3dbe7")
 txt(d,(82,380),s[0],61 if len(s[0])<17 else 48)
 txt(d,(84,530),"重要度  ×  緊急度",40,"#b6c5d6")
 boxes=[(85,730,472,975),(488,730,875,975),(85,991,472,1236),(488,991,875,1236)]
 labels=[("重要・緊急","すぐ着手"),("重要・非緊急","予定に入れる"),("非重要・緊急","委任・効率化"),("非重要・非緊急","減らす")]
 colors=["#66edda","#c4ed87","#ff9877","#aab1cc"]
 for j,b in enumerate(boxes):
  active=s[4]==j
  d.rounded_rectangle(b,radius=24,fill="#294654" if active else "#1e3146",outline=colors[j] if active else "#52647b",width=5 if active else 2)
  txt(d,(b[0]+22,b[1]+68),labels[j][0],31)
  txt(d,(b[0]+22,b[1]+140),labels[j][1],35,colors[j])
  if active and beat==1:d.rounded_rectangle((b[0]+25,b[3]-24,b[2]-25,b[3]-12),radius=5,fill=colors[j])
 d.rounded_rectangle((78,1390,904,1585),radius=32,fill="#f4f9f6")
 txt(d,(114,1450),s[1+beat],46,"#0b1425")
 d.rounded_rectangle((81,1620,895,1634),radius=6,fill="#304759")
 d.rounded_rectangle((81,1620,81+round(814*(i*2+beat+1)/12),1634),radius=6,fill="#66edda")
 txt(d,(84,1682),"例示 / 社員の品質承認後に手動投稿",26,"#c5d3de")
 p=R/f"slide_{i*2+beat:02}.png";im.save(p);return p
def main():
 audios=[];times=[]
 for i,s in enumerate(SCENES):
  mp=R/f"ja_{i:02}.mp3";gTTS(s[3],lang="ja",timeout=30).save(str(mp))
  wa=R/f"ja_{i:02}.wav"
  run(["ffmpeg","-v","error","-y","-i",str(mp),"-ar","48000","-ac","1",str(wa)])
  a,sr=sf.read(wa,dtype="float32");assert sr==SR and np.sqrt(np.mean(a*a))>.001
  frames=max(96,math.ceil(((len(a)/SR)+.55)*FPS/2)*2)
  audios.append(a);times.append(frames)
 duration=sum(times)/FPS;mix=np.zeros(round(duration*SR),dtype=np.float32)
 rows=[];concat=R/"slides.txt";lines=[];off=0
 for i,(s,frames,a) in enumerate(zip(SCENES,times,audios)):
  for beat in range(2):
   p=slide(i,beat)
   lines.extend([f"file '{p.resolve()}'",f"duration {frames/FPS/2:.6f}"])
   start=off+beat*frames//2;end=off+(beat+1)*frames//2
   rows.append(f"{len(rows)+1}\n{stamp(start/FPS)} --> {stamp(end/FPS)}\n{s[beat+1]}\n")
  begin=round((off/FPS+.12)*SR);end=begin+len(a)
  assert end<=round((off/FPS+frames/FPS-.15)*SR)
  mix[begin:end]+=.80*a;off+=frames
 lines.append(f"file '{(R/'slide_11.png').resolve()}'")
 concat.write_text("\n".join(lines)+"\n")
 (R/"captions.srt").write_text("\n".join(rows),encoding="utf-8")
 sf.write(R/"japanese_voice.wav",np.clip(mix,-.95,.95),SR)
 vid=R/"silent.mp4";out=R/"cycle495_NATIVE_JA_HUMAN_REVIEW_NOT_APPROVED.mp4"
 run(["ffmpeg","-v","error","-y","-safe","0","-f","concat","-i",str(concat),"-vf","fps=30,format=yuv420p","-frames:v",str(sum(times)),"-c:v","libx264","-preset","veryfast","-crf","20",str(vid)])
 run(["ffmpeg","-v","error","-y","-i",str(vid),"-i",str(R/"japanese_voice.wav"),"-c:v","copy","-c:a","aac","-b:a","160k","-movflags","+faststart",str(out)])
 probe=json.loads(run(["ffprobe","-v","error","-show_entries","stream=codec_type,codec_name,width,height:format=duration","-of","json",str(out)]))
 v=next(s for s in probe["streams"] if s["codec_type"]=="video")
 assert (v["width"],v["height"])==(1080,1920)
 assert int(run(["ffprobe","-v","error","-count_frames","-select_streams","v:0","-show_entries","stream=nb_read_frames","-of","default=nokey=1:noprint_wrappers=1",str(out)]))==sum(times)
 run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"])
 qa={"cycle":495,"native_japanese_audio":"GENERATED_NOT_HUMAN_LISTENED","captions":12,"frames":sum(times),"duration":float(probe["format"]["duration"]),"resolution":[1080,1920],"publication":"NOT_APPROVED","rights":"ORIGINAL_GRAPHICS","sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
 (R/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 print(json.dumps(qa,ensure_ascii=False))
if __name__=="__main__":main()
