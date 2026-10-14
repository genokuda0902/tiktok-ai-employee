"""cycle563: original proof animation, review only. Requires approved source MP4."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, json, math, subprocess

GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FPS=30
@dataclass(frozen=True)
class Proof:
    genre:str
    title:str
    source_label:str
    transform_label:str
    result_label:str
    values:tuple[int,...]
    simulated:bool=True
    verified_real_outcome:bool=False

DEFAULT=Proof(GENRES[0],"同じ4か月の売上、どう確認する？","売上データを転記","SUM関数で集計","人が元データを検算",(120,150,200,250))

def validate(p):
    if p.genre not in GENRES: raise ValueError("unsupported genre")
    if not p.simulated or p.verified_real_outcome: raise ValueError("synthetic scene must not claim real outcomes")
    if not 2<=len(p.values)<=6: raise ValueError("need 2-6 values")
    if any(type(v) is not int or not 0<=v<=9999 for v in p.values): raise ValueError("invalid data")
    if any(not x or len(x)>42 for x in (p.title,p.source_label,p.transform_label,p.result_label)): raise ValueError("text length")
    return True

def ease(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)

def draw_frame(p,t):
    validate(p)
    W,H=720,1280
    im=Image.new("RGB",(W,H),(7,20,36))
    d=ImageDraw.Draw(im)
    f=lambda s,b=False:ImageFont.truetype(BOLD if b else FONT,s)
    def label(x,y,s,size=25,color=(235,249,251),bold=False):
        d.text((x,y),s,font=f(size,bold),fill=color)
    def box(b,r=15,fill=(16,37,55),edge=None,w=1):
        d.rounded_rectangle(b,radius=r,fill=fill,outline=edge,width=w)
    for y in range(0,H,4):
        k=y/H;d.rectangle((0,y,W,y+3),fill=(round(7+7*k),round(23+8*k),round(41+14*k)))
    for x in range(24,W,56): d.line((x,160,x,1135),fill=(13,35,52))
    box((28,32,692,104),24,(12,55,76),(40,193,199),2)
    label(54,51,"AI時短ラボ  /  検証の流れ",28,bold=True)
    label(38,149,p.title,34,bold=True)
    label(38,205,"架空の数値を使った操作イメージ",20,(140,180,197))
    box((30,266,348,956),22,(15,34,53),(53,111,144),3)
    box((368,266,690,956),22,(15,34,53),(24,168,143),3)
    box((48,286,330,349),14,(35,56,75));box((388,286,670,349),14,(16,82,78))
    label(66,298,"INPUT  /  元データ",25,bold=True)
    label(404,298,"TRANSFORM  /  式",24,bold=True)
    label(54,374,p.source_label,24)
    label(390,374,p.transform_label,24)
    d.line((54,429,325,429),fill=(77,108,125),width=2)
    label(60,441,"月",23,(154,187,202));label(182,441,"売上（架空）",22,(154,187,202))
    visible=min(len(p.values),max(0,int((t-.20)/.34)+1));subtotal=0
    for i,v in enumerate(p.values):
        y=500+i*76;active=i<visible
        box((53,y,325,y+65),10,(22,53,70) if active else (18,42,58))
        label(72,y+13,f"{i+1}月",25,(228,244,248) if active else (81,112,127))
        label(190,y+13,f"{v:,}" if active else "—",26,(240,247,252) if active else (81,112,127),active)
        if active:subtotal+=v
    box((53,834,326,925),12,(30,62,75))
    label(72,844,"入力済みの合計",20,(163,203,212))
    label(73,870,f"{subtotal:,}",36,bold=True)
    box((389,438,671,530),12,(238,247,247))
    formula="=SUM(B2:B5)";n=int(len(formula)*ease((t-1)/1))
    label(405,455,formula[:n]+("▏" if t<2 else ""),28,(13,63,67),True)
    label(396,550,"計算結果",23,(171,214,207))
    ready=t>=2;total=sum(p.values)
    box((388,590,669,679),12,(19,91,85) if ready else (25,54,67))
    label(407,603,f"{total:,}" if ready else "計算中…",40,(238,255,247) if ready else (157,187,194),True)
    maximum=max(1,max(p.values))
    for i,v in enumerate(p.values):
        x=405+i*64;h=int(112*(v/maximum)*ease((t-1.7-i*.17)/.65))
        d.rounded_rectangle((x,842-h,x+39,842),radius=5,fill=(44,206,193))
        label(x+1,851,f"{i+1}月",16,(179,215,218))
    verified=t>=2.85
    box((36,985,684,1117),18,(11,70,67) if verified else (32,51,69),(32,193,169) if verified else (68,97,113),2)
    label(56,1005,"RESULT  /  検算",25,(167,240,223),True)
    label(55,1050,f"左右の合計：{total:,}  ✓" if verified else "入力 → 数式 → 確認",32,bold=True)
    label(38,1150,"※再現デモ／実測の時短効果は示していません",19,(164,184,193))
    fade=min(1,ease(t/.20),ease((4-t)/.18))
    if fade<1:im=Image.blend(Image.new("RGB",(W,H),(7,20,36)),im,fade)
    return im

def render(source,output):
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    if not source.is_file():raise FileNotFoundError(source)
    p=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(source)],capture_output=True,text=True,check=True)
    streams=json.loads(p.stdout)
    v=next(x for x in streams["streams"] if x["codec_type"]=="video")
    if (v["width"],v["height"],v["codec_name"])!=(1080,1920,"h264") or abs(float(streams["format"]["duration"])-20)>.1:
        raise ValueError("20s 1080x1920 H264 source required")
    if not any(x["codec_type"]=="audio" for x in streams["streams"]):raise ValueError("missing source audio")
    scene=output.with_name("cycle563_scene.mp4")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s","720x1280","-r","30","-i","-","-vf","scale=1080:1920:flags=lanczos","-c:v","libx264","-preset","ultrafast","-crf","18","-pix_fmt","yuv420p","-an",str(scene)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(120):proc.stdin.write(draw_frame(DEFAULT,i/FPS).tobytes())
        proc.stdin.close()
        error=proc.stderr.read().decode(errors="replace")
        if proc.wait():raise RuntimeError(error[-500:])
    finally:
        if proc.poll() is None:proc.kill()
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-i",str(scene),"-filter_complex","[1:v]setpts=PTS+2/TB[insert];[0:v][insert]overlay=0:0:eof_action=pass:enable='gte(t,2)*lt(t,6)'[v]","-map","[v]","-map","0:a:0","-map","0:s:0?","-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p","-r","30","-c:a","copy","-c:s","copy","-movflags","+faststart","-t","20",str(output)]
    subprocess.run(cmd,check=True)
    return output

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True);parser.add_argument("--output",required=True)
    args=parser.parse_args()
    print(render(args.source,args.output))
