"""Review-only, genre-generic CTA accent and acoustic-presence QA.

The source is SHA-pinned and remains local. Never use this as evidence of
Japanese semantic ASR or publication approval. No network, paid service,
or private assets are committed to the repository.
"""
from __future__ import annotations
import argparse
from array import array
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import wave
from PIL import Image, ImageDraw, ImageFont

FPS = 30
PALETTES = {
    'ai_work':'#36d9dc','money':'#f1c267','career':'#75baf7',
    'business':'#6ed9ae','health':'#ffa09b','study':'#b7a5f8',
    'lifestyle':'#f5add4','technology':'#66d7fc','travel':'#ffcf8d',
    'mindset':'#a6e7be',
}
CTA_TEXT = '次は1つ試す'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# CTA appears in the previously empty top-right header area, away from all text.
CTA_X, CTA_Y, CTA_W, CTA_H = 510, 48, 365, 120
CAPTION_START_Y = 1490
DEFAULT_CHAPTERS = [0,2.9,5.8,8.533,12.667,14.3,17.333,20.3,23.033333]


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):
            h.update(b)
    return h.hexdigest()


def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError(f'{cmd[0]} failed {p.returncode}: {p.stderr[-1600:]}')
    return p.stdout


def validate_manifest(m):
    required={'genre','synthetic_scenario','review_only','rights_status',
              'contains_private_data','cta_text','start_seconds'}
    if set(m)!=required: raise ValueError('manifest fields missing/unknown')
    if m['genre'] not in PALETTES: raise ValueError('unsupported genre')
    if m['synthetic_scenario'] is not True or m['review_only'] is not True:
        raise ValueError('review-only fictional-data gate failed')
    if m['rights_status']!='unverified' or m['contains_private_data'] is not False:
        raise ValueError('asset/privacy gate failed; publication not authorized')
    if m['cta_text']!=CTA_TEXT: raise ValueError('unreviewed CTA text')
    if type(m['start_seconds']) not in (int,float) or not 21.8<=m['start_seconds']<=22.2:
        raise ValueError('CTA onset outside reviewed final scene')
    if CTA_X<500 or CTA_Y<20 or CTA_X+CTA_W>1080 or CTA_Y+CTA_H>175 or CTA_Y+CTA_H>=CAPTION_START_Y:
        raise ValueError('caption-safe CTA region violated')
    return True


def ease(t):
    t=max(0.0,min(1.0,t))
    return t*t*(3-2*t)


def rgba_color(h,a):
    h=h.lstrip('#')
    return tuple(int(h[i:i+2],16) for i in (0,2,4))+(int(a),)


def make_cta_frame(index,total,palette,scale=2):
    if not 0<=index<total or total<2: raise ValueError('invalid CTA frame')
    if palette not in PALETTES: raise ValueError('unknown genre')
    # 0.30-second appearance then sustained display; never covers subtitles.
    a=ease(min(1.0,index/9))
    im=Image.new('RGBA',(CTA_W*scale,CTA_H*scale),(0,0,0,0))
    d=ImageDraw.Draw(im)
    dy=round((1-a)*15*scale)
    d.rounded_rectangle((4*scale,(12+dy)*scale,(CTA_W-4)*scale,(CTA_H-12+dy)*scale),
                        radius=26*scale,fill=(4,34,49,round(238*a)),
                        outline=rgba_color(PALETTES[palette],round(250*a)),width=3*scale)
    # A small check/arrow mark is drawn geometrically: no external logo.
    d.ellipse((24*scale,(42+dy)*scale,59*scale,(77+dy)*scale),
              fill=rgba_color(PALETTES[palette],round(250*a)))
    d.line([(33*scale,(59+dy)*scale),(40*scale,(65+dy)*scale),
            (51*scale,(52+dy)*scale)],fill=(7,27,39,round(255*a)),width=4*scale)
    f=ImageFont.truetype(FONT,32*scale)
    d.text((73*scale,(35+dy)*scale),CTA_TEXT,font=f,
           fill=(246,251,253,round(255*a)),stroke_width=0)
    return im.resize((CTA_W,CTA_H),Image.Resampling.LANCZOS)


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def audio_adts_sha(path):
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'audio.aac'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),
             '-map','0:a:0','-c:a','copy','-f','adts',str(p)])
        return sha256(p)


def audit_acoustic_presence(path,chapters=DEFAULT_CHAPTERS,threshold=0.012):
    """A *signal* check, not speech recognition or word/meaning alignment."""
    with tempfile.TemporaryDirectory() as tmp:
        wav=Path(tmp)/'mono.wav'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(path),
             '-vn','-ac','1','-ar','16000',str(wav)])
        with wave.open(str(wav),'rb') as f:
            if f.getnchannels()!=1 or f.getsampwidth()!=2 or f.getframerate()!=16000:
                raise RuntimeError('unexpected PCM format')
            samples=array('h'); samples.frombytes(f.readframes(f.getnframes()))
    chunk=320
    rms=[]
    for start in range(0,len(samples)-chunk+1,chunk):
        rms.append(math.sqrt(sum(v*v for v in samples[start:start+chunk])/chunk)/32768)
    entries=[]
    for a,b in zip(chapters[:-1],chapters[1:]):
        z=rms[int(a/0.02):min(len(rms),int(b/0.02))]
        if not z: raise ValueError('chapter outside audio')
        active=[i for i,v in enumerate(z) if v>=threshold]
        if not active: raise RuntimeError(f'no detectable acoustic energy in {a:.2f}-{b:.2f}s')
        entries.append({'start':a,'end':b,'active_fraction':round(len(active)/len(z),3),
                        'first_active':round(a+active[0]*0.02,3),
                        'last_active':round(a+active[-1]*0.02,3),
                        'mean_rms':round(sum(z)/len(z),5)})
    return {'method':'20ms RMS amplitude gate (NOT ASR)', 'threshold':threshold,
            'segments':entries,'semantic_alignment':'NOT_VERIFIED',
            'phoneme_alignment':'NOT_VERIFIED'}


def render(source,out,expected_sha,m):
    validate_manifest(m)
    if len(expected_sha)!=64 or sha256(source)!=expected_sha:
        raise ValueError('source SHA256 mismatch; no output written')
    meta=probe(source)
    v=next((x for x in meta['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in meta['streams'] if x['codec_type']=='audio'),None)
    if not v or not a or (v.get('width'),v.get('height'))!=(1080,1920) or v.get('r_frame_rate')!='30/1':
        raise ValueError('requires vertical 1080x1920 30fps source with audio')
    if v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('requires H264/AAC source')
    frames=int(v['nb_frames']) if v.get('nb_frames') else round(float(meta['format']['duration'])*FPS)
    first=round(m['start_seconds']*FPS)
    total=frames-first
    if total<15 or total>42: raise ValueError('CTA duration outside approved window')
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for i in range(total):
            make_cta_frame(i,total,m['genre']).save(Path(tmp)/f'cta_{i:03d}.png')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-itsoffset',f'{first/FPS:.9f}','-framerate',str(FPS),'-start_number','0',
             '-i',str(Path(tmp)/'cta_%03d.png'),
             '-filter_complex',f'[0:v][1:v]overlay={CTA_X}:{CTA_Y}:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','18',
             '-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(frames),
             '-movflags','+faststart',str(out)])
    return {'source_sha256':expected_sha,'output_sha256':sha256(out),
            'source_adts_sha256':audio_adts_sha(source),'output_adts_sha256':audio_adts_sha(out),
            'first_changed_frame':first,'expected_last_frame':frames-1,'cta_frames':total}


def smoke():
    m={'genre':'ai_work','synthetic_scenario':True,'review_only':True,
       'rights_status':'unverified','contains_private_data':False,
       'cta_text':CTA_TEXT,'start_seconds':21.966667}
    with tempfile.TemporaryDirectory() as tmp:
        src=Path(tmp)/'synthetic.mp4'; out=Path(tmp)/'synthetic_out.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','lavfi','-i',
             'color=c=0x091a30:s=1080x1920:r=30:d=23.033333',
             '-f','lavfi','-i','sine=frequency=430:sample_rate=48000:duration=23.033333',
             '-c:v','libx264','-preset','ultrafast','-crf','32','-pix_fmt','yuv420p',
             '-c:a','aac','-shortest',str(src)])
        r=render(src,out,sha256(src),m)
        run(['ffmpeg','-hide_banner','-loglevel','error','-xerror','-i',str(out),'-f','null','-'])
        assert r['source_adts_sha256']==r['output_adts_sha256']
        print(json.dumps({'smoke':'PASS','sha256':r['output_sha256']},ensure_ascii=False))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source');p.add_argument('--source-sha');p.add_argument('--out')
    p.add_argument('--manifest');p.add_argument('--report');p.add_argument('--smoke',action='store_true')
    args=p.parse_args()
    if args.smoke: return smoke()
    if not all((args.source,args.source_sha,args.out,args.manifest)):
        p.error('source/source-sha/out/manifest required')
    m=json.loads(Path(args.manifest).read_text(encoding='utf-8'))
    result=render(args.source,args.out,args.source_sha,m)
    result['audio_presence']=audit_acoustic_presence(args.out)
    result['release_status']='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    if args.report: Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
