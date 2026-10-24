#!/usr/bin/env python3
"""cycle816: reusable, privacy-safe BEFORE -> AFTER priority reveal.

Replace only 9.0–12.0 s (frames 270..359) of an existing 718-frame
1080x1920 review MP4. Public CI uses a synthetic video/tone source.
Inherited Japanese audio is stream-copied; ASR/semantic sync NOT verified.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,TOTAL=1080,1920,30,718
START,FRAMES=270,90
X,Y,CW,CH=125,660,830,640
ACCENTS={
 'ai_work':'#55d6ff','beauty':'#ff99d4','love_psychology':'#ff9cbb',
 'money_saving':'#8fe7a2','sales_business':'#60e6d2','career':'#a8b8ff',
 'health_life':'#93e2b2','science':'#9ecbff','travel_food':'#ffcc83',
 'product_life':'#a8d8ef'}
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc')
DEFAULT_LABELS=('課題A','課題B','課題C')

def font(size):
    path=os.environ.get('TIKTOK_JA_FONT') or next((p for p in FONTS if Path(p).is_file()),None)
    if not path: raise RuntimeError('Noto CJK font required')
    return ImageFont.truetype(path,size)

def validate(genre, labels, selected, fictional):
    if genre not in ACCENTS: raise ValueError('unknown genre')
    if fictional is not True: raise ValueError('fictional-data opt-in required')
    if not isinstance(labels,(tuple,list)) or len(labels)!=3: raise ValueError('3 labels required')
    if any(not isinstance(s,str) or not 1<=len(s)<=8 or '\n' in s for s in labels):
        raise ValueError('unsafe label')
    if selected not in (0,1,2): raise ValueError('invalid selected index')
    if not (X>=100 and X+CW<=W-100 and Y>=620 and Y+CH<=1360):
        raise ValueError('unsafe caption region')
    return ACCENTS[genre]

def smooth(t):
    t=max(0.,min(1.,float(t)));return t*t*(3-2*t)

def stage(frame):
    if not 0<=frame<FRAMES: raise ValueError('frame outside scene')
    return 0 if frame<27 else (1 if frame<57 else 2)

def draw(frame,genre='sales_business',labels=DEFAULT_LABELS,selected=1):
    accent=validate(genre,labels,selected,True)
    beat=stage(frame)
    im=Image.new('RGBA',(CW,CH),(0,0,0,0));d=ImageDraw.Draw(im)
    # Fully opaque inner canvas prevents inherited card text ghosting.
    d.rounded_rectangle((0,0,CW-1,CH-1),radius=29,fill='#071d30',outline='#638b9f',width=3)
    d.text((37,21),'BEFORE  →  AFTER',font=font(38),fill='#ffffff')
    d.text((646,31),'架空の例',font=font(24),fill='#ffd88a')
    d.line((34,83,798,83),fill='#376174',width=3)
    # Left: too many tasks, no clear next step.
    d.rounded_rectangle((32,109,387,500),radius=23,fill='#203245',outline='#647687',width=3)
    d.text((57,130),'BEFORE',font=font(31),fill='#f5c4c6')
    d.text((57,178),'優先順位が不明',font=font(24),fill='#e7e9ee')
    for i,label in enumerate(labels):
        top=235+i*73
        d.rounded_rectangle((55,top,359,top+57),radius=13,fill='#33495c',outline='#52687b',width=2)
        d.text((76,top+8),label,font=font(26),fill='#e0e9f0')
        d.ellipse((322,top+19,339,top+36),fill='#d2a1a6')
    # Directional cue sweeps from left to right.
    d.line((393,318,437,318),fill='#789eac',width=7)
    d.polygon([(440,318),(422,304),(422,332)],fill=accent)
    if beat>=1:
        p=smooth((frame-27)/25)
        d.line((393,318,393+int(47*p),318),fill=accent,width=9)
    # Right: one actionable priority; no claim of actual results.
    d.rounded_rectangle((451,109,800,500),radius=23,fill='#0c3040',outline=accent if beat==2 else '#52798a',width=4 if beat==2 else 2)
    d.text((478,130),'AFTER',font=font(31),fill=accent)
    d.text((478,178),'最初の一歩を決定',font=font(23),fill='#e7f6f4')
    if beat==0:
        d.rounded_rectangle((480,254,774,363),radius=17,fill='#18394b')
        d.text((501,286),'優先項目を選ぶ',font=font(24),fill='#9bb4c3')
    else:
        p=smooth((frame-27)/27)
        d.rounded_rectangle((478,250,775,379),radius=17,fill='#174c56',outline=accent,width=3)
        label=labels[selected]
        # Reveal text only after focus animation begins.
        if p>.2:
            d.text((499,266),'まずはこれ',font=font(24),fill='#c9e9e6')
            d.text((499,310),label,font=font(43),fill='#ffffff')
        if beat==2:
            d.ellipse((711,278,755,322),fill=accent)
            d.line((720,301,730,312,746,287),fill='#063043',width=5,joint='curve')
    # Three-phase progress indicator, explicit illustrative claim.
    d.text((38,529),'課題を並べる  →  ひとつ選ぶ  →  行動する',font=font(25),fill='#d4e9ed')
    d.rounded_rectangle((38,580,790,596),radius=8,fill='#284a5b')
    progress=(frame+1)/FRAMES
    d.rounded_rectangle((38,580,38+max(6,int(752*progress)),596),radius=8,fill=accent)
    return im

def run(cmd):
    p=subprocess.run([str(x) for x in cmd],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(' '.join(map(str,cmd))+'\n'+p.stderr[-2500:])
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def audio_digest(path):
    with tempfile.TemporaryDirectory() as td:
        p=Path(td)/'audio.aac'
        run(['ffmpeg','-v','error','-y','-i',path,'-map','0:a:0','-c:a','copy','-f','adts',p])
        return digest(p)

def render(source,output,genre='sales_business',labels=DEFAULT_LABELS,selected=1,
           fictional=False,synthetic_source=False):
    validate(genre,labels,selected,fictional)
    source,output=Path(source),Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    src=probe(source);v=next(s for s in src['streams'] if s['codec_type']=='video')
    a=next(s for s in src['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL):
        raise ValueError('1080x1920 30fps 718 frames required')
    if a['codec_name']!='aac' or a['sample_rate']!='48000':raise ValueError('AAC 48kHz required')
    with tempfile.TemporaryDirectory(prefix='cycle816_') as td:
        folder=Path(td)
        for i in range(FRAMES):draw(i,genre,labels,selected).save(folder/f'{i:03d}.png')
        fc=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/{FPS}/TB[card];'
            f'[0:v][card]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:'
            f'format=auto:enable=\'between(n,{START},{START+FRAMES-1})\'[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate',str(FPS),'-start_number','0','-i',folder/'%03d.png',
             '-filter_complex',fc,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
             '-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',output])
    out=probe(output);ov=next(s for s in out['streams'] if s['codec_type']=='video')
    oa=next(s for s in out['streams'] if s['codec_type']=='audio')
    if (ov['width'],ov['height'],int(ov['nb_frames']))!=(W,H,TOTAL):raise RuntimeError('video QA failed')
    if oa['codec_name']!='aac' or oa['sample_rate']!='48000':raise RuntimeError('audio QA failed')
    if abs(float(out['format']['duration'])-TOTAL/FPS)>.06:raise RuntimeError('duration QA failed')
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    if audio_digest(source)!=audio_digest(output):raise RuntimeError('AAC bitstream changed')
    qa={'cycle':816,'genre':genre,'source_sha256':digest(source),'output_sha256':digest(output),
        'scene_frames':[START,START+FRAMES-1],'synthetic_source':synthetic_source,
        'fictional_data':True,'width':W,'height':H,'fps':FPS,'frames':TOTAL,
        'duration_seconds':float(out['format']['duration']),'video_codec':ov['codec_name'],
        'audio_codec':oa['codec_name'],'audio_sample_rate':oa['sample_rate'],
        'aac_bitstream_identical':True,'full_av_decode_pass':True,
        'japanese_narration_inherited':not synthetic_source,
        'caption_region_preserved':True,'independent_asr_verified':False,
        'reference_v33_direct_comparison':False,'smartphone_verified':False,
        'rights_approved':False,'employee_approved':False,'publication_approved':False,
        'auto_post':False,'review_only':True}
    (output.parent/'cycle816_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
    return qa

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',default='sales_business',choices=tuple(ACCENTS))
    p.add_argument('--fictional-data',action='store_true',required=True)
    p.add_argument('--synthetic-source',action='store_true')
    args=p.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre,fictional=args.fictional_data,
                            synthetic_source=args.synthetic_source),ensure_ascii=False,indent=2))
