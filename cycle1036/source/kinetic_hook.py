#!/usr/bin/env python3
"""Offline, review-only kinetic opening hook. Original graphic overlay, not recovered v33.

A cinematic typography plate covers only the top content of the first 1.2 seconds,
then fades to the existing before/after proof. Captions below y=1280 and original
AAC elementary audio are preserved. No assets, source videos or outputs are uploaded.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRE_HOOKS={
 'ai_work':('まだ手作業で','集計してるの？'),
 'beauty':('毎日のケア','見直してる？'),
 'romance_psychology':('その会話','伝わってる？'),
 'money_saving':('毎月の支出','把握してる？'),
 'sales_business':('営業の数字','確認してる？'),
 'career':('仕事の進め方','変えてみる？'),
 'health_lifestyle':('毎日の習慣','続いてる？'),
 'science_trivia':('その常識','確かめた？'),
 'travel_food':('次のお出かけ','決めてる？'),
 'product_comparison_lifestyle':('その選び方','比べてみた？'),
}
W,H,FPS,HOOK_FRAMES=1080,1250,30,36
SUBTITLE_TOP=1280
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def run(cmd,binary=False):
    p=subprocess.run([str(x) for x in cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('command failed: '+' '.join(map(str,cmd[:6]))+'\n'+p.stderr.decode(errors='replace')[-2000:])
    return p.stdout if binary else p.stdout.decode()

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def opacity(frame):
    if type(frame) is not int or frame<0 or frame>=HOOK_FRAMES:raise ValueError('invalid frame')
    if frame<18:return 1.0
    t=(frame-18)/(HOOK_FRAMES-19)
    return max(0.,min(1.,1.-t*t*(3-2*t)))

def font(size):
    if not Path(FONT).exists():raise FileNotFoundError('Noto CJK font required; no unsafe fallback')
    return ImageFont.truetype(FONT,size,index=0)

def fit_text(text,maximum=100,width=880):
    d=ImageDraw.Draw(Image.new('RGB',(1,1)))
    for size in range(maximum,39,-2):
        f=font(size)
        if d.textbbox((0,0),text,font=f,stroke_width=5)[2]<=width:return f
    raise ValueError('headline too wide; manual layout needed')

def render_plate(frame,genre):
    if genre not in GENRE_HOOKS:raise ValueError('unknown genre')
    a=opacity(frame)
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(im,'RGBA')
    d.rectangle((0,0,W,H),fill=(2,13,28,int(191*a)))
    # Low-frequency cinematic streaks; no strobe, no flashing.
    shift=int(40*frame/HOOK_FRAMES)
    for j in range(13):
        y=120+j*66+shift
        d.line((0,y,210+(j%4)*38,y-100),fill=(34,212,232,int(64*a)),width=3)
        d.line((W,y+5,W-160-(j%5)*22,y-85),fill=(255,198,56,int(55*a)),width=3)
    # Bold hero card, small controlled motion (max 24px).
    dy=int(24*math.sin((frame/(HOOK_FRAMES-1))*math.pi/2))
    top=310+dy
    d.rounded_rectangle((52,top,1028,top+510),radius=38,
                        fill=(4,19,37,int(238*a)),outline=(42,211,236,int(245*a)),width=5)
    d.rounded_rectangle((94,top+35,446,top+96),radius=18,fill=(18,94,116,int(230*a)))
    small=font(36)
    d.text((114,top+44),'AI時短ラボ  /  実演',font=small,fill=(240,251,255,int(255*a)))
    for j,txt in enumerate(GENRE_HOOKS[genre]):
        f=fit_text(txt)
        bb=d.textbbox((0,0),txt,font=f,stroke_width=5)
        tw=bb[2]-bb[0]
        y=top+130+j*122
        # yellow second line, white first line, 8px dark stroke
        d.text(((W-tw)//2,y),txt,font=f,fill=(255,215,66,int(255*a)) if j else (255,255,255,int(255*a)),
               stroke_width=7,stroke_fill=(1,9,23,int(255*a)))
    d.text((116,top+433),'答えは、次の画面で確認。',font=font(35),fill=(142,244,243,int(255*a)))
    return im

def validate_source(source,expected_sha,genre,review_only,synthetic_ci=False):
    if not review_only:raise ValueError('human review gate required')
    if genre not in GENRE_HOOKS:raise ValueError('unknown genre')
    if genre!='ai_work':raise ValueError('genre-specific source rights not verified')
    if len(expected_sha)!=64 or sha(source)!=expected_sha:raise ValueError('source SHA mismatch')
    p=probe(source)
    v=[x for x in p['streams'] if x['codec_type']=='video']
    a=[x for x in p['streams'] if x['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or len(p['streams'])!=2:raise ValueError('requires exactly 1 video and 1 audio stream')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],a[0]['codec_name'],int(a[0]['sample_rate']))!=('h264',1080,1920,'30/1','aac',48000):
        raise ValueError('unsupported source A/V')
    frames=int(v[0]['nb_frames'])
    if (not synthetic_ci and frames!=691) or frames<HOOK_FRAMES+1:raise ValueError('unexpected frame count')
    return frames

def render(source,output,report,expected_sha,genre='ai_work',review_only=False,synthetic_ci=False):
    source,output,report=map(lambda p:Path(p).resolve(),(source,output,report))
    if not source.is_file() or output.exists() or report.exists() or len({source,output,report})!=3:
        raise ValueError('source missing, output already exists, or paths collide')
    frames=validate_source(source,expected_sha,genre,review_only,synthetic_ci)
    output.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='kinetic_hook_') as temp:
        folder=Path(temp)
        for n in range(HOOK_FRAMES):render_plate(n,genre).save(folder/f'{n:03d}.png')
        run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y',
             '-i',source,'-framerate',str(FPS),'-i',folder/'%03d.png',
             '-filter_complex','[0:v][1:v]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
             '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
             '-crf','18','-pix_fmt','yuv420p','-threads','2','-c:a','copy',
             '-metadata:s:a:0','language=jpn','-movflags','+faststart',
             '-frames:v',str(frames),output])
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    q=probe(output)
    ov=next(x for x in q['streams'] if x['codec_type']=='video')
    if (ov['width'],ov['height'],ov['r_frame_rate'],int(ov['nb_frames']))!=(1080,1920,'30/1',frames):
        raise RuntimeError('video output mismatch')
    if audio_sha(source)!=audio_sha(output):raise RuntimeError('AAC bitstream changed')
    result={'source_sha256':sha(source),'output_sha256':sha(output),
            'frames':frames,'duration':float(q['format']['duration']),
            'genre':genre,'hook_frames':HOOK_FRAMES,'hook_seconds':HOOK_FRAMES/FPS,
            'protected_subtitle_y_min':SUBTITLE_TOP,
            'video':'H264 1080x1920 30fps','audio':'AAC 48kHz Japanese-tagged',
            'audio_bitstream_unchanged':True,'full_av_decode':'PASS',
            'change':'Original kinetic Japanese headline 0-1.2s, fade reveals existing before/after',
            'caption_semantic_sync':'NOT_VERIFIED','independent_japanese_asr':'NOT_PERFORMED',
            'rights':'NOT_VERIFIED','employee_approval':'NOT_APPROVED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for x in ('source','output','report','expected-sha'):p.add_argument('--'+x,required=True)
    p.add_argument('--genre',default='ai_work');p.add_argument('--review-only',action='store_true')
    p.add_argument('--synthetic-ci',action='store_true')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.report,a.expected_sha,a.genre,a.review_only,a.synthetic_ci),ensure_ascii=False))
