#!/usr/bin/env python3
"""Cycle787: non-obscuring result-focus overlay for any review-only 9:16 video.

A configurable focus rectangle traces around, never across, an important result.
No external services. Does not infer rights, semantic caption correctness or publish approval.
"""
import argparse
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter


def validate(config):
    w,h=config['canvas']; x1,y1,x2,y2=config['bbox']
    assert w>0 and h>0 and 0<=x1<x2<=w and 0<=y1<y2<=h
    assert config['start']>=0 and config['end']>config['start']
    # Keep the focus indicator within a conservative TikTok central content area.
    l,t,r,b=config['safe_area']; assert 0<=l<r<=w and 0<=t<b<=h
    assert l<=x1 and x2<=r and t<=y1 and y2<=b, 'focus outside safe area'
    for a in config.get('protected_text_boxes',[]):
        # Do not place focus *border* through the inner text area.
        assert x1+12 <= a[0] and y1+12 <= a[1] and x2-12 >= a[2] and y2-12 >= a[3], 'text not inside focus border'
    assert config['end']<=config['duration']
    assert config['rights_reviewed'] is False and config['publication_approved'] is False
    return True


def easing(t):
    t=max(0,min(1,t))
    return t*t*(3-2*t)


def render_overlay_frame(config, t):
    w,h=config['canvas']; x1,y1,x2,y2=config['bbox']
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    # soft fade at both edges; no flashes, no scene-covering fill.
    fade=min(1,(t-config['start'])/.22,(config['end']-t)/.22)
    if fade<=0:return im
    alpha=easing(fade)
    pulse=0.68+0.32*math.sin(2*math.pi*(t-config['start'])/1.1)**2
    # Outline is outside the content text, animated corner markers direct attention.
    draw=ImageDraw.Draw(im)
    glow=Image.new('RGBA',(w,h),(0,0,0,0)); g=ImageDraw.Draw(glow)
    color=(55,237,223,int(95*alpha*pulse))
    g.rounded_rectangle((x1,y1,x2,y2),radius=19,outline=color,width=13)
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(13)))
    draw=ImageDraw.Draw(im)
    draw.rounded_rectangle((x1,y1,x2,y2),radius=19,outline=(124,255,239,int(230*alpha)),width=6)
    # corner dashes show a result 'lock-on' without adding claims or captions.
    corner=25; c=(255,246,171,int(235*alpha))
    for xx,sgn in [(x1,-1),(x2,1)]:
        for yy,sgny in [(y1,-1),(y2,1)]:
            draw.line([(xx+sgn*2,yy),(xx+sgn*corner,yy)],fill=c,width=5)
            draw.line([(xx,yy+sgny*2),(xx,yy+sgny*corner)],fill=c,width=5)
    for bx in config.get('protected_text_boxes',[]):
        ImageDraw.Draw(im).rectangle(tuple(bx),fill=(0,0,0,0))
    return im


def probe(path):
    p=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=index,codec_name,width,height','-of','json',str(path)],check=True,capture_output=True,text=True)
    return json.loads(p.stdout)


def run(input_mp4,output_mp4,config,report_path):
    validate(config)
    src=probe(input_mp4); video=next(s for s in src['streams'] if s['codec_name']=='h264')
    assert (video['width'],video['height'])==tuple(config['canvas'])
    assert abs(float(src['format']['duration'])-config['duration'])<.08
    fps=30
    with tempfile.TemporaryDirectory(prefix='cycle787_') as td:
        p=Path(td)
        frames=math.ceil((config['end']-config['start'])*fps)
        for i in range(frames):
            t=config['start']+i/fps
            render_overlay_frame(config,t).save(p/f'overlay_{i:04d}.png')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(input_mp4),
             '-itsoffset',str(config['start']),'-framerate',str(fps),'-i',str(p/'overlay_%04d.png'),
             '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:repeatlast=0:format=auto,format=yuv420p[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
             '-c:a','copy','-movflags','+faststart',str(output_mp4)]
        subprocess.run(cmd,check=True)
    dst=probe(output_mp4)
    report={'source':str(input_mp4),'output':str(output_mp4),'focus_seconds':[config['start'],config['end']],
            'frame_count':frames,'canvas':config['canvas'],'video_codec':next(s['codec_name'] for s in dst['streams'] if s.get('width')),
            'audio_codec':next(s['codec_name'] for s in dst['streams'] if not s.get('width')),
            'duration':float(dst['format']['duration']),'rights_reviewed':False,'publication_approved':False,
            'semantic_voice_caption_alignment':'NOT_VERIFIED','reference_v33_direct_comparison':'NOT_AVAILABLE'}
    Path(report_path).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    return report

if __name__=='__main__':
    a=argparse.ArgumentParser(); a.add_argument('--input',required=True); a.add_argument('--output',required=True)
    a.add_argument('--config',required=True); a.add_argument('--report',required=True); z=a.parse_args()
    print(json.dumps(run(z.input,z.output,json.loads(Path(z.config).read_text()),z.report),ensure_ascii=False))
