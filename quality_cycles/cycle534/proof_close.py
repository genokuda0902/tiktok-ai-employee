#!/usr/bin/env python3
"""cycle534: review-only synthetic evidence recap, generic across 10 genres.

Reimplementation, not original v33. Never publishes or treats demo as real outcome.
Uses previous reviewed audio unchanged; Japanese narration is NOT verified.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H,FPS=1080,1920,30
START,END,TOTAL=16.0,18.5,20.0
GENRES=('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約','営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学','旅行・グルメ','商品比較・暮らし')
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else REG,size)
def ease(x):
    x=max(0.,min(1.,x));return x*x*(3-2*x)
def validate(cfg):
    if cfg.get('genre') not in GENRES:raise ValueError('unsupported genre')
    if cfg.get('rights')!='SYNTHETIC_OR_OWNER_APPROVED' or cfg.get('contains_private_data') is not False:raise ValueError('rights/privacy not verified')
    if cfg.get('review_status')!='HUMAN_REVIEW' or cfg.get('publication')!='NOT_APPROVED':raise ValueError('publication must remain blocked')
    if cfg.get('claims_real_results') is not False:raise ValueError('real outcomes cannot be asserted')
    vals=cfg.get('values'); labels=cfg.get('labels')
    if not isinstance(vals,list) or len(vals)!=4 or not all(type(v)==int and 0<=v<=9999 for v in vals):raise ValueError('invalid demo values')
    if not isinstance(labels,list) or len(labels)!=4 or not all(isinstance(x,str) and 1<=len(x)<=8 for x in labels):raise ValueError('invalid demo labels')
    if not isinstance(cfg.get('verification_title'),str) or not 1<=len(cfg['verification_title'])<=14:raise ValueError('verification title required')
    if not all(Path(p).is_file() for p in (REG,BOLD)):raise ValueError('Japanese fonts missing')

def card(d,box,fill,stroke=None,r=24,w=2):d.rounded_rectangle(box,radius=r,fill=fill,outline=stroke,width=w)

def scene(t,cfg):
    """2.5-second evidence card, safe from TikTok controls (main content y=190..1590)."""
    p=max(0.,min(1.,t/(END-START)))
    im=Image.new('RGB',(W,H),(7,24,40));d=ImageDraw.Draw(im)
    for r in range(520,80,-26):
        d.arc((760-r,-100-r,760+r,-100+r),10,180,fill=(12,43,64),width=4)
    card(d,(54,68,1026,160),(14,69,85),(44,187,192),r=24,w=3)
    d.text((88,91),'AI時短ラボ  /  CHECK',font=font(35,True),fill=(237,249,252))
    d.text((772,103),'架空データ',font=font(28),fill=(184,218,223))
    d.text((72,246),cfg['verification_title'],font=font(84,True),fill=(255,255,255))
    d.text((76,373),'入力 → 計算 → 結果を確認',font=font(42),fill=(99,224,217))
    card(d,(58,500,1022,1495),(13,48,66),(49,120,139),r=35,w=4)
    d.text((94,545),'01  元データを照合',font=font(43,True),fill=(235,250,253))
    for i,(label,value) in enumerate(zip(cfg['labels'],cfg['values'])):
        x=94+(i%2)*454;y=650+(i//2)*172
        active=ease((t-.1-i*.20)/.25)
        fill=(16+int(10*active),55+int(48*active),73+int(44*active))
        card(d,(x,y,x+426,y+145),fill,(41,122,138),r=18,w=2)
        d.text((x+25,y+18),label,font=font(33),fill=(192,225,235))
        d.text((x+25,y+67),str(value),font=font(58,True),fill=(243,253,255))
    d.text((96,1085),'02  4項目を合算',font=font(42,True),fill=(235,250,253))
    expr=' + '.join(str(v) for v in cfg['values'])
    expr_font=font(43 if len(expr)<=23 else 36,True)
    d.text((100,1173),expr,font=expr_font,fill=(210,238,241))
    card(d,(94,1265,986,1415),(7,91,98),(61,225,207),r=25,w=4)
    d.text((122,1297),'合計',font=font(43,True),fill=(229,251,248))
    if t>.95:
        total=str(sum(cfg['values']))
        alpha=ease((t-.95)/.30)
        d.text((692,1277),total,font=font(84,True),fill=(int(136+119*alpha),int(195+60*alpha),int(199+56*alpha)))
    else:d.text((751,1294),'…',font=font(62),fill=(150,209,217))
    card(d,(66,1540,1014,1660),(10,63,76),(46,132,149),r=25)
    d.text((98,1569),'デモ数値です。実績ではありません。',font=font(34,True),fill=(231,248,250))
    d.text((78,1735),'HUMAN REVIEW  /  PUBLICATION NOT APPROVED',font=font(23),fill=(155,203,215))
    d.rounded_rectangle((72,1801,1008,1815),radius=7,fill=(35,87,106))
    d.rounded_rectangle((72,1801,72+round(936*p),1815),radius=7,fill=(55,219,202))
    return im

def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def render(source,output,cfg):
    validate(cfg);source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    inf=probe(source);v=next(s for s in inf['streams'] if s['codec_type']=='video');a=next(s for s in inf['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],a['codec_name'])!=('h264',W,H,'aac'):raise ValueError('wrong source streams')
    if abs(float(inf['format']['duration'])-TOTAL)>.05:raise ValueError('wrong source duration')
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=f'[0:v]trim=start=0:duration={START},setpts=PTS-STARTPTS[head];[0:v]trim=start={END}:duration={TOTAL-END},setpts=PTS-STARTPTS[tail];[head][1:v][tail]concat=n=3:v=1:a=0[v]'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-t',str(TOTAL),'-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(round((END-START)*FPS)):
            proc.stdin.write(scene(i/FPS,cfg).tobytes())
        proc.stdin.close();err=proc.stderr.read().decode('utf-8','replace')
        if proc.wait():raise RuntimeError('ffmpeg failed: '+err[-3000:])
    except Exception:
        proc.kill();raise
    return {'file':str(output),'sha256':sha(output),'source_sha256':sha(source)}

def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--config',required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.output,json.loads(Path(a.config).read_text(encoding='utf8'))),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
