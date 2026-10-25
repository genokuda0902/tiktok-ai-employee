"""Original fictional desk scene: find repeatable work. Review-only, ten genres."""
import argparse, hashlib, json, math, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business','career','health_life','science','travel_food','product_life')
PALETTES={'ai_work':'#25BFD0','beauty':'#E36FA9','love_psychology':'#B889D8','money_saving':'#22A477','sales_business':'#25AFC5','career':'#5C83D6','health_life':'#59AD82','science':'#7288E0','travel_food':'#E79C52','product_life':'#B695D0'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FPS=30; FIRST=97; LAST=193; X=65; Y=455; W=950; H=690
LABELS=('日報の集計','定型メール','議事録の整理','予定の転記')
REVIEW='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'

def validate(genre):
    if genre not in GENRES: raise ValueError('unknown genre')
    if (X<48 or X+W>1032 or Y<400 or Y+H>1160):raise ValueError('unsafe scene region')
    if len(set(LABELS))!=4 or any(c.isdigit() for c in ''.join(LABELS)):raise ValueError('unsupported claims')
    if 'NOT_APPROVED' not in REVIEW:raise ValueError('publication gate')
    return True

def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def ease(v):
    v=max(0,min(1,v));return v*v*(3-2*v)

@lru_cache(maxsize=1)
def base():
    im=Image.new('RGB',(W,H));px=im.load()
    for y in range(H):
        for x in range(W):
            g=14*math.sin(x*.011+y*.003)+7*math.sin(x*.031)
            light=35*math.exp(-((x-790)**2/160000+(y-90)**2/100000))
            px[x,y]=(int(max(0,min(255,70+g+light))),int(max(0,min(255,58+g*.75+light*.75))),int(max(0,min(255,52+g*.5+light*.5))))
    return im

def frame(progress,genre='ai_work'):
    validate(genre);p=max(0,min(1,float(progress)));accent=PALETTES[genre]
    im=base().copy()
    d=ImageDraw.Draw(im)
    # Warm desk: original illustrated objects, no external photographs or user data.
    d.rounded_rectangle((42,35,645,512),radius=26,fill='#322D2B')
    d.rounded_rectangle((51,24,633,506),radius=23,fill='#E4D2B6')
    d.rounded_rectangle((68,30,615,502),radius=17,fill='#F5ECDD')
    for y in range(190,495,42):d.line((92,y,598,y),fill='#C5CBC5',width=2)
    d.line((112,125,112,498),fill='#D6A39A',width=4)
    d.rounded_rectangle((94,66,557,139),radius=16,fill='#183B47')
    d.text((118,102),'繰り返しの仕事を見つける',font=font(28,True),fill='white',anchor='lm')
    # Notes appear one at a time; last one receives an accent focus.
    for i,label in enumerate(LABELS):
        t=ease((p-i*.18)/.20)
        if t<=0:continue
        yy=184+i*72;slide=round((1-t)*165)
        active=(i==min(3,int(p*4)))
        d.rounded_rectangle((145+slide,yy-26,573+slide,yy+34),radius=12,fill='#F7FEFD' if active else '#E7E9E3',outline=accent if active else '#C5C8C3',width=5 if active else 2)
        d.rounded_rectangle((159+slide,yy-13,192+slide,yy+20),radius=7,fill=accent if active else '#B6C4C2')
        d.text((211+slide,yy+3),label,font=font(29,True),fill='#17333C',anchor='lm')
    # Pencil, mug and plant: small parallax accents.
    d.line((676,475,832,275),fill='#132E40',width=21)
    d.line((680,469,835,272),fill='#DAB47A',width=5)
    d.ellipse((727,78,903,246),fill='#342B28')
    d.ellipse((741,92,889,231),fill='#D8C3A6')
    d.ellipse((758,108,872,214),fill='#5E4037')
    d.arc((862,110,928,204),-80,90,fill='#D8C3A6',width=13)
    for i in range(6):
        xx=790+int(42*math.sin(i*2));yy=345+i*18
        d.ellipse((xx-26,yy-13,xx+26,yy+13),fill='#42644C')
    # Action cue appears only after the viewer has seen examples.
    if p>.52:
        q=ease((p-.52)/.26)
        d.rounded_rectangle((663,300,926,371),radius=15,fill='#123845')
        d.text((795,336),'まず１つ選ぶ',font=font(29,True),fill='white',anchor='mm')
        d.rounded_rectangle((663,383,663+round(263*q),391),radius=4,fill=accent)
    d.rounded_rectangle((45,559,905,648),radius=19,fill='#153944')
    d.text((475,603),'今の作業を、まず書き出す',font=font(34,True),fill='white',anchor='mm')
    d.text((928,671),'架空の業務例',font=font(17),fill='#F5E7D5',anchor='ra')
    return im

def cmd(args):return subprocess.run(args,check=True,capture_output=True,text=True)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def audio_md5(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).decode().strip()
def mae(a,b,t):
    import numpy as np
    def get(path):return np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-ss',str(t),'-i',str(path),'-frames:v','1','-vf','scale=270:480','-pix_fmt','rgb24','-f','rawvideo','-']),dtype=np.uint8).astype('int16')
    x,y=get(a),get(b)
    if len(x)!=270*480*3 or len(y)!=len(x):raise ValueError('invalid frame')
    return float(np.abs(x-y).mean())

def render(source,output,genre='ai_work'):
    validate(genre);source=Path(source);output=Path(output)
    p=probe(source);v=next(x for x in p['streams'] if x['codec_type']=='video');a=next(x for x in p['streams'] if x['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']),v['codec_name'],a['codec_name'])!=(1080,1920,'30/1',775,'h264','aac'):raise ValueError('wrong source')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle831_') as tmp:
        tmp=Path(tmp)
        for i in range(LAST-FIRST+1):frame(i/(LAST-FIRST),genre).save(tmp/f'f{i:03d}.jpg',quality=90)
        scene=tmp/'scene.mp4'
        cmd(['ffmpeg','-v','error','-y','-framerate','30','-i',str(tmp/'f%03d.jpg'),'-frames:v',str(LAST-FIRST+1),'-c:v','libx264','-preset','ultrafast','-crf','19','-threads','4','-pix_fmt','yuv420p',str(scene)])
        filt=f"[1:v]setpts=PTS-STARTPTS+{FIRST}/30/TB[ov];[0:v][ov]overlay=x={X}:y={Y}:eof_action=pass:enable='between(n,{FIRST},{LAST})',format=yuv420p[v]"
        cmd(['ffmpeg','-v','error','-y','-i',str(source),'-i',str(scene),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v','775','-c:v','libx264','-preset','ultrafast','-crf','22','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)])
    out=probe(output);vv=next(x for x in out['streams'] if x['codec_type']=='video');aa=next(x for x in out['streams'] if x['codec_type']=='audio')
    changed=mae(source,output,4.5);stable=mae(source,output,12.5)
    checks={'h264_vertical_30fps':(vv['codec_name'],vv['width'],vv['height'],vv['r_frame_rate'])==('h264',1080,1920,'30/1'),'775_frames':int(vv['nb_frames'])==775,'aac_48khz':(aa['codec_name'],aa['sample_rate'])==('aac','48000'),'audio_packets_unchanged':audio_md5(source)==audio_md5(output),'new_scene_visible':changed>12,'unchanged_scene_stable':stable<5,'full_av_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],capture_output=True).returncode==0}
    return {'cycle':831,'previous':830,'genre':genre,'frames_changed':LAST-FIRST+1,'frame_range':[FIRST,LAST],'checks':checks,'changed_mae':changed,'unchanged_mae':stable,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),'asset':'original fictional illustration','publication_approved':False,'auto_post':False,'audible_japanese_semantics_verified':False,'word_level_sync_verified':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--genre',choices=GENRES,default='ai_work');p.add_argument('--report');a=p.parse_args()
    r=render(a.source,a.output,a.genre)
    if a.report:Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False,indent=2))
    if not all(r['checks'].values()):raise SystemExit(1)
