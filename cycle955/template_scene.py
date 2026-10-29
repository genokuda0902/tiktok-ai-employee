"""Review-only cycle955: evidence-led reusable prompt template, scene07.

This is a reimplementation, not the original v33 renderer. No publication
approval is inferred from successful rendering. Private source stays local.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
START, END = 17.4, 20.3
TOP_END = 1490  # preserve lower subtitle, waveform and footers
SOURCE_SHA256 = 'bc3db2e24d13dc93c64c9cc556b6319c23177135c7ddf56dedf389e21832171b'
GENRES = {
    'ai_work': ('営業', '採用', '事務'), 'finance': ('支出', '収入', '予算'),
    'history': ('人物', '年代', '資料'), 'science': ('観測', '仮説', '結果'),
    'health': ('記録', '経過', '相談'), 'travel': ('日程', '場所', '予算'),
    'food': ('食材', '分量', '手順'), 'career': ('経歴', '求人', '面接'),
    'education': ('単元', '課題', '復習'), 'lifestyle': ('家事', '予定', '習慣'),
}
FONT_PATHS = ['/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',
              '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc']


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()


def font(size):
    for p in FONT_PATHS:
        if Path(p).exists(): return ImageFont.truetype(p,size)
    raise RuntimeError('Noto CJK font required for Japanese rendering')


def validate(genre, source, review_only=True, publication_approved=False):
    if genre not in GENRES: raise ValueError('unknown genre')
    if genre!='ai_work': raise ValueError('genre layout and media not reviewed; fail closed')
    if review_only is not True or publication_approved is not False:
        raise ValueError('human review only, publication unapproved')
    if sha256(source)!=SOURCE_SHA256: raise ValueError('source MP4 SHA mismatch; fail closed')


def stage_at(t):
    dt=t-START
    if dt<0 or dt>=END-START: return -1
    return min(2,int(dt/((END-START)/3)))


def render_upper(t, genre='ai_work'):
    """Return a new BGR scene upper area; never paints y>=TOP_END."""
    if genre!='ai_work': raise ValueError('geometry not reviewed')
    s=stage_at(t)
    if s<0: raise ValueError('out of approved scene07 interval')
    h=TOP_END
    yy=np.linspace(0,1,h,dtype=np.float32)[:,None]
    xx=np.linspace(0,1,WIDTH,dtype=np.float32)[None,:]
    bg=np.zeros((h,WIDTH,3),dtype=np.uint8)
    bg[:,:,0]=np.clip(20+34*xx+9*yy,0,255).astype(np.uint8)
    bg[:,:,1]=np.clip(24+46*(1-xx)+13*yy,0,255).astype(np.uint8)
    bg[:,:,2]=np.clip(10+21*(1-yy)+11*xx,0,255).astype(np.uint8)
    im=Image.fromarray(cv2.cvtColor(bg,cv2.COLOR_BGR2RGB)).convert('RGBA')
    d=ImageDraw.Draw(im)
    # A small human-readable interface: not a recording of a real application.
    d.rounded_rectangle((38,40,1042,146),radius=24,fill=(5,21,42,255),outline=(69,212,215,255),width=3)
    d.text((68,66),'AI仕事術  /  REUSABLE PROMPT',font=font(35),fill=(231,250,250,255))
    d.text((70,186),'指示は「型」にして、何度も使う',font=font(55),fill=(247,250,255,255))
    d.text((72,264),'架空のテンプレート例 / 実アプリ画面ではありません',font=font(26),fill=(176,202,218,255))
    labels=('① 保存','② 入れ替え','③ 再利用')
    for i,label in enumerate(labels):
        x=65+i*337
        active=i==s
        d.rounded_rectangle((x,328,x+300,416),radius=20,
                            fill=(25,117,130,255) if active else (13,42,64,255),
                            outline=(121,249,218,255) if active else (44,92,112,255),width=4 if active else 2)
        d.text((x+48,344),label,font=font(38),fill=(255,255,255,255) if active else (155,187,205,255))
    d.rounded_rectangle((60,463,1020,1047),radius=30,fill=(244,250,253,255),outline=(90,224,215,255),width=5)
    d.rounded_rectangle((60,463,1020,538),radius=26,fill=(15,61,78,255))
    d.rectangle((60,507,1020,538),fill=(15,61,78,255))
    d.text((95,480),'PROMPT TEMPLATE  /  保存して再利用',font=font(31),fill=(245,252,252,255))
    fields=[('目的','{対象} のデータを整理'),('条件','{条件} を確認'),('出力','{形式} でまとめる')]
    for i,(key,val) in enumerate(fields):
        y=573+i*143
        highlight=(s==1 and i==1) or (s==0 and i==0) or (s==2 and i==2)
        d.rounded_rectangle((92,y,990,y+121),radius=17,
                            fill=(225,252,244,255) if highlight else (239,244,248,255),
                            outline=(25,172,153,255) if highlight else (193,207,219,255),width=5 if highlight else 2)
        d.rounded_rectangle((110,y+20,242,y+96),radius=12,fill=(12,70,92,255))
        d.text((130,y+35),key,font=font(33),fill=(255,255,255,255))
        d.text((274,y+36),val,font=font(35),fill=(12,52,70,255))
    bottom=[
        '1つの指示を、まず保存',
        '対象・条件・形式だけ変更',
        '営業・採用・事務に再利用',
    ][s]
    d.rounded_rectangle((62,1084,1018,1188),radius=22,fill=(10,73,86,255),outline=(78,222,202,255),width=3)
    d.text((100,1107),bottom,font=font(39),fill=(248,255,254,255))
    d.text((78,1290),'架空例  /  実際の利用前に内容を確認',font=font(29),fill=(191,220,226,255))
    for i in range(3):
        x=78+i*316
        d.rounded_rectangle((x,1370,x+286,1394),radius=12,
                            fill=(111,234,209,255) if i<=s else (41,96,112,255))
    return cv2.cvtColor(np.asarray(im.convert('RGB')),cv2.COLOR_RGB2BGR)


def render(source, output, genre='ai_work'):
    validate(genre,source)
    source=Path(source);output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('source decode failed')
    if round(cap.get(cv2.CAP_PROP_FPS))!=FPS or int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))!=WIDTH or int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))!=HEIGHT:
        raise ValueError('unexpected source geometry or FPS')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),'-map','0:v:0','-map','1:a:0','-frames:v',str(FRAMES),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    changed=0;count=0
    try:
        for idx in range(FRAMES):
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'source ended at frame {idx}')
            t=idx/FPS
            if START<=t<END:
                frame[:TOP_END,:,:]=render_upper(t,genre)
                changed+=1
            proc.stdin.write(frame.tobytes())
            count+=1
        proc.stdin.close();err=proc.stderr.read();ret=proc.wait()
        if ret!=0: raise RuntimeError('ffmpeg failed: '+err.decode('utf-8','replace')[-3000:])
    except Exception:
        if proc.stdin and not proc.stdin.closed: proc.stdin.close()
        proc.kill();proc.wait();raise
    finally: cap.release()
    return {'frames':count,'changed_frames':changed,'source_sha256':sha256(source),'output_sha256':sha256(output)}


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--qa',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
    r=render(a.source,a.output,a.genre)
    Path(a.qa).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r))
if __name__=='__main__': main()
