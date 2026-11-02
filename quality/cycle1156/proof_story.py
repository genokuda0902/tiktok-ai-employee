#!/usr/bin/env python3
"""Cycle1156: review-only, original 3-phase data provenance graphic.

Not original v33 source. Source media is never published or committed.
"""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES = {'ai':'#36d8cd','business':'#6dd1f5','money':'#e8c16b','learning':'#9abaff','health':'#75d5a7','food':'#efb97e','travel':'#80c8e8','beauty':'#efafd2','career':'#a2a5ff','life':'#a7dfb0'}
FPS = 30
X, Y, W, H = 55, 275, 820, 750
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ROWS = [('4月',12,8),('5月',16,9),('6月',18,12)]

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def totals(rows=ROWS):
    a = sum(r[1] for r in rows)
    b = sum(r[2] for r in rows)
    return a, b, a+b

def probe(path):
    data = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v = next(s for s in data['streams'] if s['codec_type']=='video')
    a = next(s for s in data['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['avg_frame_rate']) != ('h264',1080,1920,'30/1'):
        raise ValueError('Expected H264 1080x1920 30fps')
    if (a['codec_name'],int(a['sample_rate'])) != ('aac',48000):
        raise ValueError('Expected AAC 48kHz')
    duration = float(data['format']['duration'])
    return duration, int(v.get('nb_frames') or round(duration*FPS))

def validate(m, source, duration):
    if m.get('policy') != POLICY or m.get('asset_approval') != 'review_only_no_publication' or m.get('manual_post_only') is not True:
        raise ValueError('Fail closed: publication policy')
    if m.get('source_sha256') != sha256(source):
        raise ValueError('Source SHA mismatch')
    if m.get('genre') not in GENRES:
        raise ValueError('Unsupported genre')
    window = m.get('window')
    if not isinstance(window,list) or len(window)!=2 or any(type(x) not in (int,float) for x in window):
        raise ValueError('Invalid window')
    start,end = map(float,window)
    if not (0.5 <= start < end <= duration-.2 and 2.5 <= end-start <= 3.2):
        raise ValueError('Unsafe window')
    if X<30 or X+W>930 or Y<260 or Y+H>1050:
        raise ValueError('Header, chapter or caption protection violated')
    if totals()!=(46,29,75) or sum(x[1]+x[2] for x in ROWS)!=75:
        raise ValueError('Arithmetic invariant failed')
    return start,end

def fnt(n, bold=True):
    return ImageFont.truetype(FONT if bold else REG,n)

def rgb(s):
    return tuple(bytes.fromhex(s.lstrip('#')))

def frame(m,i,n):
    """One original procedural frame. No photos, private data, or copied reference art."""
    t = i/max(n-1,1)
    phase = min(2,int(t*3))
    accent = rgb(GENRES[m['genre']])
    im = Image.new('RGBA',(W,H),(7,22,41,255))
    d = ImageDraw.Draw(im)
    for yy in range(H):
        k = yy/H
        d.line((0,yy,W,yy),fill=(int(9+9*k),int(28+9*k),int(48+11*k),255))
    d.rounded_rectangle((3,3,W-4,H-4),radius=26,outline=accent+(220,),width=4)
    d.text((31,24),'SOURCE  →  FORMULA  →  RESULT',font=fnt(28),fill=(229,244,250,255))
    d.text((31,78),'架空データの出どころを順番に確認',font=fnt(29),fill=(191,215,228,255))
    for p,label in enumerate(('01  元データ','02  計算式','03  集計結果')):
        x=30+p*255
        selected=p==phase
        d.rounded_rectangle((x,142,x+238,204),radius=12,fill=(20,79,88,255) if selected else (16,43,61,255),outline=accent+(255,) if selected else (67,98,117,255),width=3 if selected else 2)
        d.text((x+14,151),label,font=fnt(25),fill=(247,252,253,255) if selected else (153,179,195,255))
    d.rounded_rectangle((27,230,W-27,648),radius=20,fill=(8,29,51,255),outline=(68,115,134,255),width=2)
    if phase==0:
        d.text((58,251),'月別の元データ（件）',font=fnt(38),fill=(245,250,252,255))
        for k,s in enumerate(('月','営業A','営業B','合計')):
            d.text((75+175*k,317),s,font=fnt(30),fill=accent+(255,))
        for k,(mo,a,b) in enumerate(ROWS):
            yy=373+k*67
            active = (t*3*3 >= k+.45)
            d.rounded_rectangle((56,yy-7,760,yy+52),radius=10,fill=(21,67,79,255) if active else (18,44,62,255))
            for j,s in enumerate((mo,str(a),str(b),str(a+b))):
                d.text((75+175*j,yy),s,font=fnt(31),fill=(245,251,253,255) if active else (157,183,197,255))
        d.text((58,595),'4月 12＋8＝20  /  5月 16＋9＝25  /  6月 18＋12＝30',font=fnt(23),fill=(198,226,235,255))
    elif phase==1:
        d.text((57,260),'各月を計算し、合計を検算',font=fnt(38),fill=(245,251,253,255))
        for k,(mo,a,b) in enumerate(ROWS):
            yy=340+k*85
            active=(t-1/3)*9 >= k+.3
            d.rounded_rectangle((54,yy-8,762,yy+67),radius=14,fill=(15,75,84,255) if active else (18,44,62,255),outline=accent+(180,) if active else (50,79,100,255),width=2)
            d.text((74,yy),f'{mo}   {a} ＋ {b} ＝ {a+b}',font=fnt(35),fill=(250,253,254,255) if active else (161,187,199,255))
        d.text((60,605),'20 ＋ 25 ＋ 30 ＝ 75',font=fnt(31),fill=accent+(255,))
    else:
        d.text((58,250),'営業A・営業Bの月別比較',font=fnt(37),fill=(246,251,252,255))
        d.rounded_rectangle((510,252,535,276),radius=4,fill=accent+(255,))
        d.text((544,248),'営業A',font=fnt(21),fill=(213,234,241,255))
        d.rounded_rectangle((635,252,660,276),radius=4,fill=(237,177,91,255))
        d.text((669,248),'営業B',font=fnt(21),fill=(213,234,241,255))
        prog = min(1,max(0,(t-2/3)*5))
        for k,(mo,a,b) in enumerate(ROWS):
            xx=145+k*215
            for j,val in enumerate((a,b)):
                height=int(val/20*224*prog)
                bx=xx+j*70
                d.rounded_rectangle((bx,560-height,bx+48,560),radius=7,fill=accent+(255,) if j==0 else (237,177,91,255))
                d.text((bx+5,570),str(val),font=fnt(23),fill=(226,239,244,255))
            d.text((xx+36,608),mo,font=fnt(27),fill=(226,239,244,255))
    d.rounded_rectangle((27,672,W-27,724),radius=12,fill=(12,59,68,255),outline=accent+(170,),width=2)
    d.text((47,677),'営業A 46  ＋  営業B 29  ＝  合計 75 件',font=fnt(28),fill=(240,252,251,255))
    alpha = min(1.0,(i+1)/5,(n-i)/5)
    if alpha<1:
        im.putalpha(im.getchannel('A').point(lambda a:int(a*alpha)))
    return im

def render(source,output,manifest,workdir):
    source,output,manifest,workdir = map(Path,(source,output,manifest,workdir))
    if source.resolve()==output.resolve():
        raise ValueError('Cannot overwrite source')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    duration,frames=probe(source)
    start,end=validate(m,source,duration)
    workdir.mkdir(parents=True,exist_ok=True)
    frame_dir=workdir/'overlay_frames';frame_dir.mkdir(exist_ok=True)
    n=round((end-start)*FPS)
    for i in range(n):
        frame(m,i,n).save(frame_dir/f'{i:04d}.png',compress_level=3)
    vf=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/TB[ov];[0:v][ov]overlay={X}:{Y}:format=auto:eof_action=pass:shortest=0[v]'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-i',str(frame_dir/'%04d.png'),'-filter_complex',vf,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-threads','4','-c:a','copy','-t',f'{duration:.6f}','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    dur,outframes=probe(output)
    if abs(dur-duration)>.05 or outframes!=frames:
        raise RuntimeError('Duration/frame mismatch')
    report={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),'duration':dur,'frames':outframes,'window':[start,end],'changed_overlay_frames':n,'genre':m['genre'],'arithmetic':{'A':46,'B':29,'total':75},'media_rights':'INHERITED_SOURCE_UNVERIFIED','Japanese_ASR':'NOT_VERIFIED','publication_approved':False}
    (workdir/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','workdir'):
        p.add_argument('--'+k,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.workdir),ensure_ascii=False,indent=2))
