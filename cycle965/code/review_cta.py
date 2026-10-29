"""Zero-cost original bookmark CTA for Japanese review-only image-slide MP4.
Source audio and existing burned captions are retained. No external media, posting or paid APIs.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRE_COLORS = {
    'ai_work':'#35d4c5','business':'#76baff','finance':'#e5bb69',
    'education':'#f3ac75','career':'#9bb8ff','wellness':'#87d4a1',
    'lifestyle':'#e7a6cd','technology':'#5ac5e8','travel':'#e2b98e',
    'trivia':'#c7a5f0'
}
REVIEWED_GENRES={'ai_work'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
CTA='保存'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def run(cmd, timeout=240, capture=False):
    p=subprocess.run(cmd, stdout=subprocess.PIPE if capture else subprocess.DEVNULL,
                     stderr=subprocess.PIPE,timeout=timeout,check=False)
    if p.returncode: raise RuntimeError(p.stderr.decode(errors='replace')[-3000:])
    return p.stdout if capture else None

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],capture=True))

def check_input(info,genre):
    if genre not in GENRE_COLORS: raise ValueError('Unknown genre')
    if genre not in REVIEWED_GENRES: raise PermissionError('Genre has no approved visual placement')
    v=next((s for s in info['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if not v or not a: raise ValueError('Both video and audio required')
    if (v['width'],v['height'],v['r_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Only 1080x1920 30fps source reviewed')
    if a['codec_name']!='aac' or int(a['sample_rate'])!=48000:
        raise ValueError('AAC 48kHz source required')
    duration=float(info['format']['duration'])
    if not 22.9<=duration<=23.1:raise ValueError('Source duration not reviewed')
    return duration

def build_overlay(path, genre='ai_work'):
    if genre not in GENRE_COLORS:raise ValueError('Unknown genre')
    if genre not in REVIEWED_GENRES:raise PermissionError('Unreviewed genre')
    w,h=68,112
    im=Image.new('RGBA',(w,h),(0,0,0,0));d=ImageDraw.Draw(im)
    d.rounded_rectangle((3,3,w-4,h-4),radius=15,fill=(4,33,55,248),outline=(64,205,203,240),width=2)
    d.rounded_rectangle((10,12,58,67),radius=12,fill=(21,70,87,255))
    d.line([(22,24),(22,57),(34,48),(46,57),(46,24),(22,24)],fill=(91,237,221,255),width=4,joint='curve')
    f=ImageFont.truetype(FONT,21)
    d.text((13,75),CTA,font=f,fill=(255,255,255,255))
    im.save(path)
    return im

def render(src,dst,report,genre='ai_work'):
    src,dst,report=map(Path,(src,dst,report));dst.parent.mkdir(parents=True,exist_ok=True)
    duration=check_input(probe(src),genre)
    with tempfile.TemporaryDirectory() as tmp:
        overlay=Path(tmp)/'cta.png';build_overlay(overlay,genre)
        filt='[1:v]format=rgba,fade=t=in:st=20.85:d=0.38:alpha=1[cta];[0:v][cta]overlay=x=79:y=1430:format=auto:shortest=1[v]'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),
             '-loop','1','-framerate','30','-i',str(overlay),
             '-filter_complex',filt,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','19',
             '-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn',
             '-movflags','+faststart','-t',f'{duration:.6f}',str(dst)],timeout=300)
    data={'source_sha256':sha256(src),'output_sha256':sha256(dst),
          'genre':genre,'cta_text':CTA,'cta_start_s':20.85,'fade_in_s':.38,
          'cta_bbox':[79,1430,147,1542], 'audio_copy':True,
          'review_only':True,'publish_approved':False,
          'external_assets':False,'auto_posting':False}
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--report',required=True);ap.add_argument('--genre',default='ai_work')
    a=ap.parse_args();print(json.dumps(render(a.input,a.output,a.report,a.genre),ensure_ascii=False))

if __name__=='__main__':main()
