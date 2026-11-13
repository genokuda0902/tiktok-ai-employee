"""Cycle1428: original-assets-only review renderer. Requires Pillow, ffmpeg."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json, math, wave, struct
ROOT=Path(__file__).resolve().parent
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[
 ("合計、まだ電卓で計算？","B2 1,200 / B3 3,400 / B4 2,100"),
 ("実際の数式を確認","=SUM(B2:B4) → 6,700"),
 ("数字を必ず確認","1,200 + 3,400 + 2,100 = 6,700"),
]
def render():
 font=ImageFont.truetype(FONT,52)
 for i,(title,detail) in enumerate(SCENES):
  im=Image.new("RGB",(1080,1920),(9,20,38)); d=ImageDraw.Draw(im)
  d.rounded_rectangle((65,210,1015,1490),radius=30,fill=(23,44,68))
  d.text((100,330),title,font=font,fill="white")
  d.rounded_rectangle((90,750,990,1270),radius=20,fill=(244,248,252))
  d.text((110,900),detail,font=font,fill=(19,45,66))
  d.text((100,1550),"REVIEW ONLY / 公開未承認",font=font,fill="white")
  im.save(ROOT/f"scene{i}.png")
 (ROOT/"frames.txt").write_text("".join(f"file 'scene{i}.png'\nduration 5\n" for i in range(3))+"file 'scene2.png'\n")
 with wave.open(str(ROOT/"cue.wav"),"wb") as f:
  f.setnchannels(1);f.setsampwidth(2);f.setframerate(24000)
  for n in range(15*24000):
   t=n/24000; p=t%5; envelope=max(0,1-p/0.22) if p<0.22 else 0
   f.writeframesraw(struct.pack("<h",int(1800*envelope*math.sin(2*math.pi*660*t))))
 subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(ROOT/"frames.txt"),"-i",str(ROOT/"cue.wav"),"-vf","fps=25,format=yuv420p","-c:v","libx264","-c:a","aac","-t","15","-movflags","+faststart",str(ROOT/"cycle1428_REVIEW_ONLY.mp4")],check=True)
 (ROOT/"captions.srt").write_text("1\n00:00:00,000 --> 00:00:05,000\n合計、まだ電卓で計算？\n\n2\n00:00:05,000 --> 00:00:10,000\n=SUM(B2:B4) → 6,700\n\n3\n00:00:10,000 --> 00:00:15,000\n数字を必ず確認\n",encoding="utf-8")
 (ROOT/"qa.json").write_text(json.dumps({"japanese_narration":False,"audio":"synthesized cue only","speech_synced_captions":False,"publication_approved":False,"quality_status":"PUBLICATION_NOT_APPROVED"},ensure_ascii=False,indent=2))
if __name__=="__main__":render()
