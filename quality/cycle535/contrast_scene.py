#!/usr/bin/env python3
"""cycle535 synthetic BEFORE/AFTER insert, review only; NOT v33 original."""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
W,H,FPS=1080,1920,30
START,END,DURATION=2.5,4.5,20.0
GENRES=("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(size,bold=True):return ImageFont.truetype(FONT if bold else REG,size)
def validate(cfg):
    if cfg.get('genre') not in GENRES:raise ValueError('unsupported genre')
    if cfg.get('rights')!='SYNTHETIC_OR_OWNER_APPROVED' or cfg.get('contains_private_data') is not False:raise ValueError('rights or privacy gate failed')
    if cfg.get('review_status')!='HUMAN_REVIEW' or cfg.get('publication')!='NOT_APPROVED':raise ValueError('human review gate failed')
    if cfg.get('claims_real_results') is not False:raise ValueError('unsupported results claims')
    for k in ('before','after','action'):
        v=cfg.get(k)
        if not isinstance(v,str) or not 2<=len(v)<=18 or any(c in v for c in '\n\r'):raise ValueError(f'invalid {k}')
    if not Path(FONT).is_file():raise FileNotFoundError(FONT)
    return True
def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)
def panel(d,xy,fill,outline,width=3,radius=26):
    d.rounded_rectangle(xy,radius=radius,fill=fill,outline=outline,width=width)
def scene(t,cfg):
    p=ease(t/(END-START))
    im=Image.new('RGB',(W,H),(8,21,36));d=ImageDraw.Draw(im)
    for y in range(H):
        if y%11==0:d.line((0,y,W,y),fill=(9,30,45),width=1)
    d.text((72,90),'AI時短ラボ  /  BEFORE → AFTER',font=font(36),fill=(199,240,245))
    d.text((76,235),'同じ作業、どう変わる？',font=font(67),fill='white')
    d.text((76,355),'操作イメージ / 架空データ',font=font(32,False),fill=(166,207,216))
    panel(d,(64,495,514,1405),(33,38,54),(171,82,104))
    panel(d,(566,495,1016,1405),(11,58,69),(64,211,195))
    d.text((94,538),'BEFORE',font=font(45),fill=(255,171,177))
    d.text((592,538),'AFTER',font=font(45),fill=(115,243,214))
    d.text((94,653),cfg['before'],font=font(40),fill=(245,248,249))
    d.text((592,653),cfg['after'],font=font(40),fill=(245,248,249))
    for i,label in enumerate(('① 転記','② 集計','③ グラフ')):
        y=800+i*152
        panel(d,(91,y,486,y+120),(55,56,73),(98,100,118),width=2,radius=16)
        d.text((119,y+34),label,font=font(36),fill=(232,229,235))
        if i<2:d.line((280,y+120,280,y+145),fill=(252,157,160),width=6)
    d.text((600,807),'① 指示を入力',font=font(36),fill=(228,249,246))
    d.text((600,947),'② 結果を確認',font=font(36),fill=(228,249,246))
    panel(d,(596,1110,987,1240),(21,97,101),(83,235,207),radius=18)
    d.rounded_rectangle((617,1178,962,1199),radius=9,fill=(32,67,79))
    d.rounded_rectangle((617,1178,617+round(345*ease((t-.22)/1.25)),1199),radius=9,fill=(104,243,206))
    d.text((620,1127),'人が最後に検証',font=font(32),fill=(235,255,249))
    x=519+round(16*(1-p))
    d.polygon([(x,1014),(x+35,1048),(x,1082)],fill=(255,215,111))
    d.text((84,1501),cfg['action'],font=font(43),fill=(249,253,255))
    d.text((83,1590),'※実演用の構成です。時間短縮の実績ではありません。',font=font(27,False),fill=(171,213,219))
    d.text((82,1750),'HUMAN REVIEW  /  PUBLICATION NOT APPROVED',font=font(25,False),fill=(142,180,190))
    d.rounded_rectangle((70,1810,1010,1823),radius=6,fill=(31,78,89))
    d.rounded_rectangle((70,1810,70+round(940*p),1823),radius=6,fill=(65,226,200))
    return im
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))
def render(source,output,cfg):
    validate(cfg);source=Path(source);output=Path(output)
    if not source.is_file():raise FileNotFoundError(source)
    meta=probe(source);v=next(s for s in meta['streams'] if s['codec_type']=='video');audio=[s for s in meta['streams'] if s['codec_type']=='audio']
    if (v['codec_name'],v['width'],v['height'])!=('h264',W,H) or not audio or audio[0]['codec_name']!='aac':raise ValueError('unsupported source')
    if abs(float(meta['format']['duration'])-DURATION)>.06:raise ValueError('duration mismatch')
    output.parent.mkdir(parents=True,exist_ok=True)
    filt=f'[0:v]trim=start=0:duration={START},setpts=PTS-STARTPTS[head];[0:v]trim=start={END}:duration={DURATION-END},setpts=PTS-STARTPTS[tail];[head][1:v][tail]concat=n=3:v=1:a=0[v]'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','pipe:0','-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-t',str(DURATION),'-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(round((END-START)*FPS)):proc.stdin.write(scene(i/FPS,cfg).tobytes())
        proc.stdin.close();err=proc.stderr.read().decode('utf8','replace')
        if proc.wait()!=0:raise RuntimeError(err[-3000:])
    except Exception:
        proc.kill();raise
    return {'file':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True);ap.add_argument('--config',required=True)
    args=ap.parse_args();print(json.dumps(render(args.source,args.output,json.loads(Path(args.config).read_text(encoding='utf8'))),ensure_ascii=False,indent=2))
