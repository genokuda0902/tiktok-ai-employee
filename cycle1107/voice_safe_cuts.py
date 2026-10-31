"""Narration-pause scene retimer (amplitude only; no ASR or semantic checks).

No media is committed. All processing runs offline with FFmpeg; audio is copied.
"""
import json
import re
import subprocess
from pathlib import Path

FPS = 30
SOURCE_CUTS = [0, 79, 174, 258, 340, 423, 503, 593, 675]
TITLES = ['最初の一歩','繰り返し作業','完成形の見本','目的と条件','出力の確認','修正点','テンプレート化','毎日の習慣']


def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stderr[-1200:])
    return p.stderr


def detect_silences(path, threshold=-32, duration=.12):
    log = run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af',
               f'silencedetect=noise={threshold}dB:d={duration}','-f','null','-'])
    starts, spans = [], []
    for line in log.splitlines():
        m = re.search(r'silence_start: ([\d.]+)', line)
        n = re.search(r'silence_end: ([\d.]+)', line)
        if m: starts.append(float(m.group(1)))
        if n and starts:
            a,b = starts.pop(0),float(n.group(1))
            if b-a >= duration: spans.append((a,b))
    return spans


def snap_cuts(cuts, spans, max_shift=.72):
    new=[cuts[0]]
    for cut in cuts[1:-1]:
        t=cut/FPS
        choices=[(abs((a+b)/2-t),a,b) for a,b in spans
                 if abs((a+b)/2-t)<=max_shift and a>new[-1]/FPS+.4]
        earlier=[c for c in choices if (c[1]+c[2])/2<=t]
        if not choices: new.append(cut); continue
        _,a,b=min(earlier if earlier else choices)
        new.append(round((a+b)*FPS/2))
    new.append(cuts[-1])
    if any(b<=a for a,b in zip(new,new[1:])): raise ValueError('Invalid cuts')
    return new


def pts_expression(old,new):
    parts=[f'({new[i]}+(N-{old[i]})*{(new[i+1]-new[i])/(old[i+1]-old[i]):.12f})'
           for i in range(len(old)-1)]
    expr=parts[-1]
    for i in range(len(old)-2,0,-1):
        expr=f'if(lt(N,{old[i]}),{parts[i-1]},{expr})'
    return f'({expr})/(30*TB)'


def metadata(path,cuts):
    lines=[';FFMETADATA1','title=Voice-safe chapters']
    for i,(a,b) in enumerate(zip(cuts,cuts[1:])):
        lines+=['[CHAPTER]','TIMEBASE=1/30',f'START={a}',f'END={b}',f'title={i+1:02d}/08 {TITLES[i]}']
    Path(path).write_text('\n'.join(lines)+'\n',encoding='utf-8')


def render(source,output):
    source,output=Path(source),Path(output)
    spans=detect_silences(source)
    cuts=snap_cuts(SOURCE_CUTS,spans)
    output.parent.mkdir(parents=True,exist_ok=True)
    meta=output.with_suffix('.ffmeta')
    metadata(meta,cuts)
    vf='setpts='+pts_expression(SOURCE_CUTS,cuts).replace(',',r'\,')+',fps=30,format=yuv420p'
    run(['ffmpeg','-hide_banner','-y','-v','error','-i',str(source),'-f','ffmetadata','-i',str(meta),
         '-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-vf',vf,
         '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy',
         '-metadata:s:a:0','language=jpn','-movflags','+faststart','-t','22.5',str(output)])
    manifest={'source_cuts_frames':SOURCE_CUTS,'voice_safe_cuts_frames':cuts,
              'silences_seconds':spans,'limitation':'amplitude only; independent ASR and semantic sync not verified'}
    output.with_suffix('.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest


if __name__=='__main__':
    import sys
    if len(sys.argv)!=3: raise SystemExit('usage: voice_safe_cuts.py INPUT.mp4 OUTPUT.mp4')
    print(json.dumps(render(sys.argv[1],sys.argv[2]),ensure_ascii=False))
