"""Review-only, offline scene-safe dip and Japanese caption repair.

Run on SHA-pinned private source; never uploads user MP4, posts or merges.
Actual local verification and MP4 are provided separately in review package.
"""
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

CAPTIONS=[
("AIで仕事を早くするなら、","最初の一歩が大事。"),
("まず、繰り返している作業を","書き出す。"),
("次に、完成形の見本を","用意する。"),
("指示は、目的と条件を","具体的に伝える。"),
("最初の出力は、","必ず自分で確かめる。"),
("違いがあれば、修正点を","一つずつ伝える。"),
("使える指示は、","テンプレートに残す。"),
("小さな時短を、","毎日の習慣にしよう。")]
PALETTES={'ai_work':'#36ddcb','money':'#ffd166','health':'#72e3b0',
'beauty':'#ffb7d5','education':'#7eb9ff','travel':'#f3c777',
'food':'#ffad79','lifestyle':'#b8a5ff','psychology':'#9cdeef','business':'#81ddf7'}
DIP_FACTORS={-2:.72,-1:.30,0:.30,1:.72}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.run(['ffprobe','-v','error','-show_streams','-show_chapters',
    '-show_format','-of','json',str(path)],capture_output=True,text=True,check=True).stdout)

def starts(path):
    p=probe(path)
    ch=p['chapters']
    if len(ch)!=8 or abs(float(ch[-1]['end_time'])-22.5)>.03: raise ValueError('chapters')
    x=[round(float(c['start_time'])*30) for c in ch]
    if x[0]!=0 or x!=sorted(set(x)): raise ValueError('chapter starts')
    return x

def caption_plate(index,genre='ai_work'):
    if genre not in PALETTES or not 0<=index<8: raise ValueError('genre or scene')
    accent=PALETTES[genre]
    im=Image.new('RGBA',(1080,246),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle((44,0,1036,245),radius=25,fill=(6,13,27,255),outline=(75,125,143,255),width=3)
    d.rounded_rectangle((57,24,67,218),radius=5,fill=accent)
    d.text((92,15),f'今日のポイント   {index+1:02d} / 08',font=ImageFont.truetype(FONT_REG,24),fill=(155,205,218,255))
    f=ImageFont.truetype(FONT,64)
    for j,line in enumerate(CAPTIONS[index]):
        b=d.textbbox((0,0),line,font=f); w=b[2]-b[0]
        if w>888: raise ValueError('caption overflow')
        d.text(((1080-w)//2,61+j*78),line,font=f,fill='#ffffff' if j==0 else accent)
    return im

def dip_roi(frame,offset):
    if offset not in DIP_FACTORS: raise ValueError('invalid cut offset')
    return cv2.convertScaleAbs(frame,alpha=DIP_FACTORS[offset],beta=0)

def render(source,dest,expected_sha,genre='ai_work'):
    source,dest=Path(source),Path(dest)
    if sha(source)!=expected_sha: raise ValueError('source SHA mismatch')
    p=probe(source); v=next(s for s in p['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'],v['avg_frame_rate'])!=(1080,1920,'30/1'): raise ValueError('source format')
    cuts=starts(source)[1:]
    plates=[]
    for i in range(8):
        rgba=np.asarray(caption_plate(i,genre),dtype=np.uint8)
        plates.append((cv2.cvtColor(rgba[:,:,:3],cv2.COLOR_RGB2BGR),rgba[:,:,3:4].astype(np.float32)/255))
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('source decode')
    dest.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pixel_format','bgr24',
    '-video_size','1080x1920','-framerate','30','-i','pipe:0','-i',str(source),
    '-map','0:v:0','-map','1:a:0','-map_metadata','1','-map_chapters','1',
    '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
    '-frames:v','675','-c:a','copy','-metadata:s:a:0','language=jpn',
    '-movflags','+faststart',str(dest)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    scene=0; changed=[]
    try:
        for n in range(675):
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'truncated at {n}')
            if scene<7 and n>=cuts[scene]:scene+=1
            for cut in cuts:
                offset=n-cut
                if offset in DIP_FACTORS:
                    frame[:1320]=dip_roi(frame[:1320],offset);changed.append(n);break
            bgr,alpha=plates[scene]; roi=frame[1370:1616]
            frame[1370:1616]=(roi.astype(np.float32)*(1-alpha)+bgr.astype(np.float32)*alpha).astype(np.uint8)
            proc.stdin.write(frame.tobytes())
        ok,_=cap.read()
        if ok:raise RuntimeError('source too long')
    except Exception:
        proc.kill();raise
    finally:
        cap.release();proc.stdin.close();err=proc.stderr.read().decode(errors='replace');rc=proc.wait()
    if rc:raise RuntimeError(f'ffmpeg failed: {err[-1000:]}')
    return {'source_sha256':expected_sha,'output_sha256':sha(dest),'frames':675,
    'cut_frames':cuts,'modified_frames':changed,'genre':genre,'approval':'HUMAN_REVIEW_ONLY'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True);ap.add_argument('--dest',required=True)
    ap.add_argument('--expected-sha',required=True);ap.add_argument('--genre',default='ai_work')
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.dest,a.expected_sha,a.genre),ensure_ascii=False,indent=2))
