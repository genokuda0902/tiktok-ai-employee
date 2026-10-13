#!/usr/bin/env python3
"""cycle558 review-only: genre-neutral simulated AI chat typing insert.

Requires Pillow, ffmpeg, ffprobe, Noto Sans CJK fonts and a 20-second
1080x1920 H264/AAC review baseline. This is a REIMPLEMENTATION, not v33 source.
Inherited audio is NOT verified Japanese narration and is NOT approved.
"""
import argparse, functools, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=540,960,30
START,END=6.0,9.0
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
REG="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
BOLD="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
PROMPT=("4か月の売上データを集計。","120 / 150 / 200 / 250","合計と棒グラフを作成。","結果は人が検算する。")
@functools.lru_cache(maxsize=32)
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else REG,size)
def scene_contract(genre,lines,start=START,end=END):
    if genre not in GENRES:raise ValueError("unsupported genre")
    if not isinstance(lines,(tuple,list)) or not 1<=len(lines)<=5:raise ValueError("prompt lines")
    if any(not isinstance(s,str) or not s.strip() or len(s)>30 for s in lines):raise ValueError("invalid prompt")
    if not 0<=start<end<=20 or end-start>5:raise ValueError("invalid time window")
    return True
def typed_lines(t,lines=PROMPT):
    count=min(sum(map(len,lines)),max(0,int((t-.42)*24)))
    shown=[]
    for s in lines:
        n=min(len(s),count);shown.append(s[:n]);count-=n
    return shown
def draw_frame(n,genre=GENRES[0],lines=PROMPT):
    scene_contract(genre,lines)
    if not 0<=n<int((END-START)*FPS):raise ValueError("frame range")
    t=n/FPS
    im=Image.new("RGB",(W,H),(7,20,37));d=ImageDraw.Draw(im)
    for y in range(H):
        v=y/H;d.line((0,y,W,y),fill=(int(7+4*v),int(20+10*v),int(37+18*v)))
    for x in range(0,W,54):d.line((x,100,x,H-70),fill=(14,39,59))
    for y in range(130,H-50,55):d.line((20,y,W-20,y),fill=(14,39,59))
    d.rounded_rectangle((23,36,517,90),radius=17,fill="#063a52",outline="#26c6df",width=2)
    d.text((270,63),"AI時短ラボ  /  操作イメージ",font=font(21,True),fill="white",anchor="mm")
    d.text((30,144),"STEP 02",font=font(22,True),fill="#37e4df")
    d.text((30,197),"AIへの指示を見える化",font=font(32,True),fill="white")
    d.text((30,239),"4か月の売上をどう集計する？",font=font(20),fill="#b7d6e6")
    d.rounded_rectangle((25,287,515,738),radius=25,fill="#eaf2f6",outline="#56c5db",width=3)
    d.rounded_rectangle((25,287,515,346),radius=24,fill="#153d55")
    d.rectangle((25,323,515,347),fill="#153d55")
    for i,c in enumerate(("#ff7c7b","#ffd57b","#61d8a1")):d.ellipse((44+i*22,308,57+i*22,321),fill=c)
    d.text((270,317),"AIチャット（再現デモ）",font=font(20,True),fill="white",anchor="mm")
    d.rounded_rectangle((46,367,495,653),radius=17,fill="white",outline="#c9dce7",width=2)
    d.text((66,400),"指示文",font=font(20,True),fill="#0d5670")
    visible=typed_lines(t,lines)
    for i,s in enumerate(visible):d.text((65,451+i*47),s,font=font(21,i==0),fill="#182f45")
    if int(t*4)%2==0 and t<2.3:
        idx=max(0,min(len(lines)-1,next((i for i,s in enumerate(visible) if len(s)<len(lines[i])),len(lines)-1)))
        length=d.textlength(visible[idx],font=font(21,idx==0))
        d.line((65+length+3,442+idx*47,65+length+3,465+idx*47),fill="#17a3a8",width=3)
    active=t>=2.35
    d.rounded_rectangle((326,665,483,716),radius=14,fill="#0a9f9b" if active else "#608a99")
    d.text((404,690),"入力完了" if active else "入力中…",font=font(20,True),fill="white",anchor="mm")
    d.rounded_rectangle((35,770,505,855),radius=20,fill="#083d51",outline="#36e0d6",width=2)
    d.text((270,810),"入力 → 結果を確認 → 人が検算",font=font(24,True),fill="white",anchor="mm")
    d.text((270,908),"※架空データ／実際の送信はしていません",font=font(17),fill="#b9d5e3",anchor="mm")
    d.text((270,937),"HUMAN REVIEW  /  NOT APPROVED",font=font(12),fill="#98b6c9",anchor="mm")
    return im
def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path)]))
def render(base,output,genre=GENRES[0]):
    scene_contract(genre,PROMPT)
    base=Path(base);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    meta=probe(base);v=next(x for x in meta["streams"] if x["codec_type"]=="video")
    if (v["width"],v["height"])!=(1080,1920) or abs(float(meta["format"]["duration"])-20)>.1:raise ValueError("baseline mismatch")
    if not any(x["codec_type"]=="audio" for x in meta["streams"]):raise ValueError("baseline audio missing")
    scene=output.parent/"cycle558_chat_insert.mp4"
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{W}x{H}","-r",str(FPS),"-i","pipe:0","-an","-c:v","libx264","-preset","ultrafast","-crf","20","-pix_fmt","yuv420p",str(scene)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for n in range(int((END-START)*FPS)):proc.stdin.write(draw_frame(n,genre).tobytes())
    finally:proc.stdin.close()
    if proc.wait():raise RuntimeError("insert encoding failed")
    filt=(f"[1:v]scale=1080:1920:flags=lanczos,setpts=PTS-STARTPTS+{START}/TB[insert];"
          f"[0:v][insert]overlay=shortest=0:eof_action=pass:enable='between(t,{START},{END-1/FPS})',format=yuv420p[v]")
    cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(base),"-i",str(scene),"-filter_complex",filt,"-map","[v]","-map","0:a:0","-frames:v","600","-c:v","libx264","-preset","veryfast","-crf","22","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(output)]
    subprocess.run(cmd,check=True)
    result=probe(output);vv=next(x for x in result["streams"] if x["codec_type"]=="video")
    if (vv["width"],vv["height"],int(vv["nb_frames"]))!=(1080,1920,600) or abs(float(result["format"]["duration"])-20)>.05:raise RuntimeError("output mismatch")
    return output
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--base",required=True);p.add_argument("--output",required=True);p.add_argument("--genre",default=GENRES[0]);a=p.parse_args()
    print(render(a.base,a.output,a.genre))
