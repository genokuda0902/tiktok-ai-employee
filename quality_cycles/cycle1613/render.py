"""Review-only caption safe area and fail-closed timeline validation for ten genres."""
from pathlib import Path
import subprocess, json, sys
CAPTIONS=[("表記ゆれをなくす",0,3),("入力データを統一",3,6),("集計式を確認",6,9),("結果を必ず照合",9,12)]
def validate(captions,duration=12):
    assert captions and all(0<=s<e<=duration for _,s,e in captions)
    assert all(a[2]<=b[1] for a,b in zip(captions,captions[1:]))
    assert all(len(t)<=18 for t,_,_ in captions)
def render(source,out):
    validate(CAPTIONS)
    font="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
    filters=["drawbox=x=30:y=1000:w=660:h=105:color=black@0.78:t=fill"]
    for caption,start,end in CAPTIONS:
        filters.append(f"drawtext=fontfile={font}:text='{caption}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=1022:enable='between(t,{start},{end-0.001})'")
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",",".join(filters),"-an","-r","24","-c:v","libx264","-preset","veryfast","-crf","24","-pix_fmt","yuv420p","-movflags","+faststart",str(out)],check=True)
    (out.parent/"caption_manifest.json").write_text(json.dumps({"review_only":True,"speech_synced":False,"captions":[{"text":t,"start":s,"end":e} for t,s,e in CAPTIONS]},ensure_ascii=False,indent=2))
if __name__=="__main__":
    if len(sys.argv)!=3:sys.exit("Usage: render.py INPUT_SYNTHETIC.mp4 OUTPUT.mp4")
    render(sys.argv[1],sys.argv[2])
