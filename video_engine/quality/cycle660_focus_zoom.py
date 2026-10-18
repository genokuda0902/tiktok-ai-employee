"""Review-only 10-genre genuine-screen-capture focus renderer. No posting."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
from PIL import Image, ImageDraw, ImageFont
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def validate(m, source):
    if m.get("genre") not in GENRES: raise ValueError("unknown genre")
    if m.get("publication")!="NOT_APPROVED": raise ValueError("publication gate")
    if m.get("rights")!="REVIEW_ONLY_UNVERIFIED": raise ValueError("rights gate")
    if m.get("data")!="SYNTHETIC": raise ValueError("privacy gate")
    if m.get("capture_method") not in ("x11grab","native_capture","screen_recording"): raise ValueError("capture method")
    if m.get("source_sha256")!=sha(source): raise ValueError("source SHA mismatch")
    cap=cv2.VideoCapture(str(source)); w=int(cap.get(3));h=int(cap.get(4));cap.release()
    x,y,cw,ch=m["crop"]
    if min(x,y)<0 or min(cw,ch)<=0 or x+cw>w or y+ch>h: raise ValueError("invalid crop")
    for key in ("formula_roi","result_roi"):
        a,b,c,d=m[key]
        if min(a,b)<0 or min(c,d)<=0 or a<x or b<y or a+c>x+cw or b+d>y+ch: raise ValueError("invalid focus ROI")
    return True
def render(source,base,out,m):
    validate(m,source)
    frames=out.parent/"focus_frames";frames.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source));srcfps=cap.get(5);length=cap.get(7)/srcfps
    font=ImageFont.truetype(FONT,52);small=ImageFont.truetype(FONT,36)
    x,y,cw,ch=m["crop"];ox,oy,ow,oh=52,510,976,770
    for i in range(60):
        t=i/20
        cap.set(0 if False else cv2.CAP_PROP_POS_MSEC,min(length-.07,t*length/3)*1000)
        ok,f=cap.read()
        if not ok: raise RuntimeError("capture decode failure")
        cropped=Image.fromarray(cv2.cvtColor(f[y:y+ch,x:x+cw],cv2.COLOR_BGR2RGB)).resize((ow,oh))
        im=Image.new("RGB",(1080,1920),"#051527");d=ImageDraw.Draw(im)
        d.text((58,145),"本物の操作を拡大",font=font,fill="white")
        d.text((58,270),"小さな数式と結果を見逃さない",font=small,fill="#b7eaff")
        d.rounded_rectangle((36,400,1044,1430),radius=32,fill="#0a2543",outline="#48d9f5",width=5)
        d.text((62,432),"REAL CAPTURE / 架空データ",font=small,fill="#a8d5e7")
        im.paste(cropped,(ox,oy));d=ImageDraw.Draw(im)
        a,b,c,e=m["formula_roi" if t<1.5 else "result_roi"]
        box=(ox+round((a-x)*ow/cw)-5,oy+round((b-y)*oh/ch)-5,ox+round((a+c-x)*ow/cw)+5,oy+round((b+e-y)*oh/ch)+5)
        color="#ffda54" if t<1.5 else "#3df9cc"
        d.rounded_rectangle(box,radius=8,outline=color,width=8)
        d.rounded_rectangle((65,1320,1015,1410),radius=18,fill="#113c57")
        d.text((93,1337),"① 数式 =SUM(B2:B5)" if t<1.5 else "② 計算結果 650",font=small,fill=color)
        d.text((90,1510),"120 + 150 + 200 + 180",font=small,fill="white")
        d.text((90,1580),"= 650  ✓  同じ数値を確認",font=small,fill="#5fffe0")
        d.text((63,1760),"REVIEW ONLY / 日本語ナレーション未搭載",font=small,fill="#9cbed0")
        im.save(frames/f"{i:04d}.jpg",quality=90)
    cap.release()
    clip=out.parent/"focus_scene.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-framerate","20","-i",str(frames/"%04d.jpg"),"-c:v","libx264","-pix_fmt","yuv420p",str(clip)],check=True)
    filt="[1:v]setpts=PTS-STARTPTS+10.5/TB[z];[0:v][z]overlay=0:0:enable='gte(t,10.5)*lt(t,13.5)':eof_action=pass[v]"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",str(base),"-i",str(clip),"-filter_complex",filt,"-map","[v]","-map","0:a:0","-r","30","-c:v","libx264","-pix_fmt","yuv420p","-c:a","copy","-movflags","+faststart",str(out)],check=True)
    return sha(out)
if __name__=="__main__":
    p=argparse.ArgumentParser()
    for name in ("source","base","out","manifest"):p.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    print(render(a.source,a.base,a.out,json.loads(a.manifest.read_text())))
