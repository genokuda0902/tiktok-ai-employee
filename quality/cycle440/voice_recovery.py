"""Cycle440 free Japanese voice recovery; never publishes."""
from pathlib import Path
import json, subprocess
from gtts import gTTS
ROOT=Path(__file__).resolve().parent
SCENES=[
 (1.5,""),
 (2.5,"毎月の支払い。"),
 (2.8,"一年で、一万千七百六十円。"),
 (2.7,"使っていますか。"),
 (2.7,"明細を見よう。"),
 (2.8,"使っているか確認。"),
 (2.5,"解約条件を確認。"),
 (2.5,"まずは一つ見直そう。"),
]
def run(args):
 p=subprocess.run(args,text=True,capture_output=True)
 if p.returncode:raise RuntimeError(p.stderr[-1500:])
 return p.stdout
def main():
 assert sum(round(t*30) for t,_ in SCENES)==600
 out=ROOT/"ci_voice";out.mkdir(exist_ok=True)
 wavs=[]
 for i,(slot,line) in enumerate(SCENES):
  wav=out/f"{i:02d}.wav"
  if not line:
   run(["ffmpeg","-y","-v","error","-f","lavfi","-i","anullsrc=r=44100:cl=mono","-t",str(slot),str(wav)])
  else:
   mp3=out/f"{i:02d}.mp3"
   gTTS(line,lang="ja",slow=False).save(str(mp3))
   dur=float(json.loads(run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(mp3)]))["format"]["duration"])
   speed=max(1.0,dur/(slot-0.12))
   if speed>1.5:raise RuntimeError(f"Scene {i} exceeds slot: {dur:.2f}s / {slot:.2f}s")
   run(["ffmpeg","-y","-v","error","-i",str(mp3),"-af",f"atempo={speed:.4f},apad","-ar","44100","-ac","1","-t",str(slot),str(wav)])
  wavs.append(wav)
 playlist=out/"segments.txt"
 playlist.write_text("".join(f"file '{w}'\n" for w in wavs))
 merged=ROOT/"cycle440_ja_voice.wav"
 run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(playlist),"-c:a","pcm_s16le",str(merged)])
 dur=float(json.loads(run(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(merged)]))["format"]["duration"])
 if abs(dur-20)>0.15:raise RuntimeError(f"Audio duration mismatch {dur}")
 report={"cycle":440,"audio_seconds":dur,"language_requested":"ja","approval":"HUMAN_REVIEW","publication":"NOT_APPROVED","voice_file":merged.name,"note":"Japanese listening and subtitle sync remain unverified"}
 (ROOT/"cycle440_voice_qa.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps(report,ensure_ascii=False))
if __name__=="__main__":main()
