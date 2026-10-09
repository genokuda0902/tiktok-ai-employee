"""Cycle441 independent, zero-cost GitHub Actions Japanese-voice candidate.
Requires network for gTTS; no automatic posting. Human listening still required.
"""
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
from gtts import gTTS

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"output"
OUT.mkdir(exist_ok=True)
SLOTS=[1.5,2.5,2.8,2.7,2.7,2.8,2.5,2.5]
TITLES=["月980円。","見慣れた毎月の請求","12か月で…","その契約、使ってる？","① 明細を開く","② 利用頻度を見る","③ 解約条件を確認","小さな固定費を、見える化。"]
SUBS=["1年だと、いくら？","980円 × 12か月","11,760円","使っていないなら見直し候補","毎月の固定支出を確認","使う・使わないを仕分ける","必要なら公式手順で変更","まずは明細を1つ見直そう"]
VOICE=["","毎月の支払い。","一年で、一万千七百六十円。","使っていますか。","明細を見よう。","使っているか確認。","解約条件を確認。","まずは一つ見直そう。"]
GENRES=["AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし"]
assert sum(round(s*30) for s in SLOTS)==600
def run(args):
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode: raise RuntimeError(p.stderr[-1200:])
 return p.stdout
def font(size,bold=False):
 path="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
 return ImageFont.truetype(path,size)
def slide(i):
 im=Image.new("RGB",(1080,1920),"#081A2B")
 d=ImageDraw.Draw(im)
 d.rounded_rectangle((65,92,1015,112),radius=10,fill="#365A66")
 d.rounded_rectangle((65,92,65+round(950*(i+1)/8),112),radius=10,fill="#74E5C4")
 d.text((72,160),"MONEY RESET   /   20 SEC",font=font(35,True),fill="#74E5C4")
 d.text((72,310),TITLES[i],font=font(65,True),fill="white")
 d.text((72,410),SUBS[i],font=font(42),fill="#B9D2D8")
 d.rounded_rectangle((70,570,1010,1390),radius=52,fill="#183C4E",outline="#447181",width=4)
 center=["¥980","¥980 × 12","¥11,760","使う？","明細","利用頻度","解約条件","見える化"][i]
 size=155 if len(center)<7 else 110
 d.text((540,960),center,font=font(size,True),fill="#74E5C4",anchor="mm")
 d.rounded_rectangle((70,1500,1010,1635),radius=27,fill="#F7F5E8")
 d.text((540,1567),VOICE[i] or "まず、金額を見よう。",font=font(43,True),fill="#173F49",anchor="mm")
 d.text((72,1740),"ORIGINAL VECTOR  •  FICTIONAL EXAMPLE",font=font(28),fill="#ADC8D0")
 d.text((72,1800),"HUMAN REVIEW ONLY / NO AUTO POST",font=font(26),fill="#ADC8D0")
 p=OUT/f"scene_{i:02d}.png";im.save(p);return p
def probe(path):
 return json.loads(run(["ffprobe","-v","error","-show_entries","stream=codec_name,codec_type,width,height:format=duration","-of","json",str(path)]))
def main():
 images=[slide(i) for i in range(8)]
 playlist=OUT/"slides.txt"
 playlist.write_text("".join(f"file '{p.resolve()}'\\nduration {sec}\\n" for p,sec in zip(images,SLOTS))+f"file '{images[-1].resolve()}'\\n")
 video=OUT/"silent.mp4"
 run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(playlist),"-r","30","-t","20","-c:v","libx264","-pix_fmt","yuv420p",str(video)])
 wavs=[]
 for i,(seconds,line) in enumerate(zip(SLOTS,VOICE)):
  wav=OUT/f"voice_{i:02d}.wav"
  if not line:
   run(["ffmpeg","-y","-v","error","-f","lavfi","-i","anullsrc=r=48000:cl=mono","-t",str(seconds),str(wav)])
  else:
   mp3=OUT/f"voice_{i:02d}.mp3"
   gTTS(line,lang="ja").save(str(mp3))
   duration=float(probe(mp3)["format"]["duration"])
   speed=max(1.,duration/(seconds-.18))
   if speed>1.40:raise RuntimeError(f"Scene {i} speech too long: {speed:.2f}x")
   run(["ffmpeg","-y","-v","error","-i",str(mp3),"-af",f"atempo={speed:.4f},apad,atrim=duration={seconds}","-ar","48000","-ac","1",str(wav)])
  wavs.append(wav)
 ap=OUT/"audio.txt"
 ap.write_text("".join(f"file '{p.resolve()}'\\n" for p in wavs))
 narration=OUT/"narration.wav"
 run(["ffmpeg","-y","-v","error","-f","concat","-safe","0","-i",str(ap),"-c:a","pcm_s16le",str(narration)])
 if abs(float(probe(narration)["format"]["duration"])-20)>.15:raise RuntimeError("narration duration invalid")
 final=OUT/"cycle441_ci_JA_REVIEW_ONLY_916.mp4"
 run(["ffmpeg","-y","-v","error","-i",str(video),"-i",str(narration),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","aac","-b:a","160k","-t","20","-movflags","+faststart",str(final)])
 info=probe(final)
 assert any(x["codec_type"]=="audio" for x in info["streams"])
 assert info["streams"][0]["width"]==1080 and info["streams"][0]["height"]==1920
 run(["ffmpeg","-v","error","-xerror","-i",str(final),"-f","null","-"])
 (OUT/"qa.json").write_text(json.dumps({"cycle":441,"voice_engine":"gTTS ja","narration":"SYNTHESIZED_NOT_HUMAN_VERIFIED","subtitles":"BURNED_IN_PER_SCENE","duration":20,"approval":"HUMAN_REVIEW","publication":"NOT_APPROVED","genres":GENRES},ensure_ascii=False,indent=2))
 print(final)
if __name__=="__main__":main()
