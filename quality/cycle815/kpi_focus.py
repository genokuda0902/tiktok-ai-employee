#!/usr/bin/env python3
"""cycle815: 10-genre, review-only animated KPI gap card (fictional metrics).

Overlays only frames 180..269. Source Japanese audio and bottom captions
remain intact. Public CI uses a synthetic audio/video fixture, not user media.
"""
from __future__ import annotations
import argparse, hashlib, json, os, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,TOTAL=1080,1920,30,718
START,FRAMES=180,90
X,Y,CW,CH=125,665,830,650
ACCENTS={
 'ai_work':'#55d6ff','beauty':'#ff99d4','love_psychology':'#ff9cbb',
 'money_saving':'#8fe7a2','sales_business':'#60e6d2','career':'#a8b8ff',
 'health_life':'#93e2b2','science':'#9ecbff','travel_food':'#ffcc83',
 'product_life':'#a8d8ef'}
DEFAULT_ROWS=(('接続率',18,25),('成約率',12,20),('継続率',68,80))
FONTS=('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
       '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc')

def font(size):
    path=os.environ.get('TIKTOK_JA_FONT') or next((p for p in FONTS if Path(p).is_file()),None)
    if not path: raise RuntimeError('Noto Japanese font required')
    return ImageFont.truetype(path,size)

def check(genre,rows,fictional):
    if genre not in ACCENTS: raise ValueError('unsupported genre')
    if fictional is not True: raise ValueError('fictional-data opt-in required')
    if len(rows)!=3: raise ValueError('exactly 3 KPI rows required')
    for label,actual,target in rows:
        if not isinstance(label,str) or not 1<=len(label)<=8: raise ValueError('invalid label')
        if not isinstance(actual,int) or not isinstance(target,int) or not 0<=actual<=target<=100:
            raise ValueError('invalid KPI values')
        if target==0: raise ValueError('zero target not supported')
    if X<100 or X+CW>W-100 or Y<620 or Y+CH>1320:
        raise ValueError('unsafe region')
    return ACCENTS[genre]

def smooth(t):
    t=max(0.,min(1.,float(t)))
    return t*t*(3-2*t)

def phase(frame):
    if not 0<=frame<FRAMES: raise ValueError('outside KPI scene')
    return min(2,frame//30)

def draw(frame,genre='sales_business',rows=DEFAULT_ROWS):
    accent=check(genre,rows,True)
    active=phase(frame)
    im=Image.new('RGBA',(CW,CH),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,CW-1,CH-1),radius=28,fill='#092337',outline='#84a8ba',width=3)
    d.text((40,26),'KPI / 現状と目標',font=font(36),fill='#ffffff')
    d.text((620,37),'架空データ',font=font(24),fill='#ffd68c')
    d.line((38,92,790,92),fill='#3b6075',width=2)
    for i,(label,actual,target) in enumerate(rows):
        top=118+i*137
        highlighted=i==active
        if highlighted:
            d.rounded_rectangle((25,top-10,806,top+118),radius=19,fill='#193d50',outline=accent,width=3)
        d.text((45,top),label,font=font(33),fill='#ffffff' if highlighted else '#9eb9c8')
        d.text((538,top+2),f'{actual}% / {target}%',font=font(30),fill='#ffffff' if highlighted else '#9eb9c8')
        bx,by,bw,bh=265,top+67,480,24
        d.rounded_rectangle((bx,by,bx+bw,by+bh),radius=12,fill='#2a495f')
        ratio=actual/target
        animation=smooth((frame-i*30)/22) if frame>=i*30 else 0
        # Keep inactive rows visible as contextual data; animate active one.
        shown=ratio*(animation if highlighted else (1 if i<active else 0.12))
        fill_width=int(bw*min(1,shown))
        if fill_width>2: d.rounded_rectangle((bx,by,bx+fill_width,by+bh),radius=11,fill=accent if highlighted else '#477d88')
        d.line((bx+bw,by-10,bx+bw,by+bh+10),fill='#ffd68c',width=4)
        if highlighted:
            d.text((46,top+66),f'目標まで {target-actual}pt',font=font(26),fill='#ffd68c')
    d.rounded_rectangle((26,583,804,629),radius=11,fill='#123d4b')
    d.text((46,588),'目標との差を順番に確認',font=font(28),fill='#ffffff')
    return im

def run(cmd):
    p=subprocess.run([str(x) for x in cmd],text=True,capture_output=True)
    if p.returncode: raise RuntimeError(' '.join(map(str,cmd))+'\n'+p.stderr[-2000:])
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def aac_digest(path):
    with tempfile.TemporaryDirectory() as td:
        tmp=Path(td)/'track.aac'
        run(['ffmpeg','-v','error','-y','-i',path,'-map','0:a:0','-c:a','copy','-f','adts',tmp])
        return digest(tmp)

def render(source,output,genre='sales_business',rows=DEFAULT_ROWS,fictional=False,synthetic_source=False):
    check(genre,rows,fictional)
    source,output=Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    src=probe(source); v=next(s for s in src['streams'] if s['codec_type']=='video')
    a=next(s for s in src['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['avg_frame_rate'],int(v['nb_frames']))!=(W,H,'30/1',TOTAL):
        raise ValueError('expected 1080x1920 30fps 718 frames')
    if a['codec_name']!='aac' or a['sample_rate']!='48000': raise ValueError('expected AAC 48kHz')
    with tempfile.TemporaryDirectory(prefix='cycle815_') as td:
        folder=Path(td)
        for i in range(FRAMES): draw(i,genre,rows).save(folder/f'{i:03d}.png')
        # Timeline shift, no ghosts: opaque central panel, existing subtitle is below panel.
        fc=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START}/{FPS}/TB[kpi];'
            f'[0:v][kpi]overlay=x={X}:y={Y}:eof_action=pass:shortest=0:'
            f'format=auto:enable=\'between(n,{START},{START+FRAMES-1})\'[v]')
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',source,
             '-framerate',str(FPS),'-start_number','0','-i',folder/'%03d.png',
             '-filter_complex',fc,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p',
             '-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',output])
    out=probe(output); ov=next(s for s in out['streams'] if s['codec_type']=='video')
    oa=next(s for s in out['streams'] if s['codec_type']=='audio')
    if (ov['width'],ov['height'],int(ov['nb_frames']))!=(W,H,TOTAL): raise RuntimeError('video QA failed')
    if oa['codec_name']!='aac' or oa['sample_rate']!='48000': raise RuntimeError('audio QA failed')
    if abs(float(out['format']['duration'])-TOTAL/FPS)>0.06: raise RuntimeError('duration QA failed')
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    if aac_digest(source)!=aac_digest(output): raise RuntimeError('AAC changed')
    qa={'cycle':815,'genre':genre,'source_sha256':digest(source),'output_sha256':digest(output),
        'scene_frames':[START,START+FRAMES-1],'kpi_rows':rows,'synthetic_source':synthetic_source,
        'fictional_data':True,'width':W,'height':H,'fps':FPS,'frames':TOTAL,
        'duration_seconds':float(out['format']['duration']),'video_codec':ov['codec_name'],
        'audio_codec':oa['codec_name'],'audio_sample_rate':oa['sample_rate'],
        'aac_bitstream_identical':True,'full_av_decode_pass':True,
        'japanese_narration_inherited':not synthetic_source,
        'caption_region_preserved':True,'independent_asr_verified':False,
        'reference_v33_direct_comparison':False,'smartphone_verified':False,
        'rights_approved':False,'employee_approved':False,'publication_approved':False,
        'auto_post':False,'review_only':True}
    (output.parent/'cycle815_qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
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
