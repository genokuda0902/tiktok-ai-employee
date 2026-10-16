#!/usr/bin/env python3
"""Cycle627: genre-neutral verified-result animation (REVIEW_ONLY).

Reimplementation using synthetic data. No actual AI or Excel recording.
No third-party images, fonts distributed, paid APIs, Japanese narration, or publishing.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, FRAMES = 540, 960, 30, 60
FIRST_FRAME, LAST_FRAME = 126, 186  # 4.2s through 6.2s, half-open
GENRES = ('ai_work','beauty','relationships','money','sales_business','career',
          'health_lifestyle','science_trivia','travel_food','product_lifestyle')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'


def contract(values=(120,150,200,250), labels=('1月','2月','3月','4月'),
             genre='ai_work', rights='SYNTHETIC_REVIEW_ONLY', publication='NOT_APPROVED'):
    if genre not in GENRES: raise ValueError('unsupported genre')
    if len(values) != 4 or any(type(v) is not int or not 0 <= v <= 999999 for v in values):
        raise ValueError('four nonnegative integers required')
    if len(labels) != 4 or any(not isinstance(s,str) or not 1 <= len(s) <= 8 for s in labels):
        raise ValueError('four short labels required')
    if rights != 'SYNTHETIC_REVIEW_ONLY' or publication != 'NOT_APPROVED':
        raise ValueError('review-only, synthetic assets required')
    return {'genre':genre, 'values':list(values), 'labels':list(labels),
            'total':sum(values), 'formula':'=SUM(B2:B5)',
            'actual_excel_recording':False, 'new_japanese_voice':False,
            'rights':rights,'publication':publication}


def display_state(frame:int):
    if type(frame) is not int or not 0 <= frame < FRAMES:
        raise ValueError('invalid frame')
    return 'calculating' if frame < 23 else 'verified'


def frame_text(frame, data):
    if display_state(frame) == 'calculating':
        return ('4件を読み取り中', '検算中…', '合計はまだ表示しません')
    return ('4件の数値を検算', str(data['total']), data['formula'])


def draw_frame(frame:int, data:dict):
    state=display_state(frame)
    im=Image.new('RGB',(W,H)); p=im.load()
    for y in range(H):
        for x in range(W):
            a=y/H; p[x,y]=(int(7+11*a),int(20+17*a),int(39+17*a))
    d=ImageDraw.Draw(im)
    f=lambda size,bold=False: ImageFont.truetype(BOLD if bold else FONT,size)
    cyan=(53,224,228); pale=(231,251,254)
    # Safe zone x 28..512, y 100..840 (9:16 review preview)
    d.rounded_rectangle((28,56,512,107),radius=13,fill=(16,55,76),outline=(45,140,171),width=2)
    d.text((46,68),'AI時短ラボ  /  数字の根拠',font=f(23,True),fill=pale)
    d.text((30,149),'数式の答えは、',font=f(43,True),fill=(255,255,255))
    d.text((30,215),'4つの数字から。',font=f(42,True),fill=cyan)
    # Four evidence rows always visible; no misleading intermediate total.
    d.rounded_rectangle((29,318,511,611),radius=21,fill=(229,244,246),outline=(91,194,205),width=3)
    d.text((53,332),'サンプル売上（架空）',font=f(22,True),fill=(22,78,94))
    for j,(label,v) in enumerate(zip(data['labels'],data['values'])):
        top=385+j*51
        if j%2==0:d.rounded_rectangle((44,top,495,top+49),radius=8,fill=(211,233,238))
        d.text((61,top+5),label,font=f(26,True),fill=(27,65,81))
        d.text((353,top+4),str(v),font=f(29,True),fill=(19,82,92))
        if state=='verified':
            d.ellipse((447,top+14,467,top+34),fill=(13,151,120))
            d.line([(451,top+23),(456,top+28),(465,top+17)],fill='white',width=3)
    d.rounded_rectangle((29,644,511,816),radius=22,fill=(14,64,83),outline=cyan,width=3)
    if state=='calculating':
        d.text((54,666),'検算中…',font=f(43,True),fill=pale)
        d.text((55,733),'4件を確認してから表示',font=f(23),fill=(168,221,227))
        for j in range(4):
            col=cyan if j <= frame//6 else (46,99,115)
            d.rounded_rectangle((342+j*36,684,366+j*36,707),radius=8,fill=col)
    else:
        d.text((54,657),'検算した合計',font=f(27,True),fill=(175,232,231))
        d.text((56,690),str(data['total']),font=f(74,True),fill=(255,225,114))
        d.text((315,731),data['formula'],font=f(20,True),fill=pale)
    d.text((32,842),'※ 架空データ / 操作再現 / 公開未承認',font=f(17),fill=(172,203,217))
    return im


def render(baseline:Path, output:Path):
    data=contract(); output.parent.mkdir(parents=True,exist_ok=True)
    tmp=output.with_suffix('.segment.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{W}x{H}','-r',str(FPS),'-i','-','-an','-c:v','libx264','-preset','veryfast',
         '-crf','19','-pix_fmt','yuv420p',str(tmp)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    try:
        for i in range(FRAMES):p.stdin.write(draw_frame(i,data).tobytes())
        p.stdin.close(); error=p.stderr.read().decode(); status=p.wait()
    except Exception:
        p.kill();raise
    if status:raise RuntimeError('segment render failed: '+error)
    filt=(f'[0:v]trim=start_frame=0:end_frame={FIRST_FRAME},setpts=PTS-STARTPTS[v0];'
          f'[1:v]scale=1080:1920,setsar=1,setpts=PTS-STARTPTS[v1];'
          f'[0:v]trim=start_frame={LAST_FRAME},setpts=PTS-STARTPTS[v2];'
          '[v0][v1][v2]concat=n=3:v=1:a=0[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(baseline),'-i',str(tmp),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','20','-pix_fmt','yuv420p','-r','30','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    tmp.unlink()
    return data


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--baseline',required=True);ap.add_argument('--output',required=True)
    args=ap.parse_args();d=render(Path(args.baseline),Path(args.output));print(json.dumps(d,ensure_ascii=False))
if __name__=='__main__':main()
