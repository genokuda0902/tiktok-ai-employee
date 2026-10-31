"""Two-second synthetic H264/AAC smoke test; NOT the final review video."""
import subprocess
from PIL import Image
from kinetic_focus import draw_focus
W,H,FPS=1080,1920,30
cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-f","rawvideo",
     "-pixel_format","rgb24","-video_size",f"{W}x{H}","-framerate",str(FPS),
     "-i","pipe:0","-f","lavfi","-i","anullsrc=r=48000:cl=mono",
     "-map","0:v:0","-map","1:a:0","-t","2","-c:v","libx264",
     "-preset","ultrafast","-pix_fmt","yuv420p","-c:a","aac",
     "-movflags","+faststart","/tmp/cycle1117_smoke.mp4"]
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
try:
 base=Image.new("RGB",(W,H),(10,30,48))
 for frame in range(60):
  p.stdin.write(draw_focus(base.copy(),0,frame/FPS,3).tobytes())
 p.stdin.close();err=p.stderr.read();rc=p.wait()
 if rc:raise RuntimeError(err.decode())
except Exception:
 p.kill();p.wait();raise
r=subprocess.run(["ffmpeg","-v","error","-i","/tmp/cycle1117_smoke.mp4","-f","null","-"],capture_output=True)
assert r.returncode==0,r.stderr
print("PASS synthetic 2s 1080x1920 H264/AAC full decode")
