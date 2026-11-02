#!/usr/bin/env python3
"""Offline chapter progress animation; original Japanese audio/captions preserved.
Review only. No posting, no third-party assets, no paid APIs.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw

GENRE_COLORS = {
    'ai': (76, 226, 211), 'business': (85, 188, 255),
    'money': (244, 203, 103), 'learning': (159, 150, 251),
    'health': (87, 222, 160), 'food': (255, 170, 107),
    'travel': (104, 206, 244), 'beauty': (250, 158, 194),
    'career': (127, 196, 248), 'life': (178, 220, 138),
}
FPS=30
BAR_X=78
BAR_Y=155
BAR_W=88
BAR_H=7
BAR_STEP=98
BAR_COUNT=8
OVERLAY_X=BAR_X-2
OVERLAY_Y=BAR_Y-2
OVERLAY_W=BAR_STEP*(BAR_COUNT-1)+BAR_W+4
OVERLAY_H=BAR_H+4

def cmd(args, binary=False):
    p=subprocess.run(args,capture_output=True,text=not binary)
    if p.returncode:
        err=p.stderr.decode(errors='replace') if binary else p.stderr
        raise RuntimeError(f'{args[0]} failed: {err[-1300:]}')
    return p.stdout

def probe(path):
    return json.loads(cmd(['ffprobe','-v','error','-show_streams',
                           '-show_chapters','-show_format','-of','json',str(path)]))

def chapter_index(t, chapters):
    for i,c in enumerate(chapters):
        if t < float(c['end_time'])-1e-9:
            return i
    return len(chapters)-1

def chapter_fraction(t, chapters):
    i=chapter_index(t,chapters)
    c=chapters[i]
    start,end=float(c['start_time']),float(c['end_time'])
    return i,max(0.,min(1.,(t-start)/(end-start)))

def draw_progress(index, fraction, genre='ai'):
    if genre not in GENRE_COLORS: raise ValueError('unknown genre')
    if not (0 <= index < BAR_COUNT and 0 <= fraction <= 1):
        raise ValueError('invalid chapter progress')
    image=Image.new('RGBA',(OVERLAY_W,OVERLAY_H),(0,0,0,0))
    d=ImageDraw.Draw(image)
    x=2+index*BAR_STEP
    y=BAR_Y-OVERLAY_Y
    d.rectangle((x,y,x+BAR_W-1,y+BAR_H-1),fill=(18,53,62,255))
    n=max(1,round(BAR_W*fraction))
    c=GENRE_COLORS[genre]
    d.rectangle((x,y,x+n-1,y+BAR_H-1),fill=(*c,255))
    if 2 < n < BAR_W-1:
        d.rectangle((x+n-2,y,x+n-1,y+BAR_H-1),fill=(213,246,246,255))
    return image

def adts_sha(path):
    data=cmd(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),
              '-map','0:a:0','-c:a','copy','-f','adts','pipe:1'],binary=True)
    return hashlib.sha256(data).hexdigest()

def render(source, output, workdir, genre='ai', report=None):
    source,output,workdir=map(Path,(source,output,workdir))
    if not source.is_file() or source.resolve()==output.resolve():
        raise ValueError('source missing or same as output')
    if genre not in GENRE_COLORS: raise ValueError('unknown genre')
    info=probe(source)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    chapters=info['chapters']
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name']) != ('h264',1080,1920,'30/1','aac'):
        raise ValueError('requires H264 1080x1920 30fps AAC')
    if len(chapters)!=BAR_COUNT: raise ValueError('requires eight chapter marks')
    frames=int(v['nb_frames'])
    frame_dir=workdir/'progress_frames'
    frame_dir.mkdir(parents=True,exist_ok=True)
    for i in range(frames):
        idx,fraction=chapter_fraction((i+.5)/FPS,chapters)
        draw_progress(idx,fraction,genre).save(frame_dir/f'{i:04d}.png')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd(['ffmpeg','-hide_banner','-loglevel','error','-y',
         '-i',str(source),'-framerate',str(FPS),'-start_number','0',
         '-i',str(frame_dir/'%04d.png'),'-filter_complex',
         f'[0:v][1:v]overlay={OVERLAY_X}:{OVERLAY_Y}:format=auto:shortest=0:eof_action=repeat,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-map_chapters','0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-frames:v',str(frames),'-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart',str(output)])
    out=probe(output)
    ov=next(s for s in out['streams'] if s['codec_type']=='video')
    oa=next(s for s in out['streams'] if s['codec_type']=='audio')
    if (ov['width'],ov['height'],int(ov['nb_frames'])) != (1080,1920,frames):
        raise RuntimeError('geometry/frame count mismatch')
    if oa['codec_name']!='aac' or len(out['chapters'])!=BAR_COUNT:
        raise RuntimeError('audio/chapters mismatch')
    before,after=adts_sha(source),adts_sha(output)
    if before!=after: raise RuntimeError('AAC bitstream changed')
    cmd(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(output),
         '-map','0:v:0','-map','0:a:0','-f','null','-'])
    qa={'cycle':1225,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'output_bytes':output.stat().st_size,'genre':genre,'width':1080,'height':1920,
        'fps':FPS,'frames':frames,'duration_seconds':float(out['format']['duration']),
        'chapters':BAR_COUNT,'progress_roi':[BAR_X,BAR_Y,BAR_STEP*(BAR_COUNT-1)+BAR_W,BAR_H],
        'aac_adts_sha256':after,'aac_bitstream_identical':True,
        'full_decode':'PASS','independent_japanese_asr':'NOT VERIFIED',
        'caption_semantics_and_alignment':'NOT VERIFIED',
        'reference_video_v33':'NOT ACCESSIBLE',
        'source_asset_rights':'NOT VERIFIED',
        'smartphone_hardware_playback':'NOT VERIFIED',
        'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    if report:
        Path(report).write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for flag in ('source','output','workdir','report'):
        p.add_argument('--'+flag,required=True)
    p.add_argument('--genre',choices=list(GENRE_COLORS),default='ai')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.workdir,a.genre,a.report),ensure_ascii=False))
