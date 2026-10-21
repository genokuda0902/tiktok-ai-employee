"""Offline scene-aware focus light; original Japanese AAC is stream-copied."""
import argparse,json,math,subprocess
from pathlib import Path
import cv2,numpy as np

def validate_config(c):
    assert c["canvas"]=={"width":1080,"height":1920,"fps":30}
    r=c["roi"]
    assert 0<=r["x"] and 0<=r["y"] and r["x"]+r["width"]<=1080 and r["y"]+r["height"]<=1380
    assert 10<=r["feather_px"]<=min(r["width"],r["height"])//4
    seen=set()
    for s in c["shots"]:
        assert 0<=s["start_frame"]<s["end_frame"]<=429
        assert 5<=s["max_glow"]<=40 and 80<=s["radius_px"]<=400
        assert 100<s["focus_x"]<950 and 500<s["focus_y"]<1150
        for i in range(s["start_frame"],s["end_frame"]):
            assert i not in seen
            seen.add(i)

def feather_mask(w,h,edge):
    x=np.minimum(np.arange(w),w-1-np.arange(w))/edge
    y=np.minimum(np.arange(h),h-1-np.arange(h))/edge
    x=np.clip(x,0,1);y=np.clip(y,0,1)
    x=x*x*(3-2*x);y=y*y*(3-2*y)
    return np.outer(y,x).astype(np.float32)

def eased_focus(i,s):
    n=s["end_frame"]-s["start_frame"]
    p=(i-s["start_frame"])/max(1,n-1)
    if not 0<=p<=1:return 0.0,float(s["focus_x"])
    return math.sin(math.pi*p)**2,s["focus_x"]+s["drift_x_px"]*math.sin(2*math.pi*p)

def apply_focus(frame,i,c,mask=None):
    s=next((x for x in c["shots"] if x["start_frame"]<=i<x["end_frame"]),None)
    if s is None:return frame
    strength,cx=eased_focus(i,s)
    if strength<0.0001:return frame
    r=c["roi"];x,y,w,h=r["x"],r["y"],r["width"],r["height"]
    yy,xx=np.ogrid[y:y+h,x:x+w]
    rad=s["radius_px"]
    light=np.exp(-((xx-cx)**2+(yy-s["focus_y"])**2)/(2*rad*rad)).astype(np.float32)
    alpha=mask if mask is not None else feather_mask(w,h,r["feather_px"])
    power=(light*alpha*strength*s["max_glow"])[:,:,None]
    tint=np.array([0.85,1.0,0.20],dtype=np.float32).reshape(1,1,3)
    result=frame.copy()
    roi=frame[y:y+h,x:x+w].astype(np.float32)
    result[y:y+h,x:x+w]=np.clip(roi+power*tint,0,255).astype(np.uint8)
    return result

def render(source,target,c):
    validate_config(c)
    source=Path(source);target=Path(target)
    if not source.is_file() or source.resolve()==target.resolve():raise ValueError("invalid source")
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError("cannot decode source")
    if (int(cap.get(3)),int(cap.get(4)))!=(1080,1920):raise ValueError("invalid resolution")
    target.parent.mkdir(parents=True,exist_ok=True)
    cmd=["ffmpeg","-hide_banner","-nostdin","-y","-loglevel","error",
      "-f","rawvideo","-pixel_format","bgr24","-video_size","1080x1920",
      "-framerate","30","-i","pipe:0","-i",str(source),
      "-map","0:v:0","-map","1:a:0","-c:v","libx264",
      "-preset","veryfast","-crf","17","-pix_fmt","yuv420p","-r","30",
      "-c:a","copy","-movflags","+faststart",str(target)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    r=c["roi"];mask=feather_mask(r["width"],r["height"],r["feather_px"])
    count=0
    try:
        while True:
            ok,f=cap.read()
            if not ok:break
            p.stdin.write(apply_focus(f,count,c,mask).tobytes())
            count+=1
        p.stdin.close()
        err=p.stderr.read().decode("utf-8","replace")
        if p.wait(timeout=180):raise RuntimeError(err[-500:])
    finally:
        cap.release()
        if p.poll() is None:p.kill()
    if count!=429 or not target.exists() or target.stat().st_size<100000:raise RuntimeError("bad render")
    return count

if __name__=="__main__":
    root=Path(__file__).resolve().parent
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    ap.add_argument("--config",type=Path,default=root/"motion.json")
    args=ap.parse_args()
    print(render(args.source,args.output,json.loads(args.config.read_text(encoding="utf-8"))))
