#!/usr/bin/env python3
"""Review-only, source-pinned result-first hook for ten genres.

Shows a compact proof badge in the unused scene-progress panel, not over
captions, main artwork, or private material. It never posts or uploads media.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = {'ai':'#32d9d3','business':'#51c7f4','money':'#eac56c',
          'learning':'#8fc4ff','health':'#79d7ab','food':'#f3bd79',
          'travel':'#80c8e8','beauty':'#efafd2','career':'#93a5ff',
          'life':'#a7dfb0'}
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
WIDTH,HEIGHT,FPS=1080,1920,30
ROI=(52,1305,844,82)
CAPTION_START=1480
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def probe(path):
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    a=next(x for x in info['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['r_frame_rate']) != ('h264',WIDTH,HEIGHT,'30/1'):
        raise ValueError('H264 1080x1920 30fps required')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('AAC 48kHz narration required')
    return float(info['format']['duration']),int(v.get('nb_frames') or 0)

def check(manifest,source,duration):
    if manifest.get('policy')!=POLICY or manifest.get('genre') not in GENRES:
        raise ValueError('Policy/genre fail closed')
    if manifest.get('source_sha256')!=sha256(source):
        raise ValueError('Unpinned source')
    if manifest.get('asset_approval')!='review_only_no_publication':
        raise ValueError('Unapproved or unsafe asset policy')
    if manifest.get('manual_post_only') is not True:
        raise ValueError('Posting must remain manual')
    proof=manifest.get('proof_text')
    if not isinstance(proof,str) or not 1<=len(proof)<=32 or '\n' in proof:
        raise ValueError('Proof text length/format')
    numbers=manifest.get('proof_numbers')
    if numbers is not None and (not isinstance(numbers,list) or len(numbers)!=3 or
        any(type(x) is not int or x<0 for x in numbers) or numbers[0]+numbers[1]!=numbers[2]):
        raise ValueError('Inconsistent source numbers')
    times=manifest.get('window')
    if not isinstance(times,list) or len(times)!=2 or any(type(t) not in (int,float) for t in times):
        raise ValueError('Invalid window')
    start,end=times
    if not (0.05<=start<0.5 and 1.0<=end<=1.6 and end<=duration):
        raise ValueError('Hook must be within opening 1.6s')
    x,y,w,h=ROI
    if x<0 or y<0 or x+w>WIDTH or y+h>=CAPTION_START:
        raise ValueError('Caption overlap')
    font=ImageFont.truetype(FONT,43)
    bb=font.getbbox(proof)
    if bb[2]-bb[0]>w-280:
        raise ValueError('Proof too wide for mobile')
    return start,end

def make_overlay(manifest,path):
    _,_,w,h=ROI
    im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im)
    accent=GENRES[manifest['genre']]
    d.rounded_rectangle((2,2,w-3,h-3),radius=17,fill=(3,28,43,248),outline=accent,width=3)
    d.rounded_rectangle((10,10,215,h-10),radius=12,fill=(4,68,77,255))
    label_font=ImageFont.truetype(FONT,27)
    d.text((24,18),'結果を先出し',font=label_font,fill='#d4fbfb')
    proof_font=ImageFont.truetype(FONT,43)
    proof=manifest['proof_text']
    bbox=d.textbbox((0,0),proof,font=proof_font)
    tw=bbox[2]-bbox[0]
    d.text((238+(w-250-tw)//2,8),proof,font=proof_font,fill='#ffffff',stroke_width=1,stroke_fill=accent)
    im.save(path)
    return path

def render(source,output,manifest_path,workdir=None):
    source,output=Path(source),Path(output)
    duration,frames=probe(source)
    manifest=json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    start,end=check(manifest,source,duration)
    workdir=Path(workdir) if workdir else output.parent
    workdir.mkdir(parents=True,exist_ok=True)
    overlay=make_overlay(manifest,workdir/'proof_first_overlay.png')
    fadein=0.14; fadeout=0.18
    vf=(f'[1:v]format=rgba,fade=t=in:st={start:.3f}:d={fadein:.3f}:alpha=1,'
        f'fade=t=out:st={end-fadeout:.3f}:d={fadeout:.3f}:alpha=1[proof];'
        f'[0:v][proof]overlay={ROI[0]}:{ROI[1]}:format=auto:'
        f"enable='between(t,{start:.3f},{end:.3f})'[v]")
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-loop','1','-framerate',str(FPS),'-i',str(overlay),
         '-filter_complex',vf,'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-threads','2',
         '-pix_fmt','yuv420p','-frames:v',str(frames or round(duration*FPS)),
         '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    oduration,oframes=probe(output)
    if frames and frames!=oframes:raise RuntimeError('Frame count changed')
    if abs(duration-oduration)>0.06:raise RuntimeError('Duration changed')
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'duration':oduration,'frames':oframes,'genre':manifest['genre'],
            'window':[start,end],'policy':POLICY,'source_media_uploaded':False}

def main():
    p=argparse.ArgumentParser()
    for name in ('source','output','manifest','report'):p.add_argument('--'+name,required=True)
    args=p.parse_args()
    result=render(args.source,args.output,args.manifest)
    Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))
if __name__=='__main__':main()
