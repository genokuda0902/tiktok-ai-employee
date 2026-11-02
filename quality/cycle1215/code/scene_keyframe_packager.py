#!/usr/bin/env python3
"""10-genre, free, review-only scene-aligned H264 MP4 packaging.

Preserve original Japanese AAC audio and chapter metadata; put keyframes on
editorial scene starts for mobile seeking. No cloud APIs or publishing.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
WIDTH, HEIGHT, FPS = 1080, 1920, 30
DEFAULT_BOUNDARIES = (42,96,171,252,333,414,501,579)

def run(args):
    p = subprocess.run(args, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(f'{args[0]} failed ({p.returncode}): {p.stderr[-1500:]}')
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(path)]))

def video_audio(meta):
    v = next((s for s in meta['streams'] if s['codec_type']=='video'), None)
    a = next((s for s in meta['streams'] if s['codec_type']=='audio'), None)
    if not v or not a:
        raise ValueError('Input must contain video and audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['r_frame_rate']) != ('h264',WIDTH,HEIGHT,'30/1'):
        raise ValueError('Input must be H264 1080x1920 30fps')
    if a['codec_name'] != 'aac' or int(a['sample_rate']) != 48000:
        raise ValueError('Input must have AAC 48kHz audio')
    return v,a

def validate(boundaries, frames, genre):
    if genre not in GENRES: raise ValueError('Unsupported genre')
    if frames < 2*FPS: raise ValueError('Video too short')
    if not boundaries or any(type(b) is not int for b in boundaries):
        raise ValueError('Boundaries must be integers')
    if tuple(sorted(set(boundaries))) != tuple(boundaries):
        raise ValueError('Boundaries must be unique and ascending')
    if boundaries[0] <= 0 or boundaries[-1] >= frames-1:
        raise ValueError('Boundaries must be inside video')
    return True

def keyframes(path):
    j=json.loads(run(['ffprobe','-v','error','-select_streams','v:0','-skip_frame','nokey',
                      '-show_frames','-show_entries','frame=best_effort_timestamp_time','-of','json',str(path)]))
    return [float(f['best_effort_timestamp_time']) for f in j['frames']]

def verify_keyframes(times, boundaries, fps=FPS):
    for b in boundaries:
        t=b/fps
        if not any(abs(k-t) <= 0.5/fps for k in times):
            raise ValueError(f'Missing scene-aligned keyframe at {t:.3f}s')
    return True

def has_faststart(path):
    data=Path(path).read_bytes()
    moov,mdat=data.find(b'moov'),data.find(b'mdat')
    return moov>0 and mdat>0 and moov<mdat

def render(source, output, boundaries=DEFAULT_BOUNDARIES, genre='ai', crf=19, preset='slow'):
    source,output=Path(source),Path(output)
    if source.resolve()==output.resolve(): raise ValueError('Never overwrite source')
    meta=probe(source)
    v,a=video_audio(meta)
    frames=int(v.get('nb_frames',0))
    validate(boundaries,frames,genre)
    if not 16<=crf<=23 or preset not in ('medium','slow'):
        raise ValueError('Quality settings out of approved range')
    output.parent.mkdir(parents=True,exist_ok=True)
    t=','.join(f'{b/FPS:.6f}' for b in boundaries)
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
         '-c:v','libx264','-preset',preset,'-crf',str(crf),'-pix_fmt','yuv420p',
         '-g','90','-keyint_min','15','-force_key_frames',t,'-fps_mode','passthrough',
         '-c:a','copy','-movflags','+faststart',str(output)])
    om=probe(output)
    ov,oa=video_audio(om)
    if int(ov.get('nb_frames',0))!=frames: raise RuntimeError('Frame count changed')
    if abs(float(om['format']['duration'])-float(meta['format']['duration']))>1/FPS:
        raise RuntimeError('Duration changed')
    kf=keyframes(output)
    verify_keyframes(kf,boundaries)
    if not has_faststart(output): raise RuntimeError('Missing faststart')
    if len(om.get('chapters',[]))!=len(meta.get('chapters',[])):
        raise RuntimeError('Chapter metadata count changed')
    return {'genre':genre,'source_bytes':source.stat().st_size,'output_bytes':output.stat().st_size,
            'reduction_percent':round(100*(1-output.stat().st_size/source.stat().st_size),3),
            'frames':frames,'keyframes_s':kf,'scene_starts_s':[b/FPS for b in boundaries],
            'chapter_count':len(om.get('chapters',[])),'faststart':True,
            'audio_codec':oa['codec_name'],'audio_rate':int(oa['sample_rate']),'review_only':True}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--boundaries',default=','.join(map(str,DEFAULT_BOUNDARIES)))
    ap.add_argument('--genre',choices=GENRES,default='ai')
    ap.add_argument('--crf',type=int,default=19)
    ap.add_argument('--preset',choices=['medium','slow'],default='slow')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,tuple(map(int,args.boundaries.split(','))),
                            args.genre,args.crf,args.preset),ensure_ascii=False,indent=2))
