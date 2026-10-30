#!/usr/bin/env python3
"""Review-only caption panel refresh for 10 genre videos. No ASR claim or publication.

Replaces the previously burned caption strip with a readable two-line Japanese card.
Uses a human-authored SRT as text and timings; never infers speech meaning from audio.
"""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
REAL_SHA = '779db27ac4d0a0644d1d8f12d65a4766fafd0c6c6346b2eaa12e0d43795c5172'
W, H, FPS = 1080, 1920, 30
PANEL_Y, PANEL_H = 1490, 220
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SRT_TIME = re.compile(r'^(\d\d):(\d\d):(\d\d),(\d\d\d)$')

def run(cmd, binary=False):
    p = subprocess.run([str(x) for x in cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('failed: '+ ' '.join(map(str,cmd))+'\n'+p.stderr.decode(errors='replace')[-1500:])
    return p.stdout if binary else p.stdout.decode(errors='replace')

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for part in iter(lambda:f.read(1<<20),b''):h.update(part)
    return h.hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def stamp(s):
    m=SRT_TIME.fullmatch(s.strip())
    if not m: raise ValueError('bad SRT timestamp')
    h,mi,se,ms=map(int,m.groups())
    if mi>=60 or se>=60:raise ValueError('bad timestamp range')
    return h*3600+mi*60+se+ms/1000

def parse_srt(path):
    text=Path(path).read_text(encoding='utf-8-sig').replace('\r\n','\n').strip()
    cues=[]
    for block in re.split(r'\n\s*\n',text):
        rows=[x.strip() for x in block.split('\n') if x.strip()]
        if len(rows)<3 or not rows[0].isdigit() or ' --> ' not in rows[1]:raise ValueError('invalid SRT block')
        a,b=rows[1].split(' --> ')
        start,end=stamp(a),stamp(b)
        lines=rows[2:]
        if len(lines)!=2 or any(not 1<=len(x)<=34 for x in lines):raise ValueError('exactly two safe caption lines required')
        if start>=end or (cues and abs(start-cues[-1]['end'])>.04):raise ValueError('SRT gaps/overlaps')
        cues.append({'start':start,'end':end,'lines':lines})
    if not cues or abs(cues[0]['start'])>.04:raise ValueError('caption must start at 0')
    return cues

def card(lines,index,total):
    if len(lines)!=2:raise ValueError('two lines')
    im=Image.new('RGBA',(W,PANEL_H),(0,9,18,255))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((44,8,1036,210),radius=22,fill=(10,32,46,255),outline=(38,126,145,255),width=2)
    d.rounded_rectangle((62,24,71,194),radius=4,fill=(39,214,200,255))
    font=ImageFont.truetype(FONT,59)
    mini=ImageFont.truetype(FONT,20)
    for n,line in enumerate(lines):
        bbox=d.textbbox((0,0),line,font=font)
        if bbox[2]-bbox[0]>900:raise ValueError('caption clipped')
        d.text((94,47+n*72),line,font=font,fill=(247,252,255,255),stroke_width=1,stroke_fill=(12,33,44,255))
    d.text((855,18),f'{index:02d} / {total:02d}',font=mini,fill=(113,208,214,255))
    return im

def adts(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c:a','copy','-f','adts','-'],True)).hexdigest()

def validate(source,output,cues,genre,review_only,synthetic):
    source,output=Path(source).resolve(),Path(output).resolve()
    if not review_only or genre not in GENRES or source==output or output.exists() or not source.is_file():raise ValueError('review-only/genre/file gate')
    info=probe(source)
    streams=info['streams']
    if len(streams)!=2:raise ValueError('exactly one video and one audio stream')
    v=next((x for x in streams if x['codec_type']=='video'),{})
    a=next((x for x in streams if x['codec_type']=='audio'),{})
    if (v.get('codec_name'),v.get('width'),v.get('height'),v.get('r_frame_rate'))!=('h264',W,H,'30/1'):raise ValueError('video format')
    if (a.get('codec_name'),a.get('sample_rate'),a.get('tags',{}).get('language'))!=('aac','48000','jpn'):raise ValueError('audio format')
    duration=float(info['format']['duration'])
    if abs(cues[-1]['end']-duration)>.045:raise ValueError('caption duration mismatch')
    if synthetic:
        if source.name!='synthetic_input.mp4' or duration>3.1:raise ValueError('synthetic-only CI gate')
    elif genre!='ai_work' or sha(source)!=REAL_SHA or len(cues)!=8:raise ValueError('unapproved real source or caption count')
    return info

def render(source,output,srt,report,genre,synthetic):
    cues=parse_srt(srt)
    validate(source,output,cues,genre,True,synthetic)
    with tempfile.TemporaryDirectory(prefix='caption_panel_') as tmp:
        tmp=Path(tmp)
        lines=[]
        for i,cue in enumerate(cues,1):
            name=f'cue_{i:02d}.png'
            card(cue['lines'],i,len(cues)).save(tmp/name)
            lines.append(f"file '{(tmp/name).as_posix()}'")
            lines.append(f"duration {cue['end']-cue['start']:.6f}")
        lines.append(f"file '{(tmp/f'cue_{len(cues):02d}.png').as_posix()}'")
        listing=tmp/'overlay.ffconcat'
        listing.write_text('\n'.join(lines)+'\n',encoding='utf-8')
        filtergraph=f'[1:v]fps={FPS},format=yuva420p[panel];[0:v][panel]overlay=0:{PANEL_Y}:shortest=1:format=auto[v]'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,'-f','concat','-safe','0','-i',listing,
             '-filter_complex',filtergraph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast',
             '-crf','23','-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart',output])
    run(['ffmpeg','-v','error','-xerror','-i',output,'-map','0:v:0','-f','null','-','-map','0:a:0','-f','null','-'])
    after=probe(output)
    frames=int(next(x for x in after['streams'] if x['codec_type']=='video')['nb_frames'])
    original=int(next(x for x in probe(source)['streams'] if x['codec_type']=='video')['nb_frames'])
    if frames!=original:raise AssertionError(f'frame mismatch {frames} vs {original}')
    if adts(source)!=adts(output):raise AssertionError('AAC payload changed')
    result={'input_sha256':sha(source),'output_sha256':sha(output),'genre':genre,
      'resolution':[W,H],'fps':FPS,'frames':frames,'duration':float(after['format']['duration']),
      'audio_codec':'aac','audio_sample_rate':48000,'audio_language':'jpn','audio_payload_unchanged':True,
      'subtitle_source':'existing human-authored SRT, not ASR','subtitle_cues':len(cues),
      'subtitle_visual':'redesigned caption panel, no selectable subtitle track','full_decode':'PASS',
      'japanese_speech_semantic_sync':'NOT_VERIFIED','v33_reference_mp4':'NOT_ACCESSED',
      'rights':'NOT_VERIFIED','publication':'NOT_APPROVED'}
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def main():
    ap=argparse.ArgumentParser()
    for name in ('source','output','srt','report'):ap.add_argument('--'+name,required=True)
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--review-only',action='store_true')
    ap.add_argument('--synthetic-ci',action='store_true');a=ap.parse_args()
    if not a.review_only:raise ValueError('must explicitly request review-only')
    print(json.dumps(render(a.source,a.output,a.srt,a.report,a.genre,a.synthetic_ci),ensure_ascii=False))
if __name__=='__main__':main()
