"""2-second synthetic, zero-external-media smoke. Not the user-review MP4."""
import json,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from depth_component import draw_depth_hero
with tempfile.TemporaryDirectory() as tmp:
    root=Path(tmp)
    for i in range(12):
        canvas=Image.new("RGB",(1080,1920),(6,24,39))
        canvas.paste(draw_depth_hero(i/6),(64,507))
        canvas.save(root/f"frame_{i:03}.png")
    mp4=root/"synthetic.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-framerate","6","-i",str(root/"frame_%03d.png"),
                    "-vf","fps=30","-c:v","libx264","-pix_fmt","yuv420p","-t","2",str(mp4)],check=True)
    p=subprocess.run(["ffprobe","-v","error","-count_frames","-show_entries",
                      "stream=width,height,nb_read_frames","-of","json",str(mp4)],
                     capture_output=True,text=True,check=True)
    meta=json.loads(p.stdout)["streams"][0]
    assert (meta["width"],meta["height"],meta["nb_read_frames"])==(1080,1920,"60"),meta
    subprocess.run(["ffmpeg","-v","error","-xerror","-i",str(mp4),"-f","null","-"],check=True)
    print("PASS synthetic 1080x1920 / 30fps / 60 frames / full decode")
