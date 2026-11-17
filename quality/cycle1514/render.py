"""Original synthetic review-only video; deliberately no audio or publication approval."""
import json, subprocess
from pathlib import Path
FONT="/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
SCENES=[("AIに仕事を任せる前に","目的を1行で伝える"),("次に条件を3つ決める","期限・形式・対象"),("最後は人が確認する","数字と事実を必ず照合")]
def segments():
    return [(i*2,(i+1)*2,h,b) for i,(h,b) in enumerate(SCENES)]
def manifest():
    return {"status":"PUBLICATION_NOT_APPROVED","review_only":True,"posting_allowed":False,"narration_verified":False,"caption_speech_sync_verified":False,"source":"original synthetic graphics","segments":segments()}
def render(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    f=["drawbox=x=36:y=155:w=648:h=950:color=0x132339@0.96:t=fill","drawbox=x=36:y=155:w=8:h=950:color=0x36b9bb:t=fill"]
    for i,(start,end,head,body) in enumerate(segments()):
        for t,y,size in [(head,430,38),(body,575,31)]:
            f.append(f"drawtext=fontfile={FONT}:text='{t}':fontcolor=white:fontsize={size}:x=(w-text_w)/2:y={y}:enable='between(t,{start},{end-0.001})'")
        f.append(f"drawbox=x={80+i*188}:y=820:w=160:h=10:color=0x36b9bb:t=fill:enable='between(t,{start},{end-0.001})'")
    f.append(f"drawtext=fontfile={FONT}:text='レビュー専用・音声未生成':fontcolor=0xffbd72:fontsize=26:x=(w-text_w)/2:y=1030")
    subprocess.run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","lavfi","-i","color=c=0x07111d:s=720x1280:r=24:d=6","-vf",",".join(f),"-an","-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p","-movflags","+faststart",str(path)],check=True)
    path.with_suffix(".json").write_text(json.dumps(manifest(),ensure_ascii=False,indent=2),encoding="utf-8")
if __name__=="__main__":
    import sys
    render(sys.argv[1])
