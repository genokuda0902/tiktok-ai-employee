#!/usr/bin/env python3
"""Review-only prompt clarity scene. Reimplementation, not original v33 source.

No network, private asset upload, publication, or paid services. Source MP4 stays local.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_TOP = 1490
SCENE_START, SCENE_END = 261, 348  # [8.70s,11.60s), 87 frames
GENRES = {
    "ai_work": ("#00D5D4", "#A7F3D0"),
    "business": ("#60A5FA", "#BFDBFE"),
    "finance": ("#FBBF24", "#FEF3C7"),
    "health": ("#34D399", "#D1FAE5"),
    "beauty": ("#FB7185", "#FFE4E6"),
    "travel": ("#38BDF8", "#BAE6FD"),
    "education": ("#A78BFA", "#DDD6FE"),
    "food": ("#FB923C", "#FED7AA"),
    "life_hacks": ("#2DD4BF", "#CCFBF1"),
    "tech": ("#818CF8", "#C7D2FE"),
}
APPROVED_REVIEW_GENRES = frozenset(["ai_work"])
FONT_DIRS = [Path('/usr/share/fonts/opentype/noto'), Path('/usr/share/fonts/truetype/noto')]

def font(size, bold=False):
    names = ('NotoSansCJK-Bold.ttc', 'NotoSansCJK-Regular.ttc') if bold else ('NotoSansCJK-Regular.ttc',)
    for folder in FONT_DIRS:
        for name in names:
            if (folder/name).exists():
                return ImageFont.truetype(str(folder/name), size, index=0)
    raise RuntimeError('Noto CJK Japanese font missing; fail closed')

def assert_review_genre(genre):
    if genre not in GENRES: raise ValueError('Unknown genre')
    if genre not in APPROVED_REVIEW_GENRES: raise PermissionError('Genre unreviewed; fail closed')

def draw_scene(phase: float, genre='ai_work') -> np.ndarray:
    """Return 1080x1490 RGB scene, no inherited subtitle region."""
    assert_review_genre(genre)
    accent, pale = GENRES[genre]
    im = Image.new('RGB', (WIDTH, CAPTION_TOP), '#061526')
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((30, 32, 1050, 1430), radius=32, fill='#0B2135', outline='#28536A', width=3)
    d.rounded_rectangle((62, 64, 1018, 144), radius=18, fill='#102D43')
    d.text((92, 82), 'AI WORK / PROMPT DESIGN', font=font(35, True), fill=accent)
    d.text((64, 208), 'AIへの指示は', font=font(68, True), fill='#FFFFFF')
    d.text((64, 299), '3点セットで伝える', font=font(66, True), fill='#FFFFFF')
    d.text((66, 408), '目的 → 条件 → 出力', font=font(40, True), fill=pale)
    labels = [
        ('01', '目的', '売上を月別に集計する'),
        ('02', '条件', '4〜6月・営業AとB'),
        ('03', '出力', '表とグラフで見せる'),
    ]
    for idx, (number, title, detail) in enumerate(labels):
        y = 520 + idx*238
        active = phase >= (idx / 3.0)
        d.rounded_rectangle((65, y, 1015, y+207), radius=24,
                            fill='#153C4D' if active else '#10283A',
                            outline=accent if active else '#345063', width=4 if active else 2)
        d.rounded_rectangle((92, y+28, 170, y+104), radius=18,
                            fill=accent if active else '#254559')
        d.text((107, y+36), number, font=font(34, True), fill='#052034' if active else '#9BB0BE')
        d.text((196, y+23), title, font=font(48, True), fill='#FFFFFF' if active else '#849AA8')
        d.text((105, y+117), detail, font=font(41, True), fill='#FFFFFF' if active else '#728A99')
    d.rounded_rectangle((66, 1266, 1014, 1284), radius=9, fill='#29475A')
    d.rounded_rectangle((66, 1266, 66 + int(948 * min(1, max(0, phase))), 1284), radius=9, fill=accent)
    d.text((68, 1330), '操作イメージ / 実際のChatGPT画面ではありません', font=font(28), fill='#B7CCD7')
    return np.asarray(im)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def render(source, output, report, genre='ai_work', synthetic_test=False):
    assert_review_genre(genre)
    source,output,report=map(Path,(source,output,report))
    if not source.exists(): raise FileNotFoundError(source)
    if source.resolve()==output.resolve(): raise ValueError('Output must differ from source')
    cap=cv2.VideoCapture(str(source))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)); fps=cap.get(cv2.CAP_PROP_FPS)
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    if (w,h)!=(WIDTH,HEIGHT) or abs(fps-FPS)>.01:raise ValueError('Unexpected geometry/FPS')
    if not synthetic_test and count!=691:raise ValueError('Unreviewed source length')
    start,end=(30,min(90,count)) if synthetic_test else (SCENE_START,SCENE_END)
    if count<end: raise ValueError('Source too short')
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-vcodec','rawvideo',
         '-pix_fmt','bgr24','-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','20',
         '-pix_fmt','yuv420p','-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart','-frames:v',str(count),str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    n=0
    try:
        while True:
            ok,frame=cap.read()
            if not ok:break
            if start<=n<end:
                rgb=draw_scene((n-start)/(end-start),genre)
                frame[:CAPTION_TOP,:,:]=cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
            proc.stdin.write(frame.tobytes());n+=1
        proc.stdin.close()
        stderr=proc.stderr.read().decode('utf-8','replace')
        code=proc.wait()
        if code:raise RuntimeError(f'ffmpeg exit {code}: {stderr[-2000:]}')
    finally:
        cap.release()
        if proc.poll() is None: proc.kill()
    if n!=count:raise RuntimeError(f'Frame count changed: {n}/{count}')
    data={'source_sha256':sha256(source),'output_sha256':sha256(output),
          'genre':genre,'scene_frames':[start,end],'scene_seconds':[start/FPS,end/FPS],
          'frames':n,'resolution':[w,h],'fps':fps,'subtitle_protection_y':CAPTION_TOP,
          'publication_approved':False,'independent_japanese_asr':'UNVERIFIED',
          'source_rights':'UNVERIFIED','smartphone_playback':'UNVERIFIED',
          'synthetic_ci_only':bool(synthetic_test)}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return data

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work')
    p.add_argument('--synthetic-test',action='store_true')
    a=p.parse_args(); print(json.dumps(render(a.source,a.output,a.report,a.genre,a.synthetic_test),ensure_ascii=False))
