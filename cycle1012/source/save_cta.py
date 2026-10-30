#!/usr/bin/env python3
"""Review-only end-card save CTA. Reimplementation, not recovered v33 source.

Never posts, uploads, merges, or authorizes any asset. Only exact local AI-work
source may be rendered; genre copy presets are NOT publication approvals.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path

GENRE_CTA = {
    'ai_work':'保存して、明日1つ試す',
    'business':'保存して、次の仕事で試す',
    'money':'保存して、数字を確認する',
    'learning':'保存して、復習に使う',
    'health':'保存して、情報源を確認',
    'life':'保存して、あとで試す',
    'travel':'保存して、旅の準備に',
    'food':'保存して、次の献立に',
    'tech':'保存して、設定を確認',
    'history':'保存して、あとで調べる',
}
APPROVED_LOCAL_GENRE='ai_work'
SOURCE_SHA='20e0840d790b458e7a3a406fc3e76b5288fff54ba2c4ccaa0fb4ea6d63cd58ef'
FPS=30
START_FRAME=630  # 21.0 s; the final scene begins at about 20.3 s
TOTAL_FRAMES=691
OVERLAY_Y=1188
OVERLAY_H=100
CAPTION_SAFE_Y=1490
REVIEW_BANNER_Y=1290


def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def command(args):
    p=subprocess.run([str(a) for a in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError('command failed: '+' '.join(map(str,args))+'\n'+p.stderr[-1600:])
    return p.stdout


def probe(path):
    return json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))


def fade(frame):
    t=(frame-START_FRAME)/FPS
    if t<0:return 0.
    if t<.35:
        x=t/.35
        return x*x*(3-2*x)
    return 1.


def validate(source,output,genre,review_only,expected_sha=SOURCE_SHA):
    if genre not in GENRE_CTA:raise ValueError('unknown genre')
    if genre!=APPROVED_LOCAL_GENRE or not review_only:raise ValueError('private review approval missing')
    source,output=Path(source).resolve(),Path(output).resolve()
    if not source.is_file() or source==output or output.exists():raise ValueError('invalid source/output')
    if expected_sha!=SOURCE_SHA or sha(source)!=SOURCE_SHA:raise ValueError('source SHA mismatch')
    ss=probe(source)['streams']
    if len(ss)!=2 or [s['codec_type'] for s in ss]!=['video','audio']:
        raise ValueError('expected video and Japanese audio only')
    v,a=ss
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('video format mismatch')
    if (a['codec_name'],a['sample_rate'],a.get('tags',{}).get('language'))!=('aac','48000','jpn'):
        raise ValueError('audio format mismatch')
    return True


def draw(path,frame,genre,font_path):
    from PIL import Image,ImageDraw,ImageFont
    opacity=fade(frame)
    im=Image.new('RGBA',(1080,OVERLAY_H),(0,0,0,0))
    if opacity<=0:
        im.save(path);return
    d=ImageDraw.Draw(im,'RGBA')
    a=lambda v:int(round(v*opacity))
    d.rounded_rectangle((72,8,1008,92),radius=24,fill=(3,28,39,a(238)),outline=(91,231,205,a(235)),width=3)
    # Icon drawn as an original simple outline, no third-party icon asset.
    d.line([(111,27),(111,73),(136,59),(161,73),(161,27),(111,27)],fill=(124,255,221,a(255)),width=5,joint='curve')
    font=ImageFont.truetype(str(font_path),43)
    text=GENRE_CTA[genre]
    bbox=d.textbbox((0,0),text,font=font)
    text_width=bbox[2]-bbox[0]
    if text_width>785:raise ValueError('CTA too wide for mobile-safe box')
    d.text((191,17),text,font=font,fill=(244,255,251,a(255)),stroke_width=0)
    im.save(path)


def render(source,output,report,font_path,genre='ai_work',review_only=False):
    validate(source,output,genre,review_only)
    font_path=Path(font_path)
    if not font_path.is_file():raise ValueError('Japanese font not installed')
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        for frame in range(START_FRAME,TOTAL_FRAMES):
            draw(d/f'cta_{frame-START_FRAME:03d}.png',frame,genre,font_path)
        command(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
                 '-framerate','30','-i',d/'cta_%03d.png',
                 '-filter_complex',f'[1:v]setpts=PTS+{START_FRAME/FPS}/TB[ov];[0:v][ov]overlay=0:{OVERLAY_Y}:eof_action=pass:format=auto,format=yuv420p[v]',
                 '-map','[v]','-map','0:a:0','-map_metadata','0',
                 '-c:v','libx264','-preset','veryfast','-crf','18','-r','30',
                 '-frames:v',str(TOTAL_FRAMES),'-pix_fmt','yuv420p',
                 '-c:a','copy','-metadata:s:a:0','language=jpn',
                 '-movflags','+faststart',output])
    ss=probe(output)['streams']
    v,a=ss
    if len(ss)!=2 or v['width']!=1080 or v['height']!=1920 or v['r_frame_rate']!='30/1' or a['codec_name']!='aac':
        raise RuntimeError('output stream validation failed')
    if int(v.get('nb_frames','0'))!=TOTAL_FRAMES:raise RuntimeError('unexpected frame count')
    for typ in ('v','a'):
        command(['ffmpeg','-v','error','-xerror','-i',output,'-map',f'0:{typ}:0','-f','null','-'])
    with tempfile.TemporaryDirectory() as d:
        hashes=[]
        for inp,n in ((source,'before'),(output,'after')):
            p=Path(d)/(n+'.aac')
            command(['ffmpeg','-v','error','-y','-i',inp,'-map','0:a:0','-c','copy','-f','adts',p])
            hashes.append(sha(p))
        if hashes[0]!=hashes[1]:raise RuntimeError('narration audio was modified')
    result={'source_sha256':sha(source),'output_sha256':sha(output),
            'audio_adts_sha256':hashes[0],'duration_seconds':float(probe(output)['format']['duration']),
            'resolution':'1080x1920','fps':30,'frames':TOTAL_FRAMES,
            'cta':'保存して、明日1つ試す','cta_start_seconds':START_FRAME/FPS,
            'cta_region_y':[OVERLAY_Y+8,OVERLAY_Y+92],
            'protected_review_banner_y':REVIEW_BANNER_Y,
            'protected_burned_caption_y':CAPTION_SAFE_Y,
            'subtitle_track_count':0,'japanese_speech_content_asr':'NOT_VERIFIED',
            'full_av_decode':'PASS','employee_approval':False,'publication_approved':False}
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True);p.add_argument('--font',required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--review-only',action='store_true')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.report,a.font,a.genre,a.review_only),ensure_ascii=False))
if __name__=='__main__':main()
