#!/usr/bin/env python3
"""Frame-exact, genre-neutral gentle Ken Burns motion for portrait slide shows.

No external images, network requests, uploads or posts. Motion is applied BEFORE
burned-in subtitles, so subtitle glyphs stay fixed and readable.
"""
from pathlib import Path
import json

FPS = 30
CUTS = (0, 60, 120, 180, 243, 282, 330, 378, 429)

def build_motion_expression(cuts=CUTS, amplitude=0.035):
    """Return FFmpeg zoompan expression with alternating slow push/pull per scene.

    Uses the filter's output frame index `on`; each scene is aligned to a
    declared frame boundary. Bounds: 1.0 <= zoom <= 1+amplitude.
    """
    if not (0 < amplitude <= .06):
        raise ValueError('amplitude must be in (0, 0.06]')
    if len(cuts)<2 or cuts[0]!=0 or any(b<=a for a,b in zip(cuts,cuts[1:])):
        raise ValueError('invalid scene boundaries')
    parts=[]
    for idx,(a,b) in enumerate(zip(cuts,cuts[1:])):
        span=max(1,b-a-1)
        prog=f'(on-{a})/{span}'
        if idx%2==0:
            val=f'1+{amplitude:.5f}*{prog}'
        else:
            val=f'1+{amplitude:.5f}*(1-{prog})'
        parts.append((b,val))
    expr=parts[-1][1]
    for end,val in reversed(parts[:-1]):
        expr=f'if(lt(on,{end}),{val},{expr})'
    return expr

def motion_filter(cuts=CUTS, amplitude=.035, fps=FPS):
    z=build_motion_expression(cuts,amplitude)
    return (f'fps={fps},zoompan=z=\'{z}\':x=\'(iw-iw/zoom)/2\':'
            f'y=\'(ih-ih/zoom)/2\':d=1:s=1080x1920:fps={fps}')

def verify_genres(config_path):
    data=json.loads(Path(config_path).read_text(encoding='utf-8'))
    genres=data['genres']
    names=[g['name'] for g in genres]
    if len(names)!=10 or len(set(names))!=10:
        raise ValueError('exactly ten unique genre configurations required')
    return names
