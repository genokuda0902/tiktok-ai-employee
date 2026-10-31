"""Compose original proof-trace frames over a private, locally held approved source.
Never uploads media. Source audio is stream-copied, not synthesized or ASR-verified.
"""
from __future__ import annotations
import argparse, subprocess
from pathlib import Path
from proof_trace import make_frames

def render(source:Path,output:Path,work:Path,genre='ai_work'):
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    frames=work/'proof_frames';make_frames(frames,genre)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate','30','-start_number','0','-i',str(frames/'frame_%03d.png'),
         '-filter_complex','[1:v]setpts=PTS+11.4/TB[replacement];[0:v][replacement]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','copy',
         '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);p.add_argument('--work',required=True);p.add_argument('--genre',default='ai_work')
    a=p.parse_args();render(Path(a.source),Path(a.out),Path(a.work),a.genre)
