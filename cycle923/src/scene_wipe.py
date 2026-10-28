#!/usr/bin/env python3
"""Review-only 10-genre directional scene wipes for inherited image-first MP4s.

No media, secrets, posting, merge, network access, or paid APIs. Output is
HUMAN_REVIEW / PUBLICATION_NOT_APPROVED. The source MP4 is provided locally.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

GENRE_ACCENTS = {
    'ai_work': (216, 225, 52),
    'finance': (60, 190, 244),
    'health': (130, 208, 77),
    'travel': (110, 144, 251),
    'beauty': (183, 123, 247),
    'cooking': (70, 157, 255),
    'education': (220, 139, 117),
    'career': (235, 170, 82),
    'lifestyle': (210, 147, 193),
    'technology': (209, 202, 66),
}
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
DEFAULT_CUTS = (87, 174, 261, 348, 435, 522, 609)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def validate_settings(genre, cuts, duration_frames, protect_y, height, total_frames):
    if genre not in GENRE_ACCENTS:
        raise ValueError('Unknown genre')
    if not 3 <= duration_frames <= 12:
        raise ValueError('Wipe must last 3–12 frames')
    if not 100 <= protect_y < height:
        raise ValueError('Subtitle/footer protection out of range')
    if not cuts or tuple(cuts) != tuple(sorted(set(cuts))):
        raise ValueError('Cuts must be unique and increasing')
    if cuts[0] < 2 or cuts[-1] + duration_frames >= total_frames:
        raise ValueError('Cut exceeds video bounds')
    if any(b-a <= duration_frames for a,b in zip(cuts,cuts[1:])):
        raise ValueError('Wipes overlap')
    return True


def smoothstep(x):
    x = max(0.0, min(1.0, float(x)))
    return x*x*(3-2*x)


def reveal_fraction(step, duration_frames):
    if not 0 <= step < duration_frames:
        raise ValueError('step outside transition')
    return smoothstep((step + 1) / (duration_frames + 1))


def wipe_frame(incoming, outgoing, step, total, protect_y, accent_bgr):
    """Replace only upper portion; lower caption/footer pixels remain untouched."""
    import numpy as np
    h,w = incoming.shape[:2]
    if outgoing.shape != incoming.shape:
        raise ValueError('Frame dimensions differ')
    if not 0 < protect_y <= h:
        raise ValueError('Invalid caption boundary')
    pos = reveal_fraction(step,total)
    edge = pos * w
    soft = max(24.0, w*0.055)
    xx = np.arange(w,dtype=np.float32)[None,:]
    t = np.clip((edge + soft/2 - xx)/soft,0,1)
    alpha = (t*t*(3-2*t))[:,:,None]
    result = incoming.copy()
    a = incoming[:protect_y].astype(np.float32)
    b = outgoing[:protect_y].astype(np.float32)
    result[:protect_y] = np.clip(a*alpha + b*(1-alpha),0,255).astype(np.uint8)
    center = int(edge)
    x1,x2=max(0,center-3),min(w,center+3)
    if x2>x1:
        y1=min(150,protect_y)
        y2=max(y1,min(protect_y-80,1400))
        if y2>y1:
            strip = result[y1:y2,x1:x2]
            color = np.array(accent_bgr,dtype=np.float32).reshape(1,1,3)
            result[y1:y2,x1:x2] = np.clip(strip.astype(np.float32)*0.35 + color*0.65,0,255).astype(np.uint8)
    return result


def render(source, output, genre='ai_work', cuts=DEFAULT_CUTS,
           duration_frames=9, protect_y=1460, expected_source_sha=None):
    import cv2
    source,output=Path(source),Path(output)
    if not source.is_file() or source.stat().st_size < 100_000:
        raise RuntimeError('Source MP4 missing or too small')
    digest=sha256(source)
    if expected_source_sha and digest != expected_source_sha:
        raise RuntimeError(f'Source hash mismatch: expected {expected_source_sha}, got {digest}')
    cap=cv2.VideoCapture(str(source))
    fps=cap.get(cv2.CAP_PROP_FPS)
    width,height=int(cap.get(3)),int(cap.get(4))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if (width,height)!=(1080,1920) or abs(fps-30)>0.01 or count!=691:
        raise RuntimeError(f'Unexpected source geometry {width}x{height}, {fps}fps, {count} frames')
    validate_settings(genre,cuts,duration_frames,protect_y,height,count)
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.resolve()==source.resolve():
        raise RuntimeError('Source and output must differ')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-f','rawvideo','-pixel_format','bgr24','-video_size',f'{width}x{height}',
         '-framerate','30','-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','copy',
         '-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    last=None
    outgoing=None
    changed=0
    i=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if i in cuts:
                outgoing=last.copy()
            active=next((b for b in cuts if b<=i<b+duration_frames),None)
            if active is not None:
                frame=wipe_frame(frame,outgoing,i-active,duration_frames,protect_y,GENRE_ACCENTS[genre])
                changed+=1
            if active is None:
                last=frame
            if proc.stdin is None:raise RuntimeError('Encoder stdin unavailable')
            proc.stdin.write(frame.tobytes())
            i+=1
    except Exception:
        proc.kill()
        raise
    finally:
        cap.release()
        if proc.stdin:proc.stdin.close()
    err=proc.stderr.read().decode('utf-8','replace') if proc.stderr else ''
    ret=proc.wait()
    if ret!=0:
        raise RuntimeError(f'ffmpeg failed ({ret}): {err[-2000:]}')
    if i!=count or changed!=len(cuts)*duration_frames:
        raise RuntimeError(f'Frame count / transition mismatch: {i}, {changed}')
    return {'source':str(source),'output':str(output),'source_sha256':digest,
            'output_sha256':sha256(output),'genre':genre,'cuts':list(cuts),
            'duration_frames':duration_frames,'changed_frames':changed,
            'protected_y_start':protect_y,'policy':POLICY}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',choices=GENRE_ACCENTS,default='ai_work')
    p.add_argument('--expected-source-sha')
    p.add_argument('--report')
    args=p.parse_args()
    result=render(args.source,args.output,genre=args.genre,
                  expected_source_sha=args.expected_source_sha)
    if args.report:Path(args.report).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
