"""cycle861: review-only, source-pinned cross-genre real-UI evidence montage.

This is a reimplementation. No private footage is stored in GitHub. No publishing.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
ACCENTS = {'ai_work':'#35D7EA','sales_business':'#4BE5AC','beauty':'#FF90BD',
           'romance':'#FF83A9','saving':'#56E7B3','career':'#86A6FF',
           'wellness':'#63E6BD','science':'#68D6FF','travel_food':'#F5BA79',
           'product_comparison_lifestyle':'#A9B6FF'}
POLICY = {'review_only':True,'publication_approved':False,'automatic_posting':False,
          'external_upload':False,'source_rights_reviewed':False,
          'contains_personal_data':False,'fictional_workflow_example':True}
FPS = 30
TOTAL = 691
START = 89
N = 81
ROI = (36,350,1000,1100)
# Source footage comes from the previous review-only MP4, NOT approved media.
# x,y,w,h in original 1080x1920 frame; each segment is a separate real UI recording.
CLIPS = (
    {'start':336,'crop':(80,555,775,475),'label':'集計を繰り返す','type':'Calc'},
    {'start':507,'crop':(85,575,770,425),'label':'資料を作り直す','type':'Writer'},
)
FONT_PATH = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def font(size):
    return ImageFont.truetype(FONT_PATH,size) if Path(FONT_PATH).exists() else ImageFont.load_default()

def ease(t):
    t=min(1.,max(0.,float(t)))
    return t*t*(3-2*t)

def validate_policy(manifest,source,output,genre):
    source,output=Path(source),Path(output)
    if genre not in GENRES:raise ValueError('unknown genre')
    if not source.is_file():raise FileNotFoundError(source)
    if output.exists() or output.resolve()==source.resolve():raise ValueError('refuse overwrite')
    if manifest != {**POLICY,'source_sha256':digest(source)}:raise ValueError('manifest/hash/policy mismatch')
    return source,output

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def validate_streams(path):
    ss=probe(path)['streams']
    v=next((s for s in ss if s['codec_type']=='video'),None)
    a=next((s for s in ss if s['codec_type']=='audio'),None)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v.get('nb_frames') or 0),a['codec_name'],a['sample_rate'])!=('h264',1080,1920,'30/1',TOTAL,'aac','48000'):
        raise ValueError('expected 691-frame 1080x1920 H264 30fps AAC 48kHz')

def extract_clips(source,workdir):
    """Two distinct 1.4s excerpts from previously recorded, fictional software use."""
    dirs=[]
    for index,clip in enumerate(CLIPS):
        d=Path(workdir)/f'clip_{index}';d.mkdir()
        x,y,w,h=clip['crop']
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss',str(clip['start']/FPS),
             '-i',str(source),'-frames:v','44','-vf',f'crop={w}:{h}:{x}:{y},scale=760:510:flags=lanczos',
             '-start_number','0',str(d/'frame_%03d.jpg')]
        subprocess.run(cmd,check=True,timeout=100)
        paths=sorted(d.glob('frame_*.jpg'))
        if len(paths)<40:raise RuntimeError(f'insufficient frames in {index}: {len(paths)}')
        dirs.append(paths)
    return dirs

def draw_scene(frame,images,genre='ai_work'):
    """Render one original, visually active picture region; all captions stay untouched."""
    if not 0<=frame<N:raise ValueError('invalid frame')
    if genre not in GENRES:raise ValueError('unknown genre')
    w,h=840,875;accent=ACCENTS[genre]
    im=Image.new('RGB',(w,h),(7,19,31));d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/max(1,h-1)
        d.line((0,y,w,y),fill=(round(7+9*t),round(19+13*t),round(31+17*t)))
    glow=Image.new('RGBA',(w,h),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((380,-250,1000,410),fill=(32,154,199,55))
    glow=glow.filter(ImageFilter.GaussianBlur(90))
    im=Image.alpha_composite(im.convert('RGBA'),glow)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((22,22,w-22,h-22),radius=33,outline=(43,91,110),width=3)
    d.text((54,52),'毎日の「繰り返し」を見つける',font=font(42),fill='#F7FCFF')
    d.text((55,120),'実際の操作画面から、2つの仕事を確認',font=font(26),fill='#A6C7D5')
    # First 40 frames: Calc; last 41: Writer. A short blend smooths the cut.
    if frame<39:idx=0;local=frame;mix=0.0
    elif frame<=44:idx=0;local=frame;mix=ease((frame-38)/7)
    else:idx=1;local=frame-41;mix=1.0
    def shot(which,pos):
        seq=images[which];j=max(0,min(len(seq)-1,pos))
        with Image.open(seq[j]) as img: return img.convert('RGB').copy()
    a=shot(0,min(frame,43));b=shot(1,max(0,frame-39))
    # real footage is never synthesized or replaced with an imitation UI.
    visual=Image.blend(a,b,mix)
    # Ken Burns movement: gentle, not fake cursor or simulated app behavior.
    zoom=1+0.022*ease((frame%41)/40)
    if zoom>1:
        W,H=visual.size;cw=round(W/zoom);ch=round(H/zoom)
        left=(W-cw)//2;top=(H-ch)//2
        visual=visual.crop((left,top,left+cw,top+ch)).resize((W,H),Image.Resampling.LANCZOS)
    shadow=Image.new('RGBA',(w,h),(0,0,0,0));s=ImageDraw.Draw(shadow)
    s.rounded_rectangle((35,194,805,724),radius=29,fill=(0,0,0,150))
    shadow=shadow.filter(ImageFilter.GaussianBlur(15))
    im=Image.alpha_composite(im,shadow)
    # rounded-corner mask for actual footage
    mask=Image.new('L',visual.size,0);md=ImageDraw.Draw(mask)
    md.rounded_rectangle((0,0,759,509),radius=22,fill=255)
    im.paste(visual,(40,190),mask)
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((40,190,800,700),radius=22,outline=accent,width=4)
    d.rounded_rectangle((55,210,280,259),radius=18,fill=(7,32,45))
    d.text((72,213),'実画面 / 架空データ',font=font(24),fill='#F5FAFD')
    # distinct informational label, cross-genre reusable data (not fabricated result)
    label='集計を繰り返す' if frame<=41 else '資料を作り直す'
    number='01' if frame<=41 else '02'
    d.rounded_rectangle((40,725,800,816),radius=22,fill=(13,48,63),outline=(52,122,145),width=2)
    d.text((67,738),number,font=font(51),fill=accent)
    d.text((164,745),label,font=font(43),fill='#FFFFFF')
    # Full-bleed replacement masks the old inset AND its leftover footer,
    # while preserving the actual subtitle block at y>=1490.
    W,H=ROI[2:];canvas=Image.new('RGB',(W,H),(7,19,31));cd=ImageDraw.Draw(canvas)
    for yy in range(H):
        t=yy/max(1,H-1)
        cd.line((0,yy,W,yy),fill=(round(7+7*t),round(19+11*t),round(31+13*t)))
    canvas.paste(im.convert('RGB'),((W-w)//2,12))
    cd=ImageDraw.Draw(canvas)
    cd.rounded_rectangle((118,922,W-118,1043),radius=27,fill=(15,57,74),outline=accent,width=3)
    cd.text((170,955),'まずは1つ、作業を書き出す',font=font(43),fill='#FFFFFF')
    return canvas

def frames_to_disk(folder,images,genre='ai_work'):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    if any(folder.iterdir()):raise ValueError('refuse nonempty output frame directory')
    for i in range(N):draw_scene(i,images,genre).save(folder/f'montage_{i:03d}.png')

def render(source,output,manifest,genre='ai_work'):
    source,output=validate_policy(manifest,source,output,genre)
    validate_streams(source)
    with tempfile.TemporaryDirectory(prefix='cycle861_') as tmp:
        clips=extract_clips(source,tmp)
        frames=Path(tmp)/'frames';frames_to_disk(frames,clips,genre)
        # Source frames 89..169 correspond to scene 2 (2.967–5.667s).
        filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
              f'[0:v][new]overlay=x={ROI[0]}:y={ROI[1]}:'
              f"enable='between(n,{START},{START+N-1})':eof_action=pass:repeatlast=0:format=auto[v]")
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
             '-framerate','30','-start_number','0','-i',str(frames/'montage_%03d.png'),
             '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30',
             '-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=220)
    validate_streams(output)
    return {'source_sha256':digest(source),'output_sha256':digest(output),
            'start_frame':START,'end_frame':START+N-1,'frames_replaced':N,
            'genre':genre,'input_types':['real Calc UI recording','real Writer UI recording'],
            'fictional_data':True,'source_rights_reviewed':False,'policy':POLICY}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
    p.add_argument('--genre',default='ai_work');a=p.parse_args()
    result=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
    Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))