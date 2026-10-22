"""Render review-only MP4 with Japanese captions; require approved source hash."""
import argparse, hashlib, subprocess
from pathlib import Path
from cycle758_layout import GENRES, parse_srt, make_ass

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def render(source, srt, output, expected_sha, genre='ai_work'):
    source, srt, output = Path(source), Path(srt), Path(output)
    if len(expected_sha) != 64 or sha256(source) != expected_sha:
        raise ValueError('unapproved source')
    if source.resolve() == output.resolve():
        raise ValueError('cannot overwrite input')
    output.parent.mkdir(parents=True, exist_ok=True)
    ass = output.with_suffix('.ass')
    ass.write_text(make_ass(parse_srt(srt.read_text(encoding='utf-8-sig')), genre), encoding='utf-8')
    path = str(ass.resolve()).replace(':', r'\:')
    cmd = ['ffmpeg','-y','-loglevel','error','-i',str(source),
           '-vf',f'ass=filename={path}','-map','0:v:0','-map','0:a:0',
           '-c:v','libx264','-crf','20','-pix_fmt','yuv420p',
           '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=240)
    return sha256(output)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--srt',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--expected-sha',required=True)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    a = p.parse_args()
    print(render(a.source,a.srt,a.output,a.expected_sha,a.genre))
