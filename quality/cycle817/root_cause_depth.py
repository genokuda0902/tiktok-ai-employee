#!/usr/bin/env python3
"""cycle817: privacy-safe, genre-neutral three-level root-cause animation.
Only replace video frames 360..449; preserve source AAC stream. REVIEW ONLY.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,TOTAL=1080,1920,30,718
START,COUNT=360,90
X,Y,CW,CH=125,660,830,640
ACCENTS={'ai_work':'#55d6ff','beauty':'#ff99d4','love_psychology':'#ff9cbb',
 'money_saving':'#8fe7a2','sales_business':'#60e6d2','career':'#a8b8ff',
 'health_life':'#93e2b2','science':'#9ecbff','travel_food':'#ffcc83',
 'product_life':'#a8d8ef'}
STEPS=('現象をつかむ','原因を掘る','仕組みを直す')
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc')

def font(size):
    f=os.environ.get('TIKTOK_JA_FONT') or next((p for p in FONTS if Path(p).is_file()),None)
    if not f: raise RuntimeError('Japanese Noto CJK font required')
    return ImageFont.truetype(f,size)

def validate(genre, steps, fictional):
    if genre not in ACCENTS: raise ValueError('unknown genre')
    if fictional is not True: raise ValueError('fictional-example opt-in required')
    if not isinstance(steps,(list,tuple)) or len(steps)!=3: raise ValueError('exactly 3 steps required')
    if any(not isinstance(s,str) or not 1<=len(s)<=10 or '\n' in s or '\r' in s for s in steps):
        raise ValueError('unsafe step text')
    if X<100 or X+CW>W-100 or Y<620 or Y+CH>1360: raise ValueError('subtitle safe zone violation')
    return ACCENTS[genre]

def smooth(t):
    t=max(0,min(1,float(t)))
    return t*t*(3-2*t)

def draw(frame,genre='sales_business',steps=STEPS):
    if not 0<=frame<COUNT: raise ValueError('frame out of bounds')
    accent=validate(genre,steps,True)
    img=Image.new('RGBA',(CW,CH),(0,0,0,0)); d=ImageDraw.Draw(img)
    d.rounded_rectangle((0,0,CW-1,CH-1),radius=28,fill='#081b2b',outline='#548293',width=3)
    d.text((34,22),'WHY × 3',font=font(47),fill='#ffffff')
    d.text((595,32),'考え方の例',font=font(24),fill='#ffdf9c')
    d.line((35,95,795,95),fill='#2c5967',width=3)
    for k,label in enumerate(steps):
        onset=k*27
        progress=smooth((frame-onset)/12)
        y=125+k*142
        active=progress>0
        if k<2:
            d.line((85,y+105,85,y+145),fill=accent if frame>=onset+22 else '#33546a',width=8)
            d.polygon(((75,y+138),(95,y+138),(85,y+152)),fill=accent if frame>=onset+22 else '#33546a')
        bg='#124454' if active else '#172b3c'
        edge=accent if active else '#385469'
        d.rounded_rectangle((39,y,791,y+110),radius=21,fill=bg,outline=edge,width=4 if active else 2)
        d.ellipse((62,y+19,128,y+85),fill=accent if active else '#39576a')
        d.text((79,y+27),str(k+1),font=font(29),fill='#092335' if active else '#ffffff')
        d.text((156,y+20),f'なぜ {k+1}',font=font(22),fill='#a6d7df' if active else '#8ca2af')
        if active:
            count=max(1,round(len(label)*progress))
            d.text((156,y+51),label[:count],font=font(34),fill='#ffffff')
        else:
            d.text((156,y+52),'・・・',font=font(30),fill='#668191')
    d.text((38,564),'表面で止めず、原因まで深掘り',font=font(28),fill='#e4f4f4')
    d.rounded_rectangle((38,610,790,623),radius=6,fill='#244557')
    d.rounded_rectangle((38,610,38+max(6,int(752*(frame+1)/COUNT)),623),radius=6,fill=accent)
    return img

def run(cmd):
    p=subprocess.run([str(c) for c in cmd],capture_output=True,text=True)
    if p.returncode: raise RuntimeError('command failed: '+' '.join(map(str,cmd))+'\n'+p.stderr[-2500:])
    return p.stdout

def probe(p):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',p]))

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def audio_sha(p):
    with tempfile.TemporaryDirectory() as td:
        f=Path(td)/'a.aac'
        run(['ffmpeg','-v','error','-y','-i',p,'-map','0:a:0','-c:a','copy','-f','adts',f])
        return sha(f)

def render(source,output,genre='sales_business',steps=STEPS,fictional=False,synthetic_source=False):
    validate(genre,steps,fictional)
    source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    sp=probe(source);v=next(s for s in sp['streams'] if s['codec_type']=='video')
    a=next(s for s in sp['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL):
        raise ValueError('source must be 1080x1920 30fps 718 frames')
    if a['codec_name']!='aac' or a['sample_rate']!='48000':raise ValueError('AAC 48kHz required')
    with tempfile.TemporaryDirectory(prefix='cycle817_') as td:
        for i in range(COUNT):draw(i,genre,steps).save(Path(td)/f'{i:03d}.png')
        fc=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/{FPS}/TB[card];'
            f'[0:v][card]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:'
            f'format=auto:enable=\'between(n,{START},{START+COUNT-1})\'[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate',FPS,'-start_number',0,'-i',Path(td)/'%03d.png',
             '-filter_complex',fc,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf',21,'-pix_fmt','yuv420p',
             '-frames:v',TOTAL,'-c:a','copy','-movflags','+faststart',output])
    op=probe(output);ov=next(s for s in op['streams'] if s['codec_type']=='video')
    oa=next(s for s in op['streams'] if s['codec_type']=='audio')
    if (ov['width'],ov['height'],int(ov['nb_frames']))!=(W,H,TOTAL):raise RuntimeError('video QA failed')
    if oa['codec_name']!='aac' or oa['sample_rate']!='48000':raise RuntimeError('audio QA failed')
    if abs(float(op['format']['duration'])-TOTAL/FPS)>.06:raise RuntimeError('duration QA failed')
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    same_audio=audio_sha(source)==audio_sha(output)
    if not same_audio:raise RuntimeError('inherited AAC changed')
    qa={'cycle':817,'genre':genre,'source_sha256':sha(source),'output_sha256':sha(output),
        'changed_frames':[START,START+COUNT-1],'resolution':[W,H],'fps':FPS,'frames':TOTAL,
        'duration_seconds':float(op['format']['duration']),'video_codec':ov['codec_name'],
        'audio_codec':oa['codec_name'],'audio_sample_rate':oa['sample_rate'],
        'aac_bitstream_identical':same_audio,'full_av_decode_pass':True,
        'synthetic_source':synthetic_source,'japanese_narration_inherited':not synthetic_source,
        'subtitle_area_unmodified':True,'independent_asr_verified':False,
        'reference_v33_direct_comparison':False,'smartphone_verified':False,
        'rights_approved':False,'employee_approved':False,'publication_approved':False,
        'auto_post':False,'review_only':True}
    (output.parent/'cycle817_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--genre',choices=tuple(ACCENTS),default='sales_business')
    ap.add_argument('--fictional-example',action='store_true')
    ap.add_argument('--synthetic-source',action='store_true')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,fictional=args.fictional_example,
                            synthetic_source=args.synthetic_source),ensure_ascii=False,indent=2))
