"""cycle830: evidence-safe 10-genre image-led ending; REVIEW ONLY."""
from __future__ import annotations
import argparse,hashlib,json,math,subprocess,tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business','career','health_life','science','travel_food','product_life')
PALETTES={'ai_work':'#29C3D5','beauty':'#E36FA9','love_psychology':'#B889D8','money_saving':'#22A477','sales_business':'#25AFC5','career':'#5C83D6','health_life':'#59AD82','science':'#7288E0','travel_food':'#E79C52','product_life':'#B695D0'}
FPS=30
START,END=22.617,25.833333
X,Y,W,H=48,180,984,950
PHASES=('選ぶ','試す','続ける')
CTA='今日の改善をひとつ決めよう'
LABEL='小さな改善を、毎日の習慣に'
REVIEW_STATUS='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def validate(genre='ai_work'):
    if genre not in GENRES:raise ValueError('unknown genre')
    if X<48 or X+W>1032 or Y<160 or Y+H>1130:raise ValueError('subtitle overlap')
    if len(PHASES)!=3 or len(set(PHASES))!=3:raise ValueError('invalid stages')
    if any(c.isdigit() for c in CTA+LABEL):raise ValueError('unverified numerical claim')
    if 'NOT_APPROVED' not in REVIEW_STATUS:raise ValueError('review gate')
    return True

def font(n,bold=False):return ImageFont.truetype(BOLD if bold else FONT,n)
def ease(t):
    t=max(0,min(1,float(t)));return t*t*(3-2*t)

@lru_cache(maxsize=1)
def background():
    import numpy as np
    yy,xx=np.mgrid[0:H,0:W]
    light=65*np.exp(-((xx-825)**2/(2*330**2)+(yy-120)**2/(2*280**2)))
    wood=5*np.sin(xx*.011+yy*.003)+3*np.sin(xx*.087)+2*np.sin(yy*.043)
    vignette=np.clip(1-((xx-W/2)/(W*.93))**2-((yy-H/2)/(H*1.05))**2,.62,1)
    rgb=np.stack([np.clip((82+light+wood)*vignette,0,255),
                  np.clip((63+light*.67+wood*.73)*vignette,0,255),
                  np.clip((53+light*.42+wood*.48)*vignette,0,255)],axis=-1).astype('uint8')
    im=Image.fromarray(rgb,'RGB');d=ImageDraw.Draw(im)
    d.rounded_rectangle((700,22,946,300),radius=22,fill='#967967',outline='#C9A48B',width=9)
    d.rectangle((718,42,930,277),fill='#C4A8A0')
    d.rectangle((718,170,930,277),fill='#B18C7D')
    for bx,bw,bh in ((724,27,85),(763,45,132),(822,31,113),(864,40,151),(912,15,95)):
        d.rectangle((bx,277-bh,bx+bw,277),fill='#735E5D')
    d.line((823,42,823,277),fill='#C9A48B',width=10)
    d.rounded_rectangle((65,143,646,720),radius=30,fill='#382F2C')
    d.rounded_rectangle((75,125,638,704),radius=26,fill='#D3B994')
    d.rounded_rectangle((99,139,616,682),radius=21,fill='#F2E7D3')
    for line in range(300,660,47):d.line((151,line,575,line),fill='#C8CFCC',width=3)
    d.line((165,172,165,666),fill='#E2ABA0',width=4)
    d.rounded_rectangle((516,132,556,209),radius=18,outline='#7E8588',width=7)
    d.line((690,675,856,492),fill='#152F40',width=23)
    d.line((694,671,859,489),fill='#D5B26D',width=5)
    d.ellipse((735,305,929,485),fill='#352B29')
    d.ellipse((751,317,911,469),fill='#E5D2B5')
    d.ellipse((768,335,894,451),fill='#604037')
    d.arc((888,351,965,441),-90,90,fill='#E5D2B5',width=17)
    for j in range(6):
        ax=920+int(21*math.sin(j*1.7));ay=120+j*28
        d.ellipse((ax-24,ay-12,ax+20,ay+13),fill='#496347')
    return im

def frame(progress,genre='ai_work'):
    validate(genre);p=max(0,min(1,float(progress)));accent=PALETTES[genre]
    im=background()
    zoom=1+0.034*ease(p)
    zw,zh=round(W*zoom),round(H*zoom)
    if (zw,zh)!=(W,H):
        enlarged=im.resize((zw,zh),Image.Resampling.BICUBIC)
        ox=round((zw-W)*.55);oy=round((zh-H)*.43)
        im=enlarged.crop((ox,oy,ox+W,oy+H))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((118,187,609,281),radius=20,fill='#183B45')
    d.text((143,234),'明日の自分に残す',font=font(37,True),fill='white',anchor='lm')
    d.rounded_rectangle((129,326,589,630),radius=22,fill='#FFF7E9',outline='#C9BDA6',width=3)
    for i,label in enumerate(PHASES):
        y=379+i*85;shown=p>=i/3
        d.rounded_rectangle((165,y-25,219,y+28),radius=10,fill=accent if shown else '#D4D8D5')
        if shown:d.text((192,y),'✓',font=font(33,True),fill='#173643',anchor='mm')
        d.text((249,y),label,font=font(40,True),fill='#183A43' if shown else '#8D9696',anchor='lm')
        if shown:d.line((413,y+29,549,y+29),fill=accent,width=5)
    d.rounded_rectangle((40,834,944,932),radius=22,fill='#102F3A')
    d.text((492,883),CTA,font=font(42,True),fill='white',anchor='mm')
    d.rounded_rectangle((692,578,938,648),radius=18,fill='#153A46')
    d.text((815,614),LABEL,font=font(19,True),fill='white',anchor='mm')
    d.line((48,940,936,940),fill=accent,width=7)
    return im

def run(cmd):return subprocess.run(cmd,check=True,capture_output=True,text=True)
def probe(path):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
def audio_md5(path):return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).decode().strip()
def audio_mean_db(path):
    import re
    r=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-map','0:a:0','-af','volumedetect','-f','null','-'],capture_output=True,text=True)
    m=re.search(r'mean_volume:\\s*(-?[0-9.]+) dB',r.stderr)
    return float(m.group(1)) if r.returncode==0 and m else None

def render(source:Path,output:Path,genre='ai_work'):
    validate(genre)
    if not source.is_file():raise FileNotFoundError(source)
    inp=probe(source);v=next(s for s in inp['streams'] if s['codec_type']=='video')
    a=next(s for s in inp['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])!=(1080,1920,'30/1','h264') or a['codec_name']!='aac':raise ValueError('source media invalid')
    n=int(v['nb_frames']);first=round(START*FPS);last=n-1
    if n!=775 or last-first+1!=96:raise ValueError('unexpected scene boundary')
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='cycle830_') as tmp:
        tmp=Path(tmp)
        for i in range(n-first):frame(i/max(1,n-first-1),genre).save(tmp/f'frame_{i:03d}.jpg',quality=93)
        scene=tmp/'scene830.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','30','-i',str(tmp/'frame_%03d.jpg'),'-frames:v',str(n-first),'-c:v','libx264','-preset','ultrafast','-crf','19','-threads','4','-pix_fmt','yuv420p',str(scene)])
        filt=f"[0:v][1:v]overlay=x={X}:y={Y}:shortest=1:enable='gte(n,{first})',format=yuv420p[v]"
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-stream_loop','-1','-itsoffset',f'{START:.6f}','-i',str(scene),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v',str(n),'-c:v','libx264','-preset','ultrafast','-crf','22','-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)])
    out=probe(output);vv=next(s for s in out['streams'] if s['codec_type']=='video');aa=next(s for s in out['streams'] if s['codec_type']=='audio')
    mean=audio_mean_db(output)
    checks={'vertical_1080x1920_30fps':(vv['width'],vv['height'],vv['r_frame_rate'])==(1080,1920,'30/1'),
      '775_frames':int(vv['nb_frames'])==775,
      'h264_aac_48k':vv['codec_name']=='h264' and aa['codec_name']=='aac' and aa['sample_rate']=='48000',
      'audio_packets_preserved':audio_md5(source)==audio_md5(output),
      'non_silent_audio':mean is not None and -45<mean<0,
      'full_av_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],capture_output=True).returncode==0}
    return {'cycle':830,'previous':829,'genre':genre,'scene_seconds':[START,END],
       'frame_range_inclusive':[first,last],'frames_changed':n-first,'checks':checks,
       'audio_mean_db':mean,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
       'asset_provenance':'procedural_original_fictional','unverified_benefit_claim_removed':True,
       'audio_speech_semantics_verified':False,'word_level_subtitle_sync_verified':False,
       'reference_v33_compared':False,'smartphone_verified':False,
       'publication_approved':False,'auto_post':False,'review_only':True}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work');ap.add_argument('--report',type=Path)
    args=ap.parse_args();result=render(args.source,args.output,args.genre)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(result['checks'].values()):raise SystemExit(1)
