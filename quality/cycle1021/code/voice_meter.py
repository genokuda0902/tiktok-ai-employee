#!/usr/bin/env python3
"""Audio-reactive VOICE meter for Japanese 1080x1920 slideshow MP4.

No network calls, no ASR, no publishing. Copies original AAC stream and chapters.
"""
from __future__ import annotations
import argparse
from array import array
import json
import math
from pathlib import Path
import subprocess
import sys

GENRE_COLORS = {
    'ai_work': (31, 218, 202),                # AI・仕事効率化
    'beauty': (246, 137, 172),                # 美容・身だしなみ
    'romance_psychology': (178, 146, 244),    # 恋愛・心理
    'money_saving': (234, 194, 83),           # お金・節約
    'sales_business': (91, 183, 255),         # 営業・ビジネス
    'career': (99, 214, 223),                 # 転職・キャリア
    'health_lifestyle': (88, 215, 147),       # 健康・生活改善
    'science_trivia': (223, 166, 255),        # 雑学・科学
    'travel_food': (245, 164, 85),            # 旅行・グルメ
    'product_comparison_lifestyle': (85, 194, 245), # 商品比較・暮らし
}
PATCH_X, PATCH_Y, PATCH_W, PATCH_H = 574, 73, 145, 36
BAR_COUNT, FPS = 8, 30

def probe(path):
    return json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_streams','-show_format','-show_chapters',
        '-of','json',str(path)], text=True))

def audio_rms(path, n_frames, fps=FPS):
    """Decode mono audio; RMS per 1/30 second; pad last AAC gap with zeros."""
    pcm = subprocess.check_output(['ffmpeg','-v','error','-i',str(path),
        '-map','0:a:0','-f','s16le','-ac','1','-ar',str(fps*1600),'-'])
    a = array('h'); a.frombytes(pcm)
    if sys.byteorder != 'little': a.byteswap()
    out = []
    for i in range(n_frames):
        seg = a[i*1600:(i+1)*1600]
        out.append(math.sqrt(sum(v*v for v in seg)/len(seg))/32768 if seg else 0.0)
    return out

def levels(rms):
    """Noise gate + fast attack / moderate release; no semantic ASR claim."""
    smoothed = 0.0
    out = []
    for x in rms:
        db = 20*math.log10(max(x, 1e-7))
        target = max(0.0, min(1.0, (db+49.0)/36.0))
        alpha = 0.65 if target > smoothed else 0.45
        smoothed += alpha*(target-smoothed)
        out.append(smoothed)
    return out

def make_patch(level, index, color):
    """Small RGB24 overlay, Python standard library only."""
    w,h = PATCH_W,PATCH_H
    buf = bytearray(w*h*3)
    for y in range(h):
        for x in range(w):
            p = (y*w+x)*3
            buf[p:p+3] = bytes((0, 1, 22 + (x//55)))
    for bar in range(BAR_COUNT):
        x0 = 7+bar*17
        shape = (0.82,1.00,0.92,0.74,0.96,0.86,0.78,0.90)[bar]
        height = max(2, round(2 + 24*level*shape))
        y1 = 31
        y0 = y1-height
        for y in range(y0,y1):
            for x in range(x0,x0+7):
                p=(y*w+x)*3
                f = 0.78 if y in (y0,y1-1) else 1.0
                buf[p:p+3] = bytes(min(255,int(v*f)) for v in color)
            for x in (x0-1,x0+7):
                p=(y*w+x)*3
                buf[p:p+3] = bytes(min(255,int(v*0.27)) for v in color)
    return buf

def render(source, target, genre='ai_work', ffmpeg='ffmpeg'):
    if genre not in GENRE_COLORS: raise ValueError('unknown genre: '+genre)
    meta = probe(source)
    vid = next(s for s in meta['streams'] if s['codec_type']=='video')
    aud = [s for s in meta['streams'] if s['codec_type']=='audio']
    if (vid['width'],vid['height']) != (1080,1920):
        raise ValueError('1080x1920 source required')
    if not aud: raise ValueError('audio stream required')
    frn,frd = map(int,vid['r_frame_rate'].split('/'))
    if (frn,frd)!=(30,1): raise ValueError('30fps source required')
    n = int(vid.get('nb_frames') or round(float(meta['format']['duration'])*FPS))
    rms = audio_rms(source,n)
    lev = levels(rms)
    cmd = [ffmpeg,'-hide_banner','-loglevel','error','-y',
           '-i',str(source),'-f','rawvideo','-pixel_format','rgb24',
           '-video_size',f'{PATCH_W}x{PATCH_H}', '-framerate',str(FPS),
           '-i','pipe:0',
           '-filter_complex',f'[0:v:0][1:v:0]overlay={PATCH_X}:{PATCH_Y}:shortest=1,format=yuv420p[v]',
           '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
           '-c:v','libx264','-preset','veryfast','-crf','17','-pix_fmt','yuv420p',
           '-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(target)]
    proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i,l in enumerate(lev):
            proc.stdin.write(make_patch(l,i,GENRE_COLORS[genre]))
        proc.stdin.close()
        err=proc.stderr.read().decode('utf-8',errors='replace')
        rc=proc.wait()
    except Exception:
        proc.kill(); proc.wait(); raise
    if rc: raise RuntimeError('FFmpeg failed: '+err[-2500:])
    return {'frames':n,'genre':genre,'rms_mean':round(sum(rms)/len(rms),5),
            'level_mean':round(sum(lev)/len(lev),5),
            'meter_patch':[PATCH_X,PATCH_Y,PATCH_W,PATCH_H]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('target',type=Path)
    p.add_argument('--genre',choices=GENRE_COLORS,default='ai_work')
    p.add_argument('--stats',type=Path)
    args=p.parse_args()
    result=render(args.source,args.target,args.genre)
    if args.stats: args.stats.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':main()
