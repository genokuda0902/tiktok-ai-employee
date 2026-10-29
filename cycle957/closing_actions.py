"""cycle957: review-only, actionable Japanese closing scene; not v33 original code."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START_FRAME, END_FRAME, TOP_END = 609, 691, 1490
SOURCE_SHA256 = '24af228e2842a53e124cdd8f0b329c10fd3399dba36f0734c500d3597f35e223'
GENRES = {
    'ai_work': ('1つ試す', '元データと照合', '明日も続ける'),
    'finance': ('1つ記録', '金額を確認', '習慣にする'),
    'history': ('1つ調べる', '出典を確認', '学びを残す'),
    'science': ('仮説を立てる', '結果を確認', '記録を残す'),
    'health': ('変化を記録', '専門家に確認', '無理なく続ける'),
    'travel': ('候補を選ぶ', '公式情報を確認', '計画を保存'),
    'food': ('1品試す', '分量を確認', '次に生かす'),
    'career': ('1つ準備', '条件を確認', '次に生かす'),
    'education': ('1問試す', '答えを確認', '復習する'),
    'lifestyle': ('1つ整える', '結果を確認', '習慣にする'),
}
FONT_PATHS = ['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
              '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def font(size):
    for p in FONT_PATHS:
        if Path(p).exists():return ImageFont.truetype(p,size)
    raise RuntimeError('Noto Sans CJK Bold font required')

def stage_at(frame):
    if not START_FRAME<=frame<END_FRAME:return -1
    return min(2, (frame-START_FRAME)*3//(END_FRAME-START_FRAME))

def validate(genre,source,review_only=True,publication_approved=False):
    if genre not in GENRES:raise ValueError('unknown genre')
    if genre!='ai_work':raise ValueError('layout/media not reviewed for this genre')
    if review_only is not True or publication_approved is not False:
        raise ValueError('human review only; publication unapproved')
    if sha256(source)!=SOURCE_SHA256:raise ValueError('source MP4 SHA mismatch')

def render_upper(frame,genre='ai_work'):
    if genre!='ai_work':raise ValueError('layout/media not reviewed for this genre')
    s=stage_at(frame)
    if s<0:raise ValueError('outside closing scene')
    xx=np.linspace(0,1,WIDTH,dtype=np.float32)[None,:]
    yy=np.linspace(0,1,TOP_END,dtype=np.float32)[:,None]
    bg=np.empty((TOP_END,WIDTH,3),dtype=np.uint8)
    bg[:,:,0]=np.clip(7+25*xx+10*yy,0,255)
    bg[:,:,1]=np.clip(25+38*(1-xx)+13*yy,0,255)
    bg[:,:,2]=np.clip(29+25*yy+8*xx,0,255)
    im=Image.fromarray(bg,'RGB').convert('RGBA')
    d=ImageDraw.Draw(im,'RGBA')
    d.ellipse((550,-330,1400,520),fill=(24,74,87,255))
    d.ellipse((-280,600,500,1410),fill=(17,72,77,255))
    d.rounded_rectangle((47,48,1033,139),radius=22,fill=(7,30,49,240),outline=(76,186,207,220),width=3)
    d.text((76,66),'AI仕事術  /  TODAY ACTION',font=font(35),fill=(230,248,250,255))
    d.text((60,199),'今日から、1つだけ。',font=font(71),fill=(251,254,255,255))
    d.text((63,305),'試す → 確かめる → 次につなげる',font=font(38),fill=(178,232,236,255))
    d.rounded_rectangle((56,400,1024,1032),radius=32,fill=(7,28,47,242),outline=(69,166,183,220),width=3)
    titles=GENRES[genre]
    notes=('身近な作業を1つ選ぶ','AIの出力は人が確認','できた方法を残す')
    for i,(title,note) in enumerate(zip(titles,notes)):
        y=434+i*192
        active=(i==s)
        fill=(18,92,100,255) if active else (14,45,66,255)
        d.rounded_rectangle((84,y,997,y+169),radius=24,fill=fill,
                            outline=(126,248,221,255) if active else (57,107,129,255),width=5 if active else 2)
        d.rounded_rectangle((113,y+29,216,y+132),radius=22,fill=(96,225,199,255) if active else (31,83,105,255))
        d.text((137,y+41),f'{i+1:02d}',font=font(48),fill=(8,47,57,255) if active else (184,216,227,255))
        d.text((255,y+23),title,font=font(49),fill=(251,255,255,255) if active else (191,219,229,255))
        d.text((258,y+98),note,font=font(31),fill=(188,240,232,255) if active else (131,165,182,255))
    d.rounded_rectangle((64,1082,1016,1188),radius=23,fill=(13,70,77,255),outline=(71,209,190,255),width=3)
    d.text((93,1101),'人が確認してから、次の一歩へ',font=font(42),fill=(243,253,252,255))
    # Animated progress cue: never imply employee approval or automated posting.
    for i in range(3):
        x=100+i*313
        d.rounded_rectangle((x,1215,x+270,1233),radius=8,
                            fill=(99,233,209,255) if i<=s else (37,91,112,255))
    d.rounded_rectangle((62,1292,1018,1413),radius=20,fill=(60,20,37,255),outline=(164,85,103,255),width=2)
    d.text((94,1322),'未承認｜社員確認後に手動投稿',font=font(39),fill=(255,232,235,255))
    return cv2.cvtColor(np.asarray(im.convert('RGB')),cv2.COLOR_RGB2BGR)

def render(source,output,genre='ai_work'):
    validate(genre,source)
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened():raise RuntimeError('source video cannot open')
    if (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),round(cap.get(cv2.CAP_PROP_FPS)))!=(WIDTH,HEIGHT,FPS):
        raise ValueError('unexpected video geometry/fps')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0','-frames:v',str(FRAMES),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for idx in range(FRAMES):
            ok,f=cap.read()
            if not ok:raise RuntimeError(f'source ends at frame {idx}')
            if START_FRAME<=idx<END_FRAME:f[:TOP_END]=render_upper(idx,genre)
            proc.stdin.write(f.tobytes())
        proc.stdin.close();err=proc.stderr.read();ret=proc.wait()
        if ret:raise RuntimeError(err.decode('utf-8','replace')[-3000:])
    except Exception:
        if proc.stdin and not proc.stdin.closed:proc.stdin.close()
        proc.kill();proc.wait();raise
    finally:cap.release()
    return {'frames':FRAMES,'changed_frames':END_FRAME-START_FRAME,'source_sha256':sha256(source),'output_sha256':sha256(output)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--qa',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
    r=render(a.source,a.output,a.genre)
    Path(a.qa).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r))
