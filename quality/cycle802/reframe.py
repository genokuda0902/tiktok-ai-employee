"""Review-only 10-genre scene-safe optical reframe. Never commit user media."""
import argparse
import json
import subprocess
from pathlib import Path

W, H, FPS = 1080, 1920, 30

def load_config(path):
    cfg=json.loads(Path(path).read_text(encoding="utf-8"))
    if cfg.get("mode")!="review_only": raise ValueError("review_only required")
    for key in ("rights_reviewed","employee_approved","publication_approved"):
        if cfg.get(key) is not False: raise ValueError(key+" must be false")
    genres=cfg.get("genres")
    if not isinstance(genres,list) or len(genres)!=10 or len(set(genres))!=10:
        raise ValueError("exactly ten distinct genres")
    shift=cfg.get("shift_px")
    if not isinstance(shift,int) or not 0<=shift<=180 or shift%2:
        raise ValueError("even shift_px 0..180 required")
    windows=cfg.get("windows")
    if not isinstance(windows,list) or not windows: raise ValueError("scene windows required")
    last_end=0.0
    for scene in windows:
        start,end,box=scene.get("start"),scene.get("end"),scene.get("important_content_x")
        if not isinstance(start,(int,float)) or not isinstance(end,(int,float)) or not 0<=last_end<=start<end<=cfg.get("max_duration",25):
            raise ValueError("invalid or overlapping scene windows")
        if not isinstance(box,list) or len(box)!=2 or not all(isinstance(x,int) for x in box):
            raise ValueError("scene content x bounds required")
        left,right=box
        if not 0<=left<right<=W: raise ValueError("invalid bounds")
        if left+shift<cfg.get("left_safe_px",0) or right+shift>W-cfg.get("right_safe_px",0):
            raise ValueError("unsafe text or UI placement")
        last_end=end
    if (cfg.get("width"),cfg.get("height"),cfg.get("fps"))!=(W,H,FPS):
        raise ValueError("1080x1920 30fps contract")
    return cfg

def probe(path):
    try:
        p=subprocess.run(["ffprobe","-v","error","-show_streams","-of","json",str(path)],check=True,capture_output=True,text=True)
        return json.loads(p.stdout)
    except FileNotFoundError:
        # GitHub hosted runners may not ship ffprobe. The pinned free FFmpeg
        # binary still prints source metadata. This fallback does not guess.
        import re
        p=subprocess.run(["ffmpeg","-hide_banner","-i",str(path)],capture_output=True,text=True)
        v=next((line for line in p.stderr.splitlines() if "Video:" in line and "Stream #" in line),None)
        a=next((line for line in p.stderr.splitlines() if "Audio:" in line and "Stream #" in line),None)
        if not v or not a: raise ValueError("cannot inspect both streams")
        wh=re.search(r"(\\d{3,4})x(\\d{3,4})",v)
        fps=re.search(r"(\\d+(?:\\.\\d+)?) fps",v)
        if not wh or not fps: raise ValueError("cannot inspect geometry/fps")
        fpsval=float(fps.group(1))
        return {"streams":[{"codec_type":"video","width":int(wh.group(1)),
                            "height":int(wh.group(2)),"r_frame_rate":f"{int(round(fpsval))}/1"},
                           {"codec_type":"audio"}]}

def assert_source(media):
    streams=probe(media)["streams"]
    video=next((s for s in streams if s["codec_type"]=="video"),None)
    audio=next((s for s in streams if s["codec_type"]=="audio"),None)
    if not video or not audio: raise ValueError("both video and audio required")
    if (video["width"],video["height"],video["r_frame_rate"])!=(W,H,"30/1"):
        raise ValueError("invalid source video geometry")
    return video,audio

def build_filter(cfg):
    shift=cfg["shift_px"]
    if shift==0: return "[0:v]null[v]"
    # Apply only to scenes with independently validated right-edge clearance.
    # The middle scenes contain edge-to-edge UI and MUST NOT be shifted.
    cond="+".join(f'between(t,{s["start"]},{s["end"]-0.0001:.4f})' for s in cfg["windows"])
    return (f"[0:v]split=3[orig][base][edge];"
            f"[edge]crop=2:{H}:0:0,scale={shift}:{H}:flags=neighbor[pad];"
            f"[pad][base]hstack=inputs=2,crop={W}:{H}:0:0[shifted];"
            f"[orig][shifted]overlay=shortest=1:enable='{cond}'[v]")

def render(input_path,output_path,cfg):
    src,dst=Path(input_path).resolve(),Path(output_path).resolve()
    if src==dst or not src.is_file(): raise ValueError("valid distinct input/output required")
    assert_source(src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    command=["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(src),
             "-filter_complex",build_filter(cfg),"-map","[v]","-map","0:a:0",
             "-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",
             "-r",str(FPS),"-c:a","copy","-movflags","+faststart",str(dst)]
    subprocess.run(command,check=True)
    assert_source(dst)
    return dst

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--config",required=True)
    ap.add_argument("--source-video",required=True)
    ap.add_argument("--output",required=True)
    ap.add_argument("--review-only",action="store_true",required=True)
    args=ap.parse_args()
    render(args.source_video,args.output,load_config(args.config))

if __name__=="__main__": main()
