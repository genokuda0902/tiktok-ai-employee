"""Build review-only MP4 from original Pillow slides and Japanese WAV files."""
import json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from tts import SCRIPTS,synthesize
W,H,FPS=1080,1920,30
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
TITLES=["会議メモ、読んで終わり？","決定・担当・期限に分ける",
        "AIへの指示はこの一文","メモが行動リストになる",
        "名前と期限は人が確認","AIは整理役。最終確認は自分"]
def run(args):
    subprocess.run(args,check=True)
def make_slide(i,where):
    im=Image.new("RGB",(W,H),"#0D2036");d=ImageDraw.Draw(im)
    f=lambda n:ImageFont.truetype(FONT,n)
    d.rounded_rectangle((70,80,1010,190),radius=25,fill="#16374D")
    d.text((100,106),"AI時短ラボ",font=f(48),fill="white")
    d.text((790,120),f"{i+1:02d}/06",font=f(37),fill="#77E8CC")
    d.text((80,340),TITLES[i],font=f(60),fill="#FFFFFF")
    d.rounded_rectangle((85,680,995,1350),radius=35,fill="#16425A",outline="#6ADDC9",width=4)
    d.text((130,760),["BEFORE","SORT","PROMPT","RESULT","VERIFY","SAVE"][i],font=f(67),fill="#72EAD2")
    for j,line in enumerate([SCRIPTS[i][k:k+15] for k in range(0,len(SCRIPTS[i]),15)]):
        d.text((115,1480+j*70),line,font=f(44),fill="#FFFFFF")
    d.text((85,1800),"架空の例｜要確認｜投稿未承認",font=f(32),fill="#9AB5C8")
    im.save(where)
def build():
    out=Path(__file__).parent/"out";out.mkdir(exist_ok=True)
    voices=synthesize(out);segs=[]
    for i,wav in enumerate(voices):
        png=out/f"scene_{i}.png";make_slide(i,png)
        probe=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(wav)])
        seconds=max(3,float(json.loads(probe)["format"]["duration"])+0.5)
        seg=out/f"seg_{i}.mp4"
        run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","30","-i",str(png),
             "-i",str(wav),"-filter_complex",f"[1:a]aresample=48000,apad,atrim=duration={seconds:.3f}[a]",
             "-map","0:v","-map","[a]","-t",str(seconds),"-c:v","libx264","-preset","ultrafast",
             "-pix_fmt","yuv420p","-c:a","aac","-b:a","128k",str(seg)])
        segs.append(seg)
    listing=out/"concat.txt"
    listing.write_text("\n".join("file '"+str(p.resolve())+"'" for p in segs))
    target=out/"cycle487_JAPANESE_TTS_REVIEW_NOT_APPROVED.mp4"
    run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",str(listing),
         "-c:v","copy","-c:a","aac","-movflags","+faststart",str(target)])
    run(["ffmpeg","-v","error","-i",str(target),"-f","null","-"])
    probe=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(target)]))
    v=next(x for x in probe["streams"] if x["codec_type"]=="video")
    a=next(x for x in probe["streams"] if x["codec_type"]=="audio")
    assert (v["width"],v["height"],v["codec_name"],a["codec_name"])==(W,H,"h264","aac")
    (out/"qa.json").write_text(json.dumps({"video":"1080x1920 H264","audio":"AAC",
        "japanese_tts":"Open JTalk generated, not human-audited","captions":"scene-level",
        "rights":"original Pillow graphics","publication":"NOT_APPROVED"},ensure_ascii=False,indent=2))
if __name__=="__main__":build()
