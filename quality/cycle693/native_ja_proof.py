#!/usr/bin/env python3
"""Review-only native Japanese TTS proof; fail closed, no external user media."""
import argparse,hashlib,json,shutil,subprocess,wave
from pathlib import Path
SCENES=[
("まだ手作業ですか？","その集計、まだ手作業ですか。"),
("数字を確認します","四か月の売上を確認します。"),
("正しい合計は650","正しい合計は、六百五十です。"),
("保存してあとで試す","保存して、あとで試してください。")]
VALUES=(120,150,200,180)
DIC=Path("/var/lib/mecab/dic/open-jtalk/naist-jdic")
VOICE=Path("/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice")
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def build(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True)
 if not shutil.which("open_jtalk") or not DIC.is_dir() or not VOICE.is_file():
  raise RuntimeError("FAIL_CLOSED: native Japanese Open JTalk unavailable")
 if sum(VALUES)!=650:raise RuntimeError("numeric proof invalid")
 inputs=[];filters=[];draw=[];times=[]
 for i,(caption,speech) in enumerate(SCENES):
  wav=out/f"ja{i}.wav"
  subprocess.run(["open_jtalk","-x",str(DIC),"-m",str(VOICE),"-r","1.5","-ow",str(wav)],input=speech.encode("utf-8"),check=True)
  with wave.open(str(wav),"rb") as w:
   duration=w.getnframes()/w.getframerate()
   if w.getnframes()<1000 or duration>4.6:raise RuntimeError(f"bad speech duration scene {i}: {duration:.3f}")
  st=i*5+.2;end=st+duration
  txt=out/f"caption{i}.txt";txt.write_text(caption,encoding="utf-8")
  inputs+=["-i",str(wav)]
  filters.append(f"[{i+1}:a]adelay={round(st*1000)}[v{i}]")
  draw.append("drawtext=fontfile="+FONT+":textfile="+str(txt)+":fontcolor=white:fontsize=64:x=(w-text_w)/2:y=1110:"+f"enable='between(t,{st:.3f},{max(st+1.5,end):.3f})'")
  times.append({"scene":i,"start":round(st,3),"end":round(end,3),"spoken":speech,"caption":caption})
 filters.append("".join(f"[v{i}]" for i in range(len(SCENES)))+f"amix=inputs={len(SCENES)}:duration=longest:normalize=0,apad=pad_dur=20[a]")
 title=out/"title.txt";title.write_text("AI時短ラボ｜日本語音声テスト",encoding="utf-8")
 vf=",".join(["drawtext=fontfile="+FONT+":textfile="+str(title)+":fontcolor=0x69dfdf:fontsize=68:x=(w-text_w)/2:y=480"]+draw)
 mp4=out/"cycle693_native_JA_REVIEW_ONLY.mp4"
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","lavfi","-i","color=c=0x07182c:s=1080x1920:r=30:d=20"]+inputs+["-filter_complex",";".join(filters),"-map","0:v:0","-map","[a]","-vf",vf,"-t","20","-c:v","libx264","-preset","veryfast","-pix_fmt","yuv420p","-c:a","aac","-b:a","160k","-movflags","+faststart",str(mp4)]
 subprocess.run(cmd,check=True)
 qa={"cycle":693,"native_ja":True,"segments":times,"sha256":hashlib.sha256(mp4.read_bytes()).hexdigest(),"values":VALUES,"sum":sum(VALUES),"public_approved":False,"visual_equivalent":False,"purpose":"audio/sync technical proof only"}
 (out/"qa.json").write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps(qa,ensure_ascii=False))
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--out",default="output");build(p.parse_args().out)
