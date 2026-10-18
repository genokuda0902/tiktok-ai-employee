#!/usr/bin/env python3
"""Cycle661: preserve source context beside a zoomed evidence crop.

Only operates on a local, recorded, synthetic-data screen capture. This is a
reimplementation, not recovered v33 source. No posting or approval implied.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import cv2
from PIL import Image, ImageDraw, ImageFont

GENRES = ('AI・仕事効率化','美容・身だしなみ','恋愛・心理','お金・節約',
          '営業・ビジネス','転職・キャリア','健康・生活改善','雑学・科学',
          '旅行・グルメ','商品比較・暮らし')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def check(manifest, source):
    if manifest.get('genre') not in GENRES: raise ValueError('unknown genre')
    if manifest.get('publication') != 'NOT_APPROVED' or manifest.get('rights') != 'REVIEW_ONLY_UNVERIFIED':
        raise ValueError('review-only rights gate')
    if manifest.get('data') != 'SYNTHETIC': raise ValueError('synthetic data required')
    if manifest.get('source_sha256') != sha(source): raise ValueError('source checksum mismatch')
    cap = cv2.VideoCapture(str(source))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)); height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    x,y,w,h = manifest['crop']
    if min(x,y) < 0 or min(w,h) <= 0 or x+w>width or y+h>height: raise ValueError('invalid crop')
    for k in ('formula_roi','result_roi'):
        a,b,c,d = manifest[k]
        if min(c,d)<=0 or a<x or b<y or a+c>x+w or b+d>y+h:
            raise ValueError('invalid '+k)
    return True

def scene(source, manifest, output_dir, fps=20, duration=3):
    check(manifest,source)
    output_dir.mkdir(parents=True,exist_ok=True)
    cap=cv2.VideoCapture(str(source)); src_fps=cap.get(cv2.CAP_PROP_FPS)
    src_dur=cap.get(cv2.CAP_PROP_FRAME_COUNT)/src_fps
    title=ImageFont.truetype(FONT,62); sub=ImageFont.truetype(FONT,42)
    label=ImageFont.truetype(FONT,30); small=ImageFont.truetype(FONT,27)
    x,y,w,h=manifest['crop']
    for i in range(fps*duration):
        t=i/fps; source_t=(1.5 + t*2.0) if t<1.5 else (5.2 + (t-1.5)*1.0)
        source_t=min(src_dur-0.1,source_t)
        cap.set(cv2.CAP_PROP_POS_MSEC,source_t*1000)
        ok,fr=cap.read()
        if not ok: raise RuntimeError('source video decode failure')
        original=Image.fromarray(cv2.cvtColor(fr[y:y+h,x:x+w],cv2.COLOR_BGR2RGB))
        key='formula_roi' if t<1.5 else 'result_roi'
        a,b,c,d=manifest[key]
        # A single real source frame drives both panels: no fabricated UI.
        full=original.resize((470,371),Image.Resampling.LANCZOS)
        pad=14
        region=Image.fromarray(cv2.cvtColor(fr[max(0,b-pad):min(fr.shape[0],b+d+pad),max(0,a-pad):min(fr.shape[1],a+c+pad)],cv2.COLOR_BGR2RGB))
        region.thumbnail((430,390),Image.Resampling.LANCZOS)
        zoom=region.resize((430, max(160,min(400,round(region.height*430/region.width)))),Image.Resampling.LANCZOS)
        im=Image.new('RGB',(1080,1920),'#06192e'); draw=ImageDraw.Draw(im)
        draw.text((65,100),'AI時短ラボ  /  検算の実演',font=sub,fill='#6de7ff')
        draw.text((65,210),'全体と拡大を同時に',font=title,fill='white')
        draw.text((65,315),'元の操作を見失わない',font=sub,fill='#c4e8f4')
        draw.rounded_rectangle((34,510,1046,1240),radius=28,fill='#0e2c48',outline='#327b9c',width=4)
        draw.text((65,545),'① 元の表計算画面',font=label,fill='#b8e9ff')
        draw.text((570,545),'② 同じ画面を拡大',font=label,fill='#b8e9ff')
        im.paste(full,(65,645))
        draw=ImageDraw.Draw(im)
        fx=65+round((a-x)*470/w); fy=645+round((b-y)*371/h)
        fx2=65+round((a+c-x)*470/w); fy2=645+round((b+d-y)*371/h)
        col='#ffdb5e' if key=='formula_roi' else '#51f5c8'
        draw.rectangle((fx-4,fy-4,fx2+4,fy2+4),outline=col,width=7)
        draw.line((535,840,558,840),fill=col,width=10)
        draw.polygon([(570,840),(548,827),(548,853)],fill=col)
        draw.rounded_rectangle((564,632,1020,1080),radius=18,fill='#f1f7fc',outline=col,width=7)
        im.paste(zoom,(578,665)); draw=ImageDraw.Draw(im)
        draw.rounded_rectangle((70,1165,1010,1225),radius=15,fill='#1d4562')
        draw.text((90,1170),'元画面と拡大は同じ録画フレーム',font=small,fill='white')
        draw.rounded_rectangle((60,1340,1020,1570),radius=30,fill='#0d3c54',outline=col,width=4)
        draw.text((95,1380),'STEP 1｜数式を入力' if t<1.5 else 'STEP 2｜結果を確認',font=sub,fill=col)
        draw.text((95,1460),'=SUM(B2:B5)' if t<1.5 else '120＋150＋200＋180＝650',font=sub,fill='white')
        draw.text((65,1710),'※ 架空の売上データ／公開・投稿未承認',font=small,fill='#b9cfde')
        im.save(output_dir/f'{i:04d}.jpg',quality=90)
    cap.release()

def render(source, baseline, manifest, out):
    frames=out.parent/'scene_frames';scene(source,manifest,frames)
    clip=out.parent/'split_scene.mp4'
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate','20','-i',str(frames/'%04d.jpg'),'-c:v','libx264','-pix_fmt','yuv420p','-preset','veryfast','-crf','21',str(clip)],check=True)
    filt="[1:v]setpts=PTS-STARTPTS+10.5/TB[s];[0:v][s]overlay=0:0:enable='gte(t,10.5)*lt(t,13.5)':eof_action=pass[v]"
    subprocess.run(['ffmpeg','-y','-loglevel','error','-i',str(baseline),'-i',str(clip),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-r','30','-c:v','libx264','-preset','veryfast','-crf','21','-threads','2','-c:a','copy','-movflags','+faststart',str(out)],check=True)
    return sha(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--base',type=Path,required=True);p.add_argument('--manifest',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    a=p.parse_args(); print(json.dumps({'sha256':render(a.source,a.base,json.loads(a.manifest.read_text()),a.out),'publication':'NOT_APPROVED'}))
