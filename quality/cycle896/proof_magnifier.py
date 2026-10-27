"""cycle896: review-only native-resolution evidence magnifier.

Uses only local inherited video pixels; never publishes, uploads or treats the
synthetic browser demo as actual ChatGPT/Excel. The genre-independent overlay
emphasizes a small source-UI status with native Japanese type and 3 steps.
"""
from __future__ import annotations
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

FPS=30
START=510
END=588
TOTAL=691
X,Y,W,H=66,180,948,1210
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES=('ai_productivity','beauty','romance_psychology','money_saving',
'sales_business','career','health_lifestyle','trivia_science','travel_food','product_lifestyle')
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False,
        'synthetic_ui':True,'real_service_demo':False}

def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def validate(m):
    if not isinstance(m,dict) or any(m.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Review-only policy must fail closed')
    if m.get('genre') not in GENRES:raise ValueError('Unknown genre')
    if not re.fullmatch('[a-f0-9]{64}',str(m.get('source_sha256',''))):raise ValueError('Source SHA required')
    roi=m.get('roi')
    if not isinstance(roi,list) or len(roi)!=4 or any(type(z) is not int for z in roi):raise ValueError('Invalid ROI')
    x0,y0,x1,y1=roi
    if not(0<=x0<x1<=1080 and 100<=y0<y1<=1400 and x1-x0>=100 and y1-y0>=60):
        raise ValueError('Unsafe screenshot crop')
    stages=m.get('stages')
    if not isinstance(stages,list) or len(stages)!=3:raise ValueError('Exactly 3 stages')
    for s in stages:
        if not isinstance(s,dict) or set(s)!={'title','label','value'}:raise ValueError('Bad stage keys')
        for k,lim in (('title',12),('label',22),('value',24)):
            v=s[k]
            if not isinstance(v,str) or not 1<=len(v)<=lim or re.search(r'https?://|@|[<>\r\n]|\d{8,}|(?:\d+\s*(?:分|時間|%|倍)\s*(?:短縮|削減|改善|増加))',v,re.I):
                raise ValueError('Unsafe or unverified display text')
    return True

def stage(frame):
    if type(frame) is not int or not 0<=frame<END-START:raise ValueError('Invalid frame')
    return min(2,frame//26)

def font(size,bold=False):
    p=BOLD if bold else FONT
    if not Path(p).is_file():raise RuntimeError('Noto Sans CJK font missing')
    return ImageFont.truetype(p,size)

def fit(d,xy,text,max_width,size,fill,bold=False):
    for sz in range(size,27,-1):
        f=font(sz,bold)
        if d.textbbox((0,0),text,font=f)[2]-d.textbbox((0,0),text,font=f)[0]<=max_width:
            d.text(xy,text,font=f,fill=fill)
            return sz
    raise ValueError('Text cannot fit')

def draw_patch(frame,m,crop):
    validate(m)
    if crop.mode!='RGB':crop=crop.convert('RGB')
    st=stage(frame)
    local=frame%26
    ease=min(1,local/9)
    ease=ease*ease*(3-2*ease)
    im=Image.new('RGBA',(W,H),(4,16,29,255))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((13,13,W-13,H-13),radius=35,fill=(5,25,43,255),outline=(66,199,225,255),width=4)
    d.rounded_rectangle((37,35,W-37,158),radius=22,fill=(9,67,91,255))
    fit(d,(65,53),'操作画面の要点を拡大',W-135,52,'white',True)
    d.text((65,178),'LOCAL DEMO / 架空データ・オフライン',font=font(29),fill=(148,211,231))
    # Original UI pixels are displayed in a fixed evidence window; no real-service claim.
    d.rounded_rectangle((39,237,W-39,790),radius=27,fill=(219,234,244,255),outline=(117,205,227,255),width=4)
    cw,ch=crop.size
    target_w=805
    target_h=370
    scale=min(target_w/cw,target_h/ch)*(0.88+0.12*ease)
    resized=crop.resize((int(cw*scale),int(ch*scale)),Image.Resampling.LANCZOS)
    resized=ImageEnhance.Contrast(resized).enhance(1.07)
    px=(W-resized.width)//2
    py=305+(target_h-resized.height)//2
    im.paste(resized,(px,py))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((66,253,W-66,297),radius=11,fill=(17,58,82,255))
    d.text((85,258),'実際のローカル模擬画面から切り出し',font=font(25),fill=(241,248,255))
    # 3-state native-resolution status card. Stage content is source-grounded.
    d.rounded_rectangle((41,818,W-41,1085),radius=24,fill=(10,57,80,255),outline=(61,206,222,255),width=3)
    s=m['stages'][st]
    d.rounded_rectangle((65,838,155,925),radius=21,fill=(79,232,220,255))
    d.text((91,847),str(st+1),font=font(54,True),fill=(5,28,42))
    fit(d,(179,842),s['title'],W-260,47,(255,255,255),True)
    fit(d,(78,939),s['label'],W-150,34,(174,217,233))
    fit(d,(78,994),s['value'],W-150,52,(100,246,226),True)
    for i in range(3):
        bx=66+i*290
        d.rounded_rectangle((bx,1122,bx+270,1138),radius=8,fill=(79,232,220,255) if i<=st else (53,84,105,255))
    d.text((61,1151),'架空の例 ／ 実サービスの操作ではありません',font=font(25),fill=(155,194,209))
    return im

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels','-of','json',str(p)],text=True))

def get_crop(source,frame,roi):
    cmd=['ffmpeg','-v','error','-y','-i',str(source),'-vf',f'select=eq(n\\,{frame})','-vsync','0','-frames:v','1','-f','image2pipe','-vcodec','png','-']
    import io
    data=subprocess.check_output(cmd,timeout=60)
    return Image.open(io.BytesIO(data)).convert('RGB').crop(tuple(roi))

def render(source,output,manifest,work,report):
    source,output,manifest,work,report=map(Path,(source,output,manifest,work,report))
    m=json.loads(manifest.read_text(encoding='utf-8'))
    validate(m)
    if sha256(source)!=m['source_sha256']:raise ValueError('Source SHA mismatch')
    p=probe(source)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    a=next(x for x in p['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',TOTAL):raise ValueError('Unexpected video geometry')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):raise ValueError('Unexpected audio format')
    if X<60 or X+W>1020 or Y<150 or Y+H>1450:raise ValueError('Subtitle collision')
    work.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
    crops=[get_crop(source,n,m['roi']) for n in (519,549,576)]
    for f in range(END-START):
        draw_patch(f,m,crops[stage(f)]).save(work/f'{f:03d}.png',compress_level=2)
    filt=(f'[1:v]format=rgba,setpts=PTS+{START}/({FPS}*TB)[ov];'
          f"[0:v][ov]overlay={X}:{Y}:shortest=0:repeatlast=0:eof_action=pass:format=auto:enable='between(n,{START},{END-1})'[v]")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(work/'%03d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-frames:v',str(TOTAL),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True,timeout=300)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=120)
    r={'cycle':896,'source_sha256':sha256(source),'output_sha256':sha256(output),'changed_frames':END-START,'full_decode':'PASS','review_only':True,'reference_original_mp4':'UNAVAILABLE','independent_japanese_asr':'UNVERIFIED','subtitle_semantics':'UNVERIFIED','rights':'UNVERIFIED','publication':'NOT_APPROVED'}
    report.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    return r

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for n in ('source','output','manifest','work','report'):ap.add_argument('--'+n,required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.work,a.report),ensure_ascii=False))
