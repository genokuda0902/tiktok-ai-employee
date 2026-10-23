"""Review-only caption renderer. FFmpeg + libass + Noto Sans CJK required."""
import subprocess
import sys
from pathlib import Path
from caption_contract import SPEECH_WINDOWS,CAPTIONS,validate

def timestamp(t):
    return f"{int(t//3600)}:{int(t//60)%60:02d}:{t%60:05.2f}"

def ass_text():
    head="[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
    head+="Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
    head+="Style: Caption,Noto Sans CJK JP,54,&H00FFFFFF,&H00FFFFFF,&H00231907,&H60231907,-1,0,0,0,100,100,0,0,3,15,0,2,96,96,275,1\n"
    head+="\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
    return head+"".join(f"Dialogue: 0,{timestamp(a)},{timestamp(b)},Caption,,0,0,0,,{c}\n" for (a,b),c in zip(SPEECH_WINDOWS,CAPTIONS))

def render(source,output,genre):
    validate(genre)
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True)
    ass=out.with_suffix(".ass");ass.write_text(ass_text(),encoding="utf-8")
    temp=out.with_name("video_only.mp4")
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(source),"-vf",f"subtitles={ass}","-an","-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-r","30","-frames:v","819",str(temp)],check=True)
    subprocess.run(["ffmpeg","-y","-v","error","-i",str(temp),"-i",str(source),"-map","0:v:0","-map","1:a:0","-c:v","copy","-c:a","copy",str(out)],check=True)
    temp.unlink()
    return out

if __name__=="__main__":
    render(sys.argv[1],sys.argv[2],sys.argv[3])
