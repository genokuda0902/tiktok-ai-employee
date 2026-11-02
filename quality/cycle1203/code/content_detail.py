#!/usr/bin/env python3
"""Free, offline contrast-adaptive detail recovery for TikTok portrait slides.

Only the central information panel is sharpened; burned-in Japanese narration,
progress rail, branding/footer, and TikTok-safe regions are not edited.
All input footage stays local; never posts, purchases, or merges.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

GENRE_PROFILES = {
    'ai': 0.30, 'business': 0.28, 'money': 0.28,
    'learning': 0.30, 'health': 0.24, 'food': 0.24,
    'travel': 0.24, 'beauty': 0.22, 'career': 0.28,
    'life': 0.25,
}
FPS = 30
DEFAULT_ROI = (72, 390, 936, 860)

def probe(path):
    p = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],
                       capture_output=True,text=True,check=True)
    return json.loads(p.stdout)

def validate_source(info):
    v = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in info['streams'] if s['codec_type'] == 'audio'), None)
    if v is None or a is None:
        raise ValueError('Input requires video and audio')
    if (int(v['width']),int(v['height']),v['r_frame_rate']) != (1080,1920,'30/1'):
        raise ValueError('Input must be 1080x1920 at 30fps')
    if a['codec_name'] != 'aac':
        raise ValueError('AAC audio required for lossless packet copy')
    return int(v.get('nb_frames') or round(float(info['format']['duration'])*FPS))

def validate_roi(roi):
    if len(roi) != 4 or any(not isinstance(i,int) for i in roi):
        raise ValueError('ROI must contain four integers')
    x,y,w,h = roi
    if x < 48 or x+w > 1024 or y < 320 or y+h > 1300 or w < 200 or h < 150:
        raise ValueError('ROI must stay in central content panel, excluding captions and UI safe areas')
    if w%2 or h%2 or x%2 or y%2:
        raise ValueError('ROI dimensions and offsets must be even for yuv420p')
    return tuple(roi)

def build_filter(roi, strength):
    x,y,w,h=validate_roi(roi)
    if not 0.15 <= strength <= 0.45:
        raise ValueError('CAS strength outside tested mild range')
    return (f'[0:v]split=2[original][detail];'
            f'[detail]crop={w}:{h}:{x}:{y},cas=strength={strength:.3f}[enhanced];'
            f'[original][enhanced]overlay={x}:{y}:format=auto:shortest=1[outv]')

def render(src,dst,genre='ai',roi=DEFAULT_ROI,frames=None,crf=16):
    if genre not in GENRE_PROFILES: raise ValueError('Unknown genre')
    total=validate_source(probe(src))
    if frames is not None:
        if not 1 <= frames <= total: raise ValueError('Invalid test frame count')
        total=frames
    if not 14 <= crf <= 22: raise ValueError('CRF outside safe range')
    strength=GENRE_PROFILES[genre]
    filt=build_filter(roi,strength)
    dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
         '-filter_complex',filt,'-map','[outv]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf',str(crf),'-pix_fmt','yuv420p',
         '-r',str(FPS),'-fps_mode','cfr','-c:a','copy','-frames:v',str(total),
         '-movflags','+faststart','-metadata:s:a:0','language=jpn',str(dst)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError('FFmpeg render error: '+p.stderr[-2000:])
    return {'genre':genre,'roi':list(roi),'cas_strength':strength,'expected_frames':total,'output':str(dst)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('source');ap.add_argument('output')
    ap.add_argument('--genre',choices=sorted(GENRE_PROFILES),default='ai')
    ap.add_argument('--roi',default=','.join(map(str,DEFAULT_ROI)))
    ap.add_argument('--frames',type=int,default=None)
    ap.add_argument('--crf',type=int,default=16)
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,tuple(map(int,args.roi.split(','))),args.frames,args.crf),ensure_ascii=False))

if __name__=='__main__':main()
