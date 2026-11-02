#!/usr/bin/env python3
"""Cycle1154: rights-safe original desk/problem visual, review only.

The animated overlay is procedural illustration; no employee or stock images.
Original v33 renderer is not recovered. Source MP4 must be SHA-pinned.
"""
import argparse, hashlib, json, math, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRES={'ai':'#32d5d0','business':'#6dd1f5','money':'#e8c16b','learning':'#9abaff','health':'#75d5a7','food':'#efb97e','travel':'#80c8e8','beauty':'#efafd2','career':'#a2a5ff','life':'#a7dfb0'}
FPS=30
X,Y,W,H=46,445,988,630
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def probe(path):
    j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in j['streams'] if s['codec_type']=='video')
    a=next(s for s in j['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],int(v['width']),int(v['height']),v['avg_frame_rate'])!=('h264',1080,1920,'30/1'):raise ValueError('H264 1080x1920 30fps required')
    if (a['codec_name'],int(a['sample_rate']))!=('aac',48000):raise ValueError('AAC 48kHz required')
    return float(j['format']['duration']),int(v.get('nb_frames') or round(float(j['format']['duration'])*FPS))

def validate(m,source,duration):
    if m.get('policy')!=POLICY or m.get('asset_approval')!='review_only_no_publication' or m.get('manual_post_only') is not True:raise ValueError('Fail closed: approval policy')
    if m.get('source_sha256')!=sha256(source):raise ValueError('Source SHA mismatch')
    if m.get('genre') not in GENRES:raise ValueError('Unsupported genre')
    w=m.get('window')
    if not isinstance(w,list) or len(w)!=2 or any(type(x) not in (int,float) for x in w):raise ValueError('Bad window')
    start,end=map(float,w)
    if not (0.25<=start<end<=duration-.1 and 1.5<=end-start<=4):raise ValueError('Unsafe window')
    if Y+H>=1090 or X+W>1080:raise ValueError('Caption / NEXT protection violated')
    return start,end

def fnt(size,bold=True):return ImageFont.truetype(FONT if bold else REG,size)

def rgb(h):return tuple(bytes.fromhex(h.lstrip('#')))

def frame(m,i,n):
    """Return a 988x630 RGBA visual with original desk illustration and staged task labels."""
    accent=rgb(GENRES[m['genre']]); t=i/max(1,n-1)
    im=Image.new('RGBA',(W,H),(9,25,44,255))
    d=ImageDraw.Draw(im)
    # Full-height opaque panel prevents all three inherited list rows ghosting.
    for yy in range(H):
        gl=max(0,1-abs(yy-100)/600)
        d.line((0,yy,W,yy),fill=(int(9+6*gl),int(25+16*gl),int(44+17*gl),255))
    d.rounded_rectangle((3,3,W-4,H-4),radius=28,outline=accent+(230,),width=4)
    d.text((33,21),'BEFORE / 繰り返し作業',font=fnt(28),fill=(235,244,251,255))
    d.line((34,70,W-36,70),fill=accent+(145,),width=2)
    # Stylized desk perspective, warm papers, clock: fully original graphics.
    d.polygon([(52,354),(505,354),(568,437),(27,437)],fill=(36,62,76,255))
    d.line((30,437,560,437),fill=(111,154,167,255),width=4)
    sway=int(3*math.sin(2*math.pi*t*2))
    for k in range(4):
        xx=100+k*15+sway;yy=245-k*24
        d.rounded_rectangle((xx+7,yy+8,xx+287,yy+92),radius=9,fill=(2,14,27,255))
        d.rounded_rectangle((xx,yy,xx+280,yy+82),radius=9,fill=(225-8*k,235-6*k,236-5*k,255))
        for line in range(3):d.line((xx+27,yy+25+line*17,xx+218-line*21,yy+25+line*17),fill=(94,123,134,255),width=4)
    cx,cy=408,186
    d.ellipse((cx-72,cy-72,cx+72,cy+72),fill=(16,37,56,255),outline=accent+(255,),width=7)
    for k in range(12):
        a=2*math.pi*k/12
        d.ellipse((cx+57*math.sin(a)-3,cy-57*math.cos(a)-3,cx+57*math.sin(a)+3,cy-57*math.cos(a)+3),fill=(206,230,235,255))
    a=2*math.pi*(.16+.25*t)
    d.line((cx,cy,cx+47*math.sin(a),cy-47*math.cos(a)),fill=(246,191,109,255),width=7)
    d.line((cx,cy,cx-25*math.cos(a),cy-25*math.sin(a)),fill=(220,236,238,255),width=5)
    d.ellipse((cx-7,cy-7,cx+7,cy+7),fill=(250,253,253,255))
    items=['データの集計','報告メール','資料の整形']
    for k,s in enumerate(items):
        yy=92+k*113
        active=(t*3>=k+.15)
        col=accent if active else (100,126,140)
        fill=(15,70,79,255) if active else (19,44,62,255)
        d.rounded_rectangle((582,yy,954,yy+91),radius=18,fill=fill,outline=col+(255,),width=4 if active else 2)
        d.rounded_rectangle((600,yy+16,657,yy+74),radius=12,fill=col+(255,))
        d.text((610,yy+22),f'{k+1:02d}',font=fnt(23),fill=(6,23,39,255))
        d.text((674,yy+19),s,font=fnt(34),fill=(242,249,253,255) if active else (160,184,196,255))
    d.rounded_rectangle((31,482,W-31,595),radius=19,fill=(9,42,57,255),outline=accent+(160,),width=2)
    d.text((61,494),'見える化  →  1つ選ぶ  →  試してみる',font=fnt(32),fill=(235,249,250,255))
    d.text((61,549),'実例ではなく、繰り返し作業を整理するための図解',font=fnt(22,False),fill=(195,218,229,255))
    a=min(1,i/5,(n-1-i)/5)
    if a<1:im.putalpha(im.getchannel('A').point(lambda v:int(v*max(0,a))))
    return im

def render(source,output,manifest,workdir):
    source,output,manifest,workdir=map(Path,(source,output,manifest,workdir))
    if source.resolve()==output.resolve():raise ValueError('Source overwrite forbidden')
    m=json.loads(manifest.read_text(encoding='utf-8'))
    duration,nframes=probe(source);start,end=validate(m,source,duration)
    workdir.mkdir(parents=True,exist_ok=True)
    frames_dir=workdir/'overlay_frames';frames_dir.mkdir(exist_ok=True)
    n=round((end-start)*FPS)
    for i in range(n):frame(m,i,n).save(frames_dir/f'{i:04d}.png',compress_level=3)
    vf=f'[1:v]format=rgba,setpts=PTS-STARTPTS+{start}/TB[ov];[0:v][ov]overlay={X}:{Y}:format=auto:eof_action=pass:shortest=0[v]'
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-i',str(frames_dir/'%04d.png'),'-filter_complex',vf,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-threads','4','-c:a','copy','-t',f'{duration:.6f}','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    dur,outframes=probe(output)
    if abs(dur-duration)>.05 or outframes!=nframes:raise RuntimeError('Duration/frame mismatch')
    report={'policy':POLICY,'source_sha256':sha256(source),'output_sha256':sha256(output),'duration':dur,'frames':outframes,'window':[start,end],'changed_overlay_frames':n,'genre':m['genre'],'media_rights':'INHERITED_SOURCE_UNVERIFIED','Japanese_ASR':'NOT_VERIFIED','publication_approved':False}
    (workdir/'render_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for k in ('source','output','manifest','workdir'):p.add_argument('--'+k,required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.manifest,a.workdir),ensure_ascii=False,indent=2))
