"""Review-only MP4 with always-visible and selectable Japanese captions. Reimplementation, not v33 original."""
from pathlib import Path
import subprocess

def validate_srt(text):
    if '-->' not in text or not any('\u3040' <= c <= '\u9fff' for c in text):
        raise ValueError('Japanese timed captions required')

def render(source: Path, srt: Path, output: Path):
    if not source.is_file() or not srt.is_file():
        raise FileNotFoundError('MP4 and SRT required')
    validate_srt(srt.read_text(encoding='utf-8-sig'))
    escaped = str(srt).replace('\\', '\\\\').replace(':', '\\:').replace("'", "\\'")
    vf = "subtitles='{}':force_style='FontName=Noto Sans CJK JP,FontSize=17,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=3,BackColour=&H99000000,MarginV=115,Alignment=2'".format(escaped)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(srt),'-map','0:v:0','-map','1:0','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p','-c:s','mov_text','-metadata:s:s:0','language=jpn','-movflags','+faststart',str(output)],check=True)
