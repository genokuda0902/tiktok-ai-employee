"""Reproduce cycle871 MP4 from the locally delivered review package.

Inputs: assets/slide_01..08.png, source/browser_local_cycle866.mp4,
source/inherited_japanese_voice.m4a, work/captions.ass.
All sources are local; no APIs, uploads, merging, or posting.
Requires ffmpeg with libx264 and libass.
"""
from pathlib import Path
import subprocess, argparse
from quality_core import SCENES,CROP,DEST,validate_layout,validate_scenes

def render(root):
    root=Path(root)
    validate_layout();validate_scenes()
    manifest=root/'work'/'slides.ffconcat'
    manifest.parent.mkdir(parents=True,exist_ok=True)
    lines=['ffconcat version 1.0']
    for i,(a,b) in enumerate(SCENES,1):
        p=root/'assets'/f'slide_{i:02d}.png'
        if not p.exists():raise FileNotFoundError(p)
        lines.extend([f"file '{p.resolve().as_posix()}'",f'duration {b-a:.9f}'])
    lines.append(f"file '{(root/'assets'/'slide_08.png').resolve().as_posix()}'")
    manifest.write_text('\n'.join(lines)+'\n')
    browser=root/'source'/'browser_local_cycle866.mp4'
    voice=root/'source'/'inherited_japanese_voice.m4a'
    captions=root/'work'/'captions.ass'
    for p in (browser,voice,captions):
        if not p.exists():raise FileNotFoundError(p)
    cx,cy,cx1,cy1=CROP;dx,dy,dx1,dy1=DEST
    filters=(
        '[0:v]fps=30,scale=1080:1920:flags=lanczos,format=yuv420p[bg];'
        f'[1:v]crop={cx1-cx}:{cy1-cy}:{cx}:{cy},'
        f'scale={dx1-dx}:{dy1-dy}:flags=lanczos,setsar=1[ui];'
        f"[bg][ui]overlay={dx}:{dy}:enable='gte(t,8.45)*lt(t,17.25)':shortest=1[hybrid];"
        f"[hybrid]ass=filename='{captions.resolve().as_posix()}'[out]"
    )
    out=root/'output'/'cycle871_SAFE_FRAME_HOOK_JP_HUMAN_REVIEW.mp4'
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-y','-hide_banner','-loglevel','error',
        '-f','concat','-safe','0','-i',str(manifest),'-i',str(browser),
        '-i',str(voice),'-filter_complex',filters,'-map','[out]',
        '-map','2:a:0','-frames:v','691','-r','30',
        '-c:v','libx264','-preset','ultrafast','-crf','21','-threads','2',
        '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)],check=True)
    return out

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--root',required=True,help='Extracted cycle871 review package directory')
    print(render(p.parse_args().root))
