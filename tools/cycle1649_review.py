"""Offline review-only caption overlay. Requires a rights-cleared input MP4."""
import argparse, json, subprocess
from pathlib import Path
CUES=((0,3,"入力前を確認"),(3,6,"表記ゆれを発見"),(6,9,"修正後を比較"),(9,12,"最後に人が確認"))
def render(source, target, font="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"):
    source,target=Path(source),Path(target)
    if not source.is_file(): raise FileNotFoundError(source)
    filters=["drawbox=x=64:y=1450:w=952:h=190:color=black@0.80:t=fill"]
    for start,end,caption in CUES:
        filters.append(f"drawtext=fontfile={font}:text='{caption}':fontcolor=white:fontsize=56:x=(w-text_w)/2:y=1502:enable='between(t,{start},{end})'")
    filters.append(f"drawtext=fontfile={font}:text='音声未生成・投稿禁止':fontcolor=yellow:fontsize=28:x=(w-text_w)/2:y=1700")
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",",".join(filters),"-t","12","-an","-c:v","libx264","-pix_fmt","yuv420p",str(target)],check=True)
    info=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",str(target)]))
    v=next(s for s in info["streams"] if s["codec_type"]=="video")
    assert (v["width"],v["height"])==(1080,1920)
    assert not any(s["codec_type"]=="audio" for s in info["streams"])
    subprocess.run(["ffmpeg","-v","error","-i",str(target),"-f","null","-"],check=True)
    return {"video_decode":True,"japanese_narration":False,"speech_synced_captions":False,"publication_approved":False}
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("source");p.add_argument("target")
    a=p.parse_args();print(json.dumps(render(a.source,a.target)))
