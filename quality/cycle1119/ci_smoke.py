"""Synthetic 1.5-second 1080x1920 H264/AAC QA, not the private review MP4."""
import subprocess,tempfile,json
from pathlib import Path
from proof_component import draw_hook_frame,W,H,FPS
with tempfile.TemporaryDirectory() as d:
 path=Path(d)/"synthetic.mp4"
 cmd=["ffmpeg","-hide_banner","-loglevel","error","-y",
      "-f","rawvideo","-pixel_format","rgb24","-video_size",f"{W}x{H}",
      "-framerate",str(FPS),"-i","pipe:0",
      "-f","lavfi","-i","anullsrc=r=48000:cl=mono",
      "-map","0:v:0","-map","1:a:0","-t","1.5",
      "-c:v","libx264","-preset","ultrafast","-pix_fmt","yuv420p",
      "-c:a","aac","-movflags","+faststart",str(path)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for f in range(45):p.stdin.write(draw_hook_frame(f/FPS).tobytes())
  p.stdin.close();err=p.stderr.read().decode();rc=p.wait()
  if rc:raise RuntimeError(err[-1200:])
 except Exception:
  p.kill();p.wait();raise
 meta=json.loads(subprocess.check_output(["ffprobe","-v","error",
  "-show_entries","stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames",
  "-of","json",str(path)]))
 v=next(x for x in meta["streams"] if x["codec_type"]=="video")
 a=next(x for x in meta["streams"] if x["codec_type"]=="audio")
 assert (v["codec_name"],v["width"],v["height"],v["r_frame_rate"],int(v["nb_frames"]))==("h264",1080,1920,"30/1",45)
 assert a["codec_name"]=="aac"
 subprocess.run(["ffmpeg","-v","error","-i",str(path),"-f","null","-"],check=True)
 print("PASS synthetic 1.5s 1080x1920 30fps H264/AAC full decode")
