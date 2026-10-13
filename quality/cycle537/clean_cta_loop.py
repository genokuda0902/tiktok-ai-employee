#!/usr/bin/env python3
"""cycle537: genre-neutral clean CTA / loop. Reimplementation, REVIEW ONLY.
Requires approved-format 20s input. Audio copied; Japanese narration NOT certified.
"""
import argparse, hashlib, io, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS,DURATION=1080,1920,30,20.
START,CTA_END=18.5,19.7
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REGULAR='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
'営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')

def validate(c):
    if c.get('genre') not in GENRES: raise ValueError('genre')
    if c.get('rights')!='SYNTHETIC_OR_OWNER_APPROVED' or c.get('contains_private_data') is not False: raise ValueError('rights/privacy')
    if c.get('review_status')!='HUMAN_REVIEW' or c.get('publication')!='NOT_APPROVED': raise ValueError('publication')
    if c.get('claims_real_results') is not False: raise ValueError('claims')
    for k,lim in [('brand',12),('cta',18),('step_1',11),('step_2',11),('step_3',11)]:
        s=c.get(k)
        if not isinstance(s,str) or not 2<=len(s)<=lim or any(x in s for x in '\n\r\t'): raise ValueError(k)
    if not Path(FONT).exists(): raise FileNotFoundError(FONT)
    return True

def ease(t):
    t=max(0.,min(1.,t))
    return t*t*(3-2*t)

def text(d,pos,s,size,color,bold=True):
    ft=ImageFont.truetype(FONT if bold else REGULAR,size)
    x0,y0,x1,y1=d.textbbox(pos,s,font=ft)
    if x0<72 or x1>1008 or y0<200 or y1>1590: raise ValueError('text safe region: '+s)
    d.text(pos,s,font=ft,fill=color)

def cta_frame(t,c):
    validate(c)
    im=Image.new('RGB',(W,H),(6,20,35));d=ImageDraw.Draw(im)
    for y in range(0,H,8):
        z=y/H
        d.rectangle((0,y,W,y+8),fill=(round(6+7*z),round(20+17*z),round(35+17*z)))
    for i in range(8):
        x=75+i*127
        d.rounded_rectangle((x,340+i%3*38,x+76,970-i%3*37),radius=32,fill=(11+i*3,42+i*3,60+i*3))
    d.rounded_rectangle((70,230,1010,317),radius=21,fill='#113e4d',outline='#3faaa9',width=2)
    text(d,(104,247),c['brand']+'  /  保存版',37,'#b5fff1')
    text(d,(95,445),'あとで試せるように',64,'#ffffff')
    d.rounded_rectangle((77,572,1003,720),radius=31,fill='#2aead1')
    text(d,(108,599),c['cta'],65,'#062b34')
    for i,label in enumerate((c['step_1'],c['step_2'],c['step_3'])):
        x,y=89,833+136*i;active=ease((t-.14*i)/.35)
        d.rounded_rectangle((x,y,991,y+109),radius=23,fill='#183c4a',outline='#3b7e81',width=2)
        d.rounded_rectangle((x+20,y+21,x+89,y+89),radius=17,fill='#0e7d78')
        text(d,(x+38,y+30),str(i+1),40,'#ffffff')
        text(d,(x+122,y+27),label,45,'#ffffff' if active>.15 else '#8ba7b4')
        d.rounded_rectangle((x+120,y+93,x+120+round(755*active),y+99),radius=3,fill='#2aead1')
    text(d,(102,1371),'※架空データによる再現デモ',34,'#c6e0e5',False)
    text(d,(102,1452),'結果は必ず自分で確認',39,'#ffffff')
    text(d,(104,1550),'REVIEW ONLY',26,'#a5c6cc',False)
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def render(source,output,c):
    validate(c)
    source,output=Path(source),Path(output)
    p=probe(source);v=next(s for s in p['streams'] if s['codec_type']=='video')
    a=[s for s in p['streams'] if s['codec_type']=='audio']
    if (v['codec_name'],v['width'],v['height'])!=('h264',W,H) or not a or a[0]['codec_name']!='aac': raise ValueError('source codec')
    if abs(float(p['format']['duration'])-DURATION)>.05: raise ValueError('source duration')
    output.parent.mkdir(parents=True,exist_ok=True)
    head=subprocess.check_output(['ffmpeg','-hide_banner','-loglevel','error','-i',str(source),'-frames:v','1','-f','image2pipe','-vcodec','png','pipe:1'])
    first=Image.open(io.BytesIO(head)).convert('RGB')
    n_cta=round((CTA_END-START)*FPS);n_hold=round((DURATION-CTA_END)*FPS)
    filt=f'[0:v]trim=0:{START},setpts=PTS-STARTPTS[h];[h][1:v]concat=n=2:v=1:a=0[v]'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
    '-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','pipe:0',
    '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
    '-crf','20','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-t',str(DURATION),'-movflags','+faststart',str(output)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(n_cta): p.stdin.write(cta_frame(i/FPS,c).tobytes())
        for i in range(n_hold): p.stdin.write(first.tobytes())
        p.stdin.close();err=p.stderr.read().decode('utf8','replace')
        if p.wait()!=0: raise RuntimeError(err[-3000:])
    except Exception: p.kill();raise
    return {'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'output':str(output),'narration':'NOT_VERIFIED','publication':'NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--config',required=True)
    x=ap.parse_args()
    print(json.dumps(render(x.source,x.output,json.loads(Path(x.config).read_text(encoding='utf8'))),ensure_ascii=False))
