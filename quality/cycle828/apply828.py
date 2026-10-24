"""cycle828: original fictional recommendation-to-action animation, review only.

A genre-neutral scene overlay. Does not use real app screens or private media.
The source video is never uploaded to GitHub; CI reconstructs its own
fictional Japanese voice and subtitle source using the existing workflow.
"""
from __future__ import annotations
import argparse,hashlib,json,math,subprocess,tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter

GENRES=('ai_work','beauty','love_psychology','money_saving','sales_business',
        'career','health_life','science','travel_food','product_life')
PALETTES={'ai_work':'#20C3DB','beauty':'#E36FA9','love_psychology':'#B889D8',
          'money_saving':'#22A477','sales_business':'#25AFC5','career':'#5C83D6',
          'health_life':'#59AD82','science':'#7288E0','travel_food':'#E79C52',
          'product_life':'#B695D0'}
W,H,FPS=952,648,30
START,END=16.150,19.383
X,Y=64,482
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STEPS=('AIの提案を確認','予定に落とし込む','文章を整える','実行準備が完了')
NOTICE='架空の業務例・実在するサービス画面ではありません'

def validate(genre='ai_work',start=START,end=END):
    if genre not in GENRES:raise ValueError('unknown genre')
    if abs(start-START)>0.001 or abs(end-END)>0.001:raise ValueError('unexpected scene range')
    if X<50 or X+W>1030 or Y<420 or Y+H>1190:raise ValueError('subtitle unsafe')
    if len(STEPS)!=4 or '架空' not in NOTICE:raise ValueError('review provenance missing')
    return True

def f(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)

@lru_cache(maxsize=1)
def _base():
    # Original warm desk scene: deterministic gradients, lighting and laptop.
    im=Image.new('RGB',(W,H));px=im.load()
    for y in range(H):
        for x in range(W):
            shade=math.sin(x*.018+y*.004)*2.7+math.sin(y*.11)*1.8
            glow=max(0,1-math.hypot(x-780,y-120)/780)*38
            px[x,y]=(int(27+glow*.65+shade),int(37+glow*.39+shade),int(44+glow*.21+shade))
    for i,(cx,cy,r) in enumerate(((110,120,48),(730,70,65),(875,315,38))):
        light=Image.new('RGBA',(W,H));ld=ImageDraw.Draw(light)
        ld.ellipse((cx-r,cy-r,cx+r,cy+r),fill=(238,174,85,90 if i!=1 else 130))
        light=light.filter(ImageFilter.GaussianBlur(r*.75))
        im=Image.alpha_composite(im.convert('RGBA'),light).convert('RGB')
    d=ImageDraw.Draw(im)
    d.polygon(((0,450),(952,406),(952,648),(0,648)),fill='#3A3430')
    for k in range(8):
        yy=465+k*28;d.line((0,yy,952,yy-37),fill='#53443B',width=2)
    d.rounded_rectangle((100,40,855,502),radius=28,fill='#0B1921',outline='#6C8588',width=5)
    d.rounded_rectangle((119,58,836,473),radius=18,fill='#112B36')
    d.polygon(((120,473),(836,473),(910,535),(50,535)),fill='#8B9290')
    d.polygon(((50,535),(910,535),(865,552),(88,552)),fill='#424B4C')
    d.rounded_rectangle((155,93,799,429),radius=17,fill='#EAF2F0')
    d.rounded_rectangle((155,93,799,148),radius=17,fill='#174B5D')
    d.rectangle((155,132,799,148),fill='#174B5D')
    d.text((184,121),'今日の仕事を、次の行動に変える',font=f(29,True),fill='white',anchor='lm')
    d.text((184,177),'AIの提案',font=f(27,True),fill='#173A45')
    d.rounded_rectangle((179,215,755,270),radius=12,fill='#D7E6E6')
    d.text((203,242),'「優先事項を整理して、まず一つ実行」',font=f(24),fill='#26454D',anchor='lm')
    return im

def frame(progress,genre='ai_work'):
    validate(genre)
    p=max(0.,min(1.,float(progress)))
    accent=PALETTES[genre]
    im=_base().copy()
    d=ImageDraw.Draw(im)
    states=(p>=.17,p>=.42,p>=.67,p>=.89)
    for i,(label,done) in enumerate(zip(STEPS,states)):
        yy=298+i*35
        if i==3:break
        d.rounded_rectangle((180,yy,757,yy+31),radius=9,fill='#D7F2ED' if done else '#EDF1F1')
        d.rounded_rectangle((192,yy+5,214,yy+27),radius=6,fill=accent if done else '#C2D0D2')
        if done:d.text((203,yy+16),'✓',font=f(18,True),fill='#073543',anchor='mm')
        d.text((231,yy+16),label,font=f(22,True),fill='#16404A' if done else '#849A9E',anchor='lm')
    if states[3]:
        d.rounded_rectangle((510,386,756,419),radius=10,fill=accent)
        d.text((633,402),'✓  実行準備OK',font=f(21,True),fill='#10313C',anchor='mm')
    else:
        d.text((635,401),'確認中…',font=f(20),fill='#6E9399',anchor='mm')
    pts=((610,253),(210,316),(210,353),(635,401))
    phase=min(3,int(p*4));cx,cy=pts[phase]
    d.polygon(((cx,cy),(cx+17,cy+32),(cx+23,cy+21),(cx+36,cy+18)),fill='#F8FDFF')
    d.line(((cx,cy),(cx+17,cy+32),(cx+23,cy+21),(cx+36,cy+18),(cx,cy)),fill='#153C4B',width=2)
    d.rounded_rectangle((23,568,929,630),radius=14,fill='#102D38')
    d.text((42,589),STEPS[phase],font=f(26,True),fill='#FFFFFF')
    d.text((910,590),f'{phase+1}/4',font=f(23,True),fill=accent,anchor='rm')
    d.text((476,616),NOTICE,font=f(17),fill='#B5CCD1',anchor='mm')
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def md5_audio(path):
    return subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c','copy','-f','md5','-']).decode().strip()

def render(source:Path,output:Path,genre='ai_work'):
    validate(genre)
    if not source.is_file():raise FileNotFoundError(source)
    info=probe(source)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=next(s for s in info['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'],v['codec_name'])!=(1080,1920,'30/1','h264') or a['codec_name']!='aac':
        raise ValueError('invalid source media')
    if float(info['format']['duration'])<END:raise ValueError('source too short')
    n=round((END-START)*FPS)
    output.parent.mkdir(parents=True,exist_ok=True)
    # Two-stage FFmpeg avoids rawvideo framesync stalls in unattended CI.
    with tempfile.TemporaryDirectory(prefix='cycle828_') as td:
        overlay_path=Path(td)/'scene828.mp4'
        for i in range(n):
            frame(i/max(1,n-1),genre).save(Path(td)/f'frame_{i:03d}.jpg',quality=94)
        build=['ffmpeg','-hide_banner','-loglevel','error','-y',
               '-framerate',str(FPS),'-i',str(Path(td)/'frame_%03d.jpg'),
               '-frames:v',str(n),'-c:v','libx264','-preset','ultrafast',
               '-crf','18','-threads','4','-pix_fmt','yuv420p',str(overlay_path)]
        subprocess.run(build,check=True,capture_output=True)
        filter_complex=f"[0:v][1:v]overlay=x={X}:y={Y}:shortest=1:enable='between(t,{START:.3f},{END:.3f})',format=yuv420p[v]"
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
             '-stream_loop','-1','-itsoffset',f'{START:.6f}','-i',str(overlay_path),
             '-filter_complex',filter_complex,'-map','[v]','-map','0:a:0',
             '-frames:v',str(v['nb_frames']),'-c:v','libx264','-preset','ultrafast',
             '-crf','22','-threads','4','-pix_fmt','yuv420p','-c:a','copy',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,capture_output=True)
    o=probe(output)
    vv=next(s for s in o['streams'] if s['codec_type']=='video')
    aa=next(s for s in o['streams'] if s['codec_type']=='audio')
    checks={'video_1080x1920_30fps':(vv['width'],vv['height'],vv['r_frame_rate'])==(1080,1920,'30/1'),
        '775_frames_preserved':int(vv['nb_frames'])==int(v['nb_frames']),
        'h264_aac_48k':vv['codec_name']=='h264' and aa['codec_name']=='aac' and aa['sample_rate']=='48000',
        'audio_bitstream_unchanged':md5_audio(source)==md5_audio(output),
        'full_av_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],capture_output=True).returncode==0}
    return {'cycle':828,'prior_cycle':827,'scene':[START,END],'frames_changed':n,'genre':genre,
      'checks':checks,'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
      'fictional_procedural_assets':True,'narration_content_independently_verified':False,
      'word_level_caption_sync_verified':False,'reference_v33_direct_comparison':False,
      'smartphone_verified':False,'publication_approved':False,'review_only':True,'auto_post':False}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--genre',choices=GENRES,default='ai_work')
    ap.add_argument('--report',type=Path)
    args=ap.parse_args()
    result=render(args.source,args.output,args.genre)
    if args.report:
        args.report.parent.mkdir(parents=True,exist_ok=True)
        args.report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if not all(result['checks'].values()):raise SystemExit(1)
