#!/usr/bin/env python3
"""Review-only image-first scene smooth-wipe transition renderer (10-genre reusable).

Uses ffmpeg slideleft xfade between *cloned edge frames*, so the timeline, Japanese audio,
existing lower-third captions and original cut timestamps remain intact.
No external uploads, AI impersonation, posting, or rights approvals occur.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

FPS = 30
CUTS = (3.2, 6.5, 9.8, 12.8, 24.3)
DURATION = 0.2  # 6 frames; 0.1 seconds on either side
GENRES = ('ai_work', 'romance', 'beauty', 'money', 'trivia', 'gadgets',
          'health', 'sales', 'travel', 'mystery')


def validate_cuts(cuts=CUTS, duration=DURATION, total=27.3, fps=FPS):
    if not cuts or len(GENRES) != 10 or len(set(GENRES)) != 10:
        raise ValueError('missing cuts or genre mismatch')
    if not (0 < duration <= 0.3):
        raise ValueError('transition must be short')
    if abs(duration * fps - round(duration * fps)) > 1e-7:
        raise ValueError('transition must align to frame boundary')
    if abs(duration * fps / 2 - round(duration * fps / 2)) > 1e-7:
        raise ValueError('half transition must align to frame boundary')
    if any(abs(c * fps - round(c * fps)) > 1e-7 for c in cuts):
        raise ValueError('cuts must align to frame boundary')
    if cuts != tuple(sorted(set(cuts))):
        raise ValueError('cuts must be strictly increasing')
    if cuts[0] <= duration or cuts[-1] >= total-duration:
        raise ValueError('transition outside timeline')
    if any(b-a <= duration for a, b in zip(cuts, cuts[1:])):
        raise ValueError('transitions overlap')
    return True


def filtergraph(cuts=CUTS, duration=DURATION, total=27.3, scale=None):
    """Return deterministic ffmpeg filter preserving cut centers and duration."""
    validate_cuts(cuts, duration, total)
    n = len(cuts)+1
    head = 'fps=30,format=yuv420p'
    if scale:
        w, h = scale
        if w*16 != h*9:
            raise ValueError('not 9:16')
        head = f'fps=30,scale={w}:{h}:flags=lanczos,format=yuv420p'
    f = [f'[0:v]{head},split={n}' + ''.join(f'[s{i}]' for i in range(n))]
    bounds = (0.0,) + tuple(cuts) + (total,)
    half = duration/2
    for i, (start, end) in enumerate(zip(bounds, bounds[1:])):
        pad = []
        if i:
            pad += ['start_mode=clone', f'start={round(half*FPS)}']
        if i < n-1:
            pad += ['stop_mode=clone', f'stop={round(half*FPS)}']
        f.append(f'[s{i}]trim=start={start:g}:end={end:g},setpts=PTS-STARTPTS,'
                 f'tpad={":".join(pad)},setpts=N/(30*TB),fps=30,settb=AVTB[v{i}]')
    prev = 'v0'
    for i, cut in enumerate(cuts, start=1):
        out = f'x{i}'
        f.append(f'[{prev}][v{i}]xfade=transition=slideleft:duration={duration:g}:'
                 f'offset={cut-half:g}[{out}]')
        prev = out
    f.append(f'[{prev}]format=yuv420p[v]')
    return ';'.join(f)


def render(source: Path, output: Path, genre: str, proxy=False, cuts=CUTS, duration=DURATION, total=27.3):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    if not source.is_file():
        raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    fg = filtergraph(cuts=tuple(cuts), duration=duration, total=total,
                     scale=(270,480) if proxy else None)
    cmd = ['ffmpeg','-hide_banner','-nostdin','-y','-loglevel','error',
           '-filter_complex_threads','2','-threads','2','-i',str(source),
           '-filter_complex',fg,'-map','[v]','-map','0:a:0',
           '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
           '-r','30','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=240)
    return cmd


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work')
    ap.add_argument('--proxy',action='store_true')
    ap.add_argument('--cuts',default=','.join(map(str,CUTS)),help='comma-separated scene cut seconds')
    ap.add_argument('--transition',type=float,default=DURATION)
    ap.add_argument('--total',type=float,default=27.3,help='video timeline duration, frame aligned')
    args=ap.parse_args()
    cuts=tuple(float(x) for x in args.cuts.split(','))
    cmd=render(args.source,args.output,args.genre,args.proxy,cuts,args.transition,args.total)
    print(json.dumps({'output':str(args.output),'cuts':cuts,'transition_seconds':args.transition,
                      'genre':args.genre,'command':cmd},ensure_ascii=False))

if __name__=='__main__':
    main()
