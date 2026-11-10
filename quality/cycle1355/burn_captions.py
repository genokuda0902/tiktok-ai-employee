"""Review-only burn-in for an approved synthetic MP4 and SRT. Never asserts speech sync."""
from pathlib import Path
import subprocess, json, sys
def render(source:Path, captions:Path, output:Path):
    if not source.is_file() or not captions.is_file():
        raise FileNotFoundError("missing source video or SRT")
    style="FontName=Noto Sans CJK JP,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,BackColour=&H99000000,MarginV=140"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(source),"-vf",f"subtitles={captions}:force_style='{style}'","-c:v","libx264","-crf","21","-pix_fmt","yuv420p","-an","-movflags","+faststart",str(output)],check=True)
    manifest={"review_only":True,"caption_burned_in":True,"japanese_narration_verified":False,"speech_sync_verified":False,"publication_approved":False}
    output.with_suffix(".json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    return manifest
if __name__=="__main__":
    if len(sys.argv)!=4: raise SystemExit("usage: python burn_captions.py input.mp4 captions.srt output.mp4")
    render(*map(Path,sys.argv[1:]))
