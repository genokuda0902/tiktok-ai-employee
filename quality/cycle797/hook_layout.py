#!/usr/bin/env python3
"""cycle797: deterministic crop-safe, image-first hook rebuild (review only).

Source video and visual crops stay local; never uploads any source media.
No external network, music, or commercial service. No posting.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT, FPS = 1080, 1920, 30
INTRO_FRAMES = 96
FONT_REGULAR = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = ('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス',
          '転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
CARDS = ((70, 634, 462, 1164), (503, 634, 895, 1164))
SAFE = (54, 192, 900, 1530)  # right 180px reserved, top10%, bottom20%
CAPTION = (72, 1336, 896, 1450)


def run(args):
    p = subprocess.run([str(a) for a in args], capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError('Command failed: ' + ' '.join(map(str,args)) + '\n' + p.stderr[-1800:])
    return p.stdout


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def check_config(cfg):
    if cfg.get('genre') not in GENRES or set(cfg.get('genres',[])) != set(GENRES):
        raise ValueError('Genre contract must include all 10 supported genres')
    if cfg.get('mode') != 'review_only' or cfg.get('rights_reviewed') is not False or \
       cfg.get('employee_approved') is not False or cfg.get('publication_approved') is not False:
        raise ValueError('Fail-closed: unapproved assets are review-only')
    for card in CARDS:
        if not (SAFE[0] <= card[0] < card[2] <= SAFE[2] and SAFE[1] <= card[1] < card[3] <= SAFE[3]):
            raise ValueError('Card outside safe area')
    if not (SAFE[0] <= CAPTION[0] < CAPTION[2] <= SAFE[2] and
            SAFE[1] <= CAPTION[1] < CAPTION[3] <= SAFE[3]):
        raise ValueError('Caption outside safe area')
    if CAPTION[1] <= max(c[3] for c in CARDS):
        raise ValueError('Caption overlaps card')
    return True


def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def fit_font(draw, text, max_width, start=42, min_size=23):
    for size in range(start, min_size-1, -1):
        f=font(size, True)
        if draw.textbbox((0,0), text, font=f)[2] <= max_width:
            return f
    raise ValueError('Text cannot fit safe card: '+text)


def make_spreadsheet_panel():
    # Recreate fictional spreadsheet proof as typography rather than crop tiny UI.
    panel=Image.new('RGB',(372,330),(238,247,249))
    d=ImageDraw.Draw(panel)
    d.rectangle((0,0,372,48),fill=(14,105,83))
    d.text((16,7),'月別売上（架空）',font=font(26,True),fill=(255,255,255))
    d.rectangle((0,48,372,85),fill=(203,224,223))
    d.text((22,51),'月',font=font(24,True),fill=(10,47,57))
    d.text((125,51),'売上（円）',font=font(24,True),fill=(10,47,57))
    for i,(month,amount) in enumerate(((1,'120,000'),(2,'150,000'),(3,'200,000'),(4,'180,000'))):
        y=85+i*43
        d.rectangle((0,y,372,y+43),fill=(248,252,253) if i%2==0 else (224,238,240))
        d.text((22,y+3),f'{month}月',font=font(25,True),fill=(20,49,61))
        d.text((124,y+3),amount,font=font(25,True),fill=(20,49,61))
    d.rectangle((0,257,372,330),fill=(4,46,62))
    d.text((12,261),'合計',font=font(24,True),fill=(116,241,224))
    d.text((111,261),'650,000円',font=font(32,True),fill=(255,255,255))
    return panel


def source_stills(video, time=1.2):
    import cv2
    cap=cv2.VideoCapture(str(video))
    if not cap.isOpened():raise ValueError('Cannot open approved-for-local-review source')
    cap.set(cv2.CAP_PROP_POS_MSEC,time*1000)
    ok,frame=cap.read();cap.release()
    if not ok or frame.shape[1] != WIDTH or frame.shape[0] != HEIGHT:
        raise ValueError('Clean hook source must be 1080x1920')
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    im=Image.fromarray(frame)
    # Crop only the face/photo, excluding the source's clipped Japanese captions.
    return im.crop((85,845,445,1150)), make_spreadsheet_panel()


def rounded_photo(image, size):
    w,h=size
    # center-crop only inside photo panel; never crop Japanese text (all text drawn separately).
    iw,ih=image.size
    scale=max(w/iw,h/ih)
    resized=image.resize((math.ceil(iw*scale),math.ceil(ih*scale)),Image.Resampling.LANCZOS)
    rw,rh=resized.size
    crop=resized.crop(((rw-w)//2,(rh-h)//2,(rw+w)//2,(rh+h)//2))
    mask=Image.new('L',size,0);md=ImageDraw.Draw(mask);md.rounded_rectangle((0,0,w-1,h-1),radius=15,fill=255)
    crop.putalpha(mask)
    return crop


def make_background():
    im=Image.new('RGB',(WIDTH,HEIGHT))
    px=im.load()
    for y in range(HEIGHT):
        fy=y/HEIGHT
        for x in range(WIDTH):
            glow=max(0.,1.-math.hypot((x-750)/1000,(y-750)/950))
            px[x,y]=(int(3+7*glow),int(22+13*glow+3*fy),int(44+23*glow+5*fy))
    d=ImageDraw.Draw(im)
    for x in range(70,1040,120):d.line((x,170,x,1580),fill=(10,38,61),width=2)
    for y in range(210,1580,120):d.line((40,y,1040,y),fill=(10,38,61),width=2)
    return im


def make_frame(t, bg, stills, cfg):
    im=bg.copy().convert('RGBA');d=ImageDraw.Draw(im,'RGBA')
    d.rounded_rectangle((70,215,470,270),radius=20,fill=(2,52,67,245),outline=(74,221,220,245),width=2)
    d.text((93,222),'AI × 表計算  /  DEMO',font=font(26,True),fill=(208,248,247))
    d.text((72,325),'その集計、',font=font(76,True),fill=(246,251,255))
    d.text((72,424),'まだ手作業？',font=font(76,True),fill=(246,251,255))
    d.text((75,544),'BEFORE  →  AFTER で比較',font=font(32),fill=(110,236,229))
    # slide-in animation on cards, with bounded motion and clean full-width footers.
    settle=max(0.,1.-t/0.52)**2
    for i,(box,pic) in enumerate(zip(CARDS,stills)):
        x0,y0,x1,y1=box;dx=int(((-60 if i==0 else 60)*settle))
        x0+=dx;x1+=dx
        border=(255,173,144,255) if i==0 else (74,242,227,255)
        d.rounded_rectangle((x0,y0,x1,y1),radius=25,fill=(3,18,39,255),outline=border,width=5)
        d.rounded_rectangle((x0+8,y0+8,x1-8,y0+80),radius=17,fill=(5,21,39,255))
        d.text((x0+26,y0+16),'BEFORE' if i==0 else 'AFTER',font=font(42,True),fill=border)
        ph=rounded_photo(pic,(x1-x0-20,330))
        im.alpha_composite(ph,(x0+10,y0+85))
        d.rounded_rectangle((x0+9,y1-103,x1-9,y1-9),radius=17,fill=(4,29,50,255))
        label=cfg['before_label'] if i==0 else cfg['after_label']
        f=fit_font(d,label,(x1-x0)-48,36)
        textwidth=d.textbbox((0,0),label,font=f)[2]
        d.text((x0+(x1-x0-textwidth)//2,y1-88),label,font=f,fill=(255,255,255))
    # central comparison cue is never laid over Japanese text.
    cx=482;cy=910
    d.ellipse((cx-29,cy-29,cx+29,cy+29),fill=(3,29,49,255),outline=(220,250,249,255),width=3)
    d.line((cx-15,cy,cx+12,cy),fill=(238,253,255),width=5)
    d.polygon([(cx+15,cy),(cx+4,cy-10),(cx+4,cy+10)],fill=(238,253,255))
    # The disclaimer and subtitle are in separate, non-overlapping lanes.
    d.rounded_rectangle((72,1212,896,1288),radius=18,fill=(2,17,34,240),outline=(40,125,143,255),width=2)
    d.text((92,1231),'※ 架空データを使用した再現映像です',font=font(28),fill=(204,226,237))
    d.rounded_rectangle(CAPTION,radius=24,fill=(2,15,33,250),outline=(73,223,223,255),width=3)
    line=cfg['caption']
    f=fit_font(d,line,CAPTION[2]-CAPTION[0]-45,41)
    w=d.textbbox((0,0),line,font=f)[2]
    d.text(((CAPTION[0]+CAPTION[2]-w)//2,CAPTION[1]+23),line,font=f,fill=(255,255,255))
    return im.convert('RGB')


def render(cfg_path, latest, clean, out, report, opener_out):
    cfg=json.loads(Path(cfg_path).read_text(encoding='utf-8'));check_config(cfg)
    latest,clean,out,report,opener_out=map(Path,(latest,clean,out,report,opener_out))
    if not latest.exists() or not clean.exists():raise FileNotFoundError('Missing local review-only source')
    if 'REVIEW_ONLY' not in out.name:raise ValueError('Never render unlabelled publication video')
    if out.resolve() in (latest.resolve(),clean.resolve()):raise ValueError('Refuse source overwrite')
    source_meta=probe(latest)
    streams=source_meta['streams'];v=next(s for s in streams if s['codec_type']=='video')
    a=next((s for s in streams if s['codec_type']=='audio'),None)
    if not a or (v['width'],v['height'],v['codec_name']) != (WIDTH,HEIGHT,'h264'):
        raise ValueError('Requires vertical H.264 source with AAC narration')
    if a['codec_name']!='aac':raise ValueError('Expected AAC source audio')
    if out.parent:out.parent.mkdir(parents=True,exist_ok=True)
    report.parent.mkdir(parents=True,exist_ok=True);opener_out.parent.mkdir(parents=True,exist_ok=True)
    stills=source_stills(clean)
    bg=make_background()
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','-','-an','-c:v','libx264',
         '-preset','ultrafast','-crf','18','-pix_fmt','yuv420p',str(opener_out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(INTRO_FRAMES):
            p.stdin.write(make_frame(i/FPS,bg,stills,cfg).tobytes())
        p.stdin.close()
        err=p.stderr.read().decode(errors='replace');code=p.wait()
        if code:raise RuntimeError('Opener encode failed: '+err[-2000:])
    except BaseException:
        p.kill();p.wait();raise
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(latest),'-i',str(opener_out),
         '-filter_complex','[0:v][1:v]overlay=x=0:y=0:eof_action=pass:shortest=0,format=yuv420p[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
         '-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart',str(out)])
    run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'])
    result=probe(out);vv=next(s for s in result['streams'] if s['codec_type']=='video')
    aa=next(s for s in result['streams'] if s['codec_type']=='audio')
    if (vv['width'],vv['height'],vv['codec_name']) != (WIDTH,HEIGHT,'h264') or aa['codec_name']!='aac':
        raise ValueError('Wrong video/audio codec or resolution')
    if int(vv.get('nb_frames',0)) != int(v.get('nb_frames',0)):
        raise ValueError('Frame count mismatch')
    if abs(float(result['format']['duration'])-float(source_meta['format']['duration'])) > .06:
        raise ValueError('Duration mismatch')
    def audhash(pth):
        return run(['ffmpeg','-v','error','-i',str(pth),'-map','0:a:0','-c:a','copy','-f','hash','-hash','sha256','-']).strip()
    audio_equal=audhash(latest)==audhash(out)
    if not audio_equal:raise ValueError('Inherited Japanese narration AAC changed')
    qa={'cycle':797,'mode':'HUMAN_REVIEW','publication':'NOT_APPROVED',
        'source_sha256':hashlib.sha256(latest.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
        'duration_seconds':float(result['format']['duration']),
        'video':{'width':vv['width'],'height':vv['height'],'codec':vv['codec_name'],
                 'fps':vv['r_frame_rate'],'frames':int(vv['nb_frames'])},
        'audio':{'codec':aa['codec_name'],'sample_rate':aa['sample_rate'],
                 'aac_bitstream_identical':audio_equal,'Japanese_voice_source':'inherited_unverified'},
        'change':'Rebuild 0-3.2s hook with full-width readable before/after footer and separate caption/disclaimer lanes',
        'hook_frames':INTRO_FRAMES,'genre_contract_count':len(GENRES),
        'local_full_decode':True,'rights_verified':False,'employee_approved':False,
        'semantic_caption_sync_verified':False,'Japanese_speech_naturalness_verified':False,
        'mobile_playback_verified':False,'v33_original_compared':False}
    report.write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True)
    ap.add_argument('--source',required=True);ap.add_argument('--clean-hook',required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--report',required=True)
    ap.add_argument('--opener',required=True)
    a=ap.parse_args();print(json.dumps(render(a.config,a.source,a.clean_hook,a.output,a.report,a.opener),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
