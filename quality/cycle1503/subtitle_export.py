"""Review-only burn-in captions; no speech/approval claims."""
import subprocess,sys
from pathlib import Path
def export(source,captions,output):
    source,captions,output=map(Path,(source,captions,output))
    if not source.is_file() or not captions.is_file(): raise FileNotFoundError("input missing")
    s=captions.read_text(encoding="utf-8-sig")
    if "-->" not in s or not any("\u3040"<=c<="\u9fff" for c in s): raise ValueError("timed Japanese captions required")
    style="FontName=Noto Sans CJK JP,FontSize=18,Outline=2,Shadow=0,Alignment=2,MarginV=150"
    subprocess.run(["ffmpeg","-y","-i",str(source),"-vf",f"subtitles={captions.resolve()}:force_style='{style}'","-c:v","libx264","-crf","22","-c:a","copy","-movflags","+faststart",str(output)],check=True)
    subprocess.run(["ffmpeg","-v","error","-i",str(output),"-f","null","-"],check=True)
    return {"publication_approved":False,"japanese_narration_verified":False,"speech_caption_sync_verified":False}
if __name__=="__main__": print(export(*sys.argv[1:4]))
