"""Review-only 23.033-second progress rail overlay. Does not certify voice, subtitles or rights."""
import subprocess
def filtergraph():
    return "drawbox=x=90:y=250:w=900:h=12:color=white@0.20:t=fill,drawbox=x=90:y=250:w='900*min(t/23.033,1)':h=12:color=0x46d9c7@0.95:t=fill"
def render(src,dst):
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(src),"-vf",filtergraph(),"-c:v","libx264","-preset","veryfast","-crf","22","-c:a","copy","-movflags","+faststart",str(dst)],check=True)
