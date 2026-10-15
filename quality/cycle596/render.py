"""Reproduce cycle596 from an authorized local baseline.

Run: python -m quality.cycle596.render --baseline BASELINE.mp4 --out OUT.mp4
No baseline or inherited audio is stored in GitHub. Review only.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
from .scene import frame,W,H,FPS
def run(args):
    p=subprocess.run(args,text=True,capture_output=True)
    if p.returncode:raise RuntimeError("ffmpeg: "+p.stderr[-1500:])
    return p.stdout
def render(baseline,out,scene_path,qa_path):
    p=subprocess.Popen(["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),"-i","-","-c:v","libx264","-preset","ultrafast","-crf","20","-pix_fmt","yuv420p",str(scene_path)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    for i in range(60):
        im,_=frame(i/FPS);p.stdin.write(im.tobytes())
    p.stdin.close();err=p.stderr.read();rc=p.wait()
    if rc:raise RuntimeError("scene encode failed: "+err.decode(errors="replace")[-1500:])
    filt="[1:v]setpts=PTS-STARTPTS+16/TB[insert];[0:v][insert]overlay=eof_action=pass:enable='gte(t,16)*lt(t,18)'[v]"
    run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(baseline),"-i",str(scene_path),"-filter_complex",filt,"-map","[v]","-map","0:a:0","-c:v","libx264","-preset","ultrafast","-crf","21","-pix_fmt","yuv420p","-r","30","-frames:v","600","-c:a","copy","-movflags","+faststart",str(out)])
    run(["ffmpeg","-v","error","-i",str(out),"-f","null","-"])
    meta=json.loads(run(["ffprobe","-v","error","-show_entries","stream=codec_name,codec_type,width,height,nb_frames,sample_rate:format=duration","-of","json",str(out)]))
    video=next(s for s in meta["streams"] if s["codec_type"]=="video")
    audio=next((s for s in meta["streams"] if s["codec_type"]=="audio"),None)
    if (video["width"],video["height"],int(video["nb_frames"]))!=(1080,1920,600) or not audio:raise ValueError("technical QA failed")
    result={"cycle":596,"sha256":hashlib.sha256(out.read_bytes()).hexdigest(),"full_decode":"PASS","video":video,"audio":audio,"japanese_voice_present":False,"voice_caption_sync_verified":False,"quality":"HUMAN_REVIEW","publication":"PUBLICATION_NOT_APPROVED"}
    qa_path.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    return result
if __name__=="__main__":
    a=argparse.ArgumentParser()
    a.add_argument("--baseline",type=Path,required=True)
    a.add_argument("--out",type=Path,required=True)
    a.add_argument("--scene",type=Path,default=Path("cycle596_scene.mp4"))
    a.add_argument("--qa",type=Path,default=Path("cycle596_qa.json"))
    x=a.parse_args()
    print(json.dumps(render(x.baseline,x.out,x.scene,x.qa),ensure_ascii=False))
