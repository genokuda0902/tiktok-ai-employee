#!/usr/bin/env python3
"""Offline, review-only Japanese voice presence EQ for 10-genre vertical slide videos.

Burned captions and H.264 frames are preserved byte-for-byte via video stream copy.
No ASR, semantic approval, automatic posting, copyrighted music, or paid API.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

GENRES = ('ai','business','money','learning','health','food','travel',
          'beauty','career','life')
FILTER = 'highpass=f=80,equalizer=f=3200:t=q:w=1:g=1.3,volume=-0.5dB'


def command(*args):
    return subprocess.run(args, check=True, text=True, capture_output=True).stdout


def probe(path):
    return json.loads(command('ffprobe','-v','error','-show_streams',
                              '-show_format','-show_chapters','-of','json',str(path)))


def validate_source(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(p)
    data = probe(p)
    vs = [s for s in data['streams'] if s['codec_type']=='video']
    aud = [s for s in data['streams'] if s['codec_type']=='audio']
    if len(vs)!=1 or len(aud)!=1:
        raise ValueError('one video and one narration audio track required')
    v,a=vs[0],aud[0]
    if (int(v['width']),int(v['height']),v['r_frame_rate']) != (1080,1920,'30/1'):
        raise ValueError('source must be 1080x1920 at 30 fps')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('source audio must be AAC 48kHz')
    if float(data['format']['duration']) < 2:
        raise ValueError('source too short')
    return data


def render(source, output, genre='ai'):
    if genre not in GENRES:
        raise ValueError('unknown genre')
    src,dst=Path(source),Path(output)
    if src.resolve()==dst.resolve() or dst.exists():
        raise ValueError('never overwrite input or existing output')
    before=validate_source(src)
    dst.parent.mkdir(parents=True,exist_ok=True)
    temp=dst.with_name(dst.stem+'.partial.mp4')
    if temp.exists():
        raise ValueError('partial output exists; inspect before retry')
    cmd=['ffmpeg','-nostdin','-hide_banner','-loglevel','error','-i',str(src),
         '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
         '-c:v','copy','-af',FILTER,'-c:a','aac','-b:a','160k','-ar','48000',
         '-ac','1','-movflags','+faststart',str(temp)]
    try:
        subprocess.run(cmd,check=True,capture_output=True,text=True)
        after=probe(temp)
        v0=next(s for s in before['streams'] if s['codec_type']=='video')
        v1=next(s for s in after['streams'] if s['codec_type']=='video')
        a1=next(s for s in after['streams'] if s['codec_type']=='audio')
        if v1['nb_frames']!=v0['nb_frames'] or (int(v1['width']),int(v1['height']))!=(1080,1920):
            raise RuntimeError('video geometry or frame count changed')
        if a1['codec_name']!='aac' or int(a1['sample_rate'])!=48000:
            raise RuntimeError('output narration codec mismatch')
        if abs(float(after['format']['duration'])-float(before['format']['duration']))>0.06:
            raise RuntimeError('duration changed by more than 60ms')
        temp.rename(dst)
    except BaseException:
        if temp.exists(): temp.unlink()
        raise
    return {'genre':genre,'filter':FILTER,'frames':int(v1['nb_frames']),
            'video_stream_copy':True,'chapters':len(after.get('chapters',[])),
            'independent_japanese_asr':False,'publication_approved':False}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=GENRES,default='ai')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))
