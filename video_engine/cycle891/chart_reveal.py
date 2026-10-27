"""cycle891: three-stage data-grounded chart reveal, offline review ONLY.

Only fictional source values; inherited media stays local. No external upload/post.
Reusable for ten genres by supplying a three-period numeric dataset.
"""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
START=170
END=251
FRAMES=691
PATCH_X=80
PATCH_Y=525
PATCH_W=920
PATCH_H=710
PERIODS=('4月','5月','6月')
SERIES_A=(12,16,18)
SERIES_B=(8,9,12)
GENRES=('ai_productivity','beauty','romance_psychology','money_saving',
        'sales_business','career','health_lifestyle','trivia_science',
        'travel_food','product_lifestyle')
POLICY={'review_only':True,'publication_approved':False,
        'external_upload':False,'automatic_posting':False,
        'source_rights_reviewed':False,'fictional_data':True}
FONT_CANDIDATES=('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')

def font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():return ImageFont.truetype(path,size)
    raise RuntimeError('No usable font')

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    return h.hexdigest()

def validate_data(periods,a,b):
    if len(periods)!=3 or len(a)!=3 or len(b)!=3:raise ValueError('3 periods required')
    for p in periods:
        if not isinstance(p,str) or not 1<=len(p)<=8 or re.search(r'[@<>\r\n]|https?://|\d{8}',p):
            raise ValueError('unsafe period label')
    if any(type(x) is not int or x<0 or x>1000 for x in (*a,*b)):
        raise ValueError('unsafe values')
    return True

def validate_manifest(m,source):
    if any(m.get(k)!=v for k,v in POLICY.items()):raise ValueError('review policy mismatch')
    if m.get('source_sha256')!=sha256(source):raise ValueError('source hash mismatch')
    return True

def revealed(frame):
    if not 0<=frame<END-START:raise ValueError('frame outside scene')
    return tuple(min(1.,max(0.,(frame-i*25)/21.)) for i in range(3))

def displayed_totals(frame,a=SERIES_A,b=SERIES_B):
    p=revealed(frame)
    return (sum(round(x*f) for x,f in zip(a,p)),sum(round(x*f) for x,f in zip(b,p)))

def safe_geometry():
    return PATCH_X>=64 and PATCH_X+PATCH_W<=1016 and PATCH_Y>250 and PATCH_Y+PATCH_H<1390

def draw_patch(frame,periods=PERIODS,a=SERIES_A,b=SERIES_B):
    validate_data(periods,a,b)
    if not safe_geometry():raise ValueError('unsafe subtitle region')
    im=Image.new('RGBA',(PATCH_W,PATCH_H),(0,0,0,0))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((0,0,PATCH_W-1,PATCH_H-1),radius=30,
                        fill=(4,25,45,251),outline=(49,169,203,255),width=4)
    d.rounded_rectangle((28,26,400,84),radius=13,fill=(13,91,121,255))
    d.text((48,32),'完成見本 / データ可視化',font=font(31),fill='white')
    d.text((32,105),'架空データを3か月で比較',font=font(37),fill=(239,249,255))
    d.line((68,545,866,545),fill=(109,159,182),width=3)
    p=revealed(frame)
    for i,(name,va,vb,f) in enumerate(zip(periods,a,b,p)):
        x=114+i*270
        ha=round(320*va/20*f);hb=round(320*vb/20*f)
        if ha:d.rounded_rectangle((x,545-ha,x+63,545),radius=8,fill=(43,210,231))
        if hb:d.rounded_rectangle((x+74,545-hb,x+137,545),radius=8,fill=(255,181,90))
        d.text((x+18,555),name,font=font(33),fill=(236,247,253))
        if f>0:
            d.text((x+8,535-ha-43),str(round(va*f)),font=font(31),fill=(157,247,255))
            d.text((x+84,535-hb-43),str(round(vb*f)),font=font(31),fill=(255,220,164))
    ta,tb=displayed_totals(frame,a,b)
    d.rounded_rectangle((31,621,889,683),radius=14,fill=(14,65,91,255))
    d.ellipse((48,639,67,658),fill=(43,210,231))
    d.text((82,626),f'営業A {ta}',font=font(34),fill='white')
    d.ellipse((454,639,473,658),fill=(255,181,90))
    d.text((490,626),f'営業B {tb}',font=font(34),fill='white')
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of','json',str(path)],text=True))

def render(source,output,manifest,work,report):
    source=Path(source);output=Path(output);work=Path(work);report=Path(report)
    validate_manifest(json.loads(Path(manifest).read_text()),source)
    m=probe(source);v=next(s for s in m['streams'] if s['codec_type']=='video')
    a=next(s for s in m['streams'] if s['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',FRAMES):
        raise ValueError('unexpected video specification')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):
        raise ValueError('unexpected audio specification')
    work.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
    for i in range(END-START):draw_patch(i).save(work/f'{i:03d}.png',compress_level=2)
    filt=(f'[1:v]format=rgba,setpts=PTS+{START}/({FPS}*TB)[ov];'
          f"[0:v][ov]overlay={PATCH_X}:{PATCH_Y}:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-framerate',str(FPS),'-start_number','0','-i',str(work/'%03d.png'),
        '-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v',str(FRAMES),
        '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
        '-c:a','copy','-movflags','+faststart',str(output)],check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),
        '-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,timeout=120)
    result={'cycle':891,'source_sha256':sha256(source),'output_sha256':sha256(output),
            'modified_frame_range':[START,END-1],'full_av_decode':'PASS',
            'japanese_transcript_semantics':'UNVERIFIED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','work','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args();print(json.dumps(render(a.source,a.output,a.manifest,a.work,a.report),ensure_ascii=False))
