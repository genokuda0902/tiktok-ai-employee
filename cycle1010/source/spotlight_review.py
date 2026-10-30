#!/usr/bin/env python3
"""Private-review-only before/after spotlight on the first scene.

This is a REIMPLEMENTATION, not the original v33 renderer. Source media stays
local. Only AI-work private video is approved for this local transform; other
nine genre identifiers fail closed. No publishing, uploading, or auto-posting.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path

GENRES = ('ai_work','business','money','learning','health','life','travel','food','tech','history')
SOURCE_SHA256 = '25c38de04d557190dd93ca44211e88364e7629511548dc5ae2ae331ca7981d06'
FPS = 30
END_FRAME = 45
OVERLAY_Y = 280
OVERLAY_HEIGHT = 970  # ends at 1250, above baked captions at y >= 1280
CAPTION_SAFE_Y = 1280


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()


def run(args):
    p=subprocess.run([str(x) for x in args],capture_output=True,text=True)
    if p.returncode:raise RuntimeError('command failed: '+' '.join(map(str,args))+'\n'+p.stderr[-1200:])
    return p.stdout


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))


def phase(t):
    """Before/after reveal only within the actual 0–1.5s opening shot."""
    if t < 0.12 or t >= 1.50:return 'none',0.0
    if t < 0.26:return 'before',(t-0.12)/0.14
    if t < 0.64:return 'before',1.0
    if t < 0.79:return 'before',(0.79-t)/0.15
    if t < 0.92:return 'after',(t-0.79)/0.13
    if t < 1.34:return 'after',1.0
    return 'after',max(0.0,(1.50-t)/0.16)


def validate_source(source,output,genre,review_only,expected_sha):
    if genre not in GENRES or genre != 'ai_work':raise ValueError('genre not privately approved: fail closed')
    if not review_only:raise ValueError('review-only required')
    source,output=Path(source).resolve(),Path(output).resolve()
    if not source.is_file() or source==output or output.exists():raise ValueError('source missing or output already exists')
    if expected_sha != SOURCE_SHA256 or sha256(source)!=SOURCE_SHA256:raise ValueError('source SHA256 mismatch')
    meta=probe(source);ss=meta['streams']
    if len(ss)!=2 or [x['codec_type'] for x in ss]!=['video','audio']:
        raise ValueError('requires video + audio with NO selectable subtitle track')
    v,a=ss
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('source video format mismatch')
    if (a['codec_name'],a['sample_rate'],a.get('tags',{}).get('language'))!=('aac','48000','jpn'):
        raise ValueError('source Japanese-tagged audio format mismatch')
    return meta


def draw_overlay(path,frame):
    from PIL import Image,ImageDraw
    t=frame/FPS
    side,amount=phase(t)
    im=Image.new('RGBA',(1080,OVERLAY_HEIGHT),(0,0,0,0))
    if amount <= 0:
        im.save(path);return
    d=ImageDraw.Draw(im,'RGBA')
    # Restrict effects to the content panel. No changes in caption-safe region.
    left=(44,35,535,930);right=(545,35,1036,930)
    inactive=right if side=='before' else left
    active=left if side=='before' else right
    d.rounded_rectangle(inactive,radius=28,fill=(1,9,22,int(86*amount)))
    # Subtle teal edge; avoid covering the existing Japanese labels.
    d.rounded_rectangle(active,radius=28,outline=(105,242,224,int(210*amount)),width=5)
    # Animated vertical glint, confined to the active half and below top titles.
    x0,x1=active[0]+18,active[2]-18
    p=(t*0.75)%1.0
    x=int(x0+(x1-x0)*p)
    d.line([(x,120),(x,790)],fill=(115,255,233,int(42*amount)),width=7)
    im.save(path)


def render(source,output,report,genre='ai_work',review_only=False,expected_sha=SOURCE_SHA256):
    before=validate_source(source,output,genre,review_only,expected_sha)
    Path(output).parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        tmp=Path(tmp)
        for i in range(END_FRAME):draw_overlay(tmp/f'overlay_{i:03d}.png',i)
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate','30','-i',tmp/'overlay_%03d.png',
             '-filter_complex',f'[0:v][1:v]overlay=0:{OVERLAY_Y}:eof_action=pass:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-map_chapters','0','-map_metadata','0',
             '-c:v','libx264','-preset','veryfast','-crf','18','-r','30','-pix_fmt','yuv420p',
             '-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',output])
    after=probe(output)
    ss=after['streams'];v,a=ss
    assert len(ss)==2 and v['codec_name']=='h264' and a['codec_name']=='aac'
    assert (v['width'],v['height'],v['r_frame_rate'])==(1080,1920,'30/1')
    assert a['sample_rate']=='48000' and a.get('tags',{}).get('language')=='jpn'
    assert abs(float(before['format']['duration'])-float(after['format']['duration']))<0.04
    for stream in ('v','a'):
        run(['ffmpeg','-v','error','-xerror','-i',output,'-map',f'0:{stream}:0','-f','null','-'])
    # Stream-copy preserves AAC packets, unlike the re-encoded H264.
    with tempfile.TemporaryDirectory() as tmp:
        src=Path(tmp)/'src.aac';dst=Path(tmp)/'dst.aac'
        for inp,out in ((source,src),(output,dst)):
            run(['ffmpeg','-v','error','-y','-i',inp,'-map','0:a:0','-c','copy','-f','adts',out])
        assert sha256(src)==sha256(dst),'audio elementary stream unexpectedly changed'
        audio_sha=sha256(src)
    result={'source_sha256':sha256(source),'output_sha256':sha256(output),
            'audio_adts_sha256':audio_sha,'duration_s':float(after['format']['duration']),
            'width':v['width'],'height':v['height'],'fps':v['r_frame_rate'],
            'video_codec':v['codec_name'],'audio_codec':a['codec_name'],
            'audio_sample_rate':a['sample_rate'],'audio_language_metadata':a.get('tags',{}).get('language'),
            'subtitle_tracks':0,'burned_in_subtitles':'inherited; no independent ASR verification',
            'overlay_frames':END_FRAME,'overlay_region_y':[OVERLAY_Y,OVERLAY_Y+OVERLAY_HEIGHT],
            'full_video_audio_decode':'PASS','review_only':True,'publication_approved':False}
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work')
    p.add_argument('--review-only',action='store_true');p.add_argument('--source-sha256',default=SOURCE_SHA256)
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.report,a.genre,a.review_only,a.source_sha256),ensure_ascii=False))
if __name__=='__main__':main()
