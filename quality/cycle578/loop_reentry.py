#!/usr/bin/env python3
"""cycle578: short-form CTA-to-hook visual loop; review-only reimplementation.

Do not publish: inherited source asset rights and Japanese speech are not approved.
No external assets, no credentials, no posting.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SOURCE_SHA256 = '854c813a0458e3dd0ed07c3aa0c4c38ced235eeab0d9047dad3f104a9fc86858'
GENRES = ('ai_productivity','beauty','relationships','finance','sales','career','wellness','science','travel_food','product_comparison')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SUBS = (
(0,2,'手計算の前に、合計720を確認'),
(2,4,'4か月分の売上を入力'),
(4,6,'SUM関数でも合計720'),
(6,9,'数字を入力して集計を指示'),
(9,12,'B2:B5 を選択する'),
(12,16,'グラフの数値も確認'),
(16,18,'手入力と関数を比較'),
(18,19,'保存して、あとで試そう'),
(19,20,'手計算の前に、合計720を確認'),
)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def validate_contract(genre, scenes, duration=20):
    if genre not in GENRES: raise ValueError('unknown genre')
    if not scenes or scenes[0][0]!=0 or scenes[-1][1]!=duration: raise ValueError('incomplete timeline')
    for i,(start,end,caption) in enumerate(scenes):
        if start>=end or end-start<1: raise ValueError('caption under 1 second')
        if not caption or len(caption)>36: raise ValueError('caption missing or too long')
        if i and scenes[i-1][1]!=start: raise ValueError('timeline gap or overlap')
    return True

def timestamp(t):
    ms=round(t*1000)
    return f'{ms//3600000:02}:{ms//60000%60:02}:{ms//1000%60:02},{ms%1000:03}'

def make_srt(path, scenes=SUBS):
    validate_contract('ai_productivity',scenes)
    Path(path).write_text(''.join(f'{i}\n{timestamp(start)} --> {timestamp(end)}\n{text}\n\n' for i,(start,end,text) in enumerate(scenes,1)),encoding='utf-8')

def make_card(path):
    W,H=1080,1920
    im=Image.new('RGB',(W,H))
    pix=im.load()
    for y in range(H):
        t=y/H
        c=(int(5+5*t),int(17+15*t),int(34+20*t))
        for x in range(W):pix[x,y]=c
    d=ImageDraw.Draw(im)
    font=lambda size:ImageFont.truetype(FONT,size)
    d.rounded_rectangle((48,82,1032,1792),radius=62,fill=(9,35,55),outline=(49,203,210),width=5)
    d.rounded_rectangle((106,185,974,304),radius=30,fill=(18,67,85))
    d.text((540,242),'AI時短ラボ  /  20秒で学ぶ',font=font(44),anchor='mm',fill='#c2f9f3')
    d.text((540,486),'保存して、',font=font(104),anchor='mm',fill='#ffffff')
    d.text((540,616),'あとで試そう',font=font(108),anchor='mm',fill='#78f3dc')
    d.rounded_rectangle((144,788,936,1144),radius=36,fill=(10,28,45),outline=(36,132,155),width=4)
    d.text((540,876),'120 + 150 + 200 + 250',font=font(54),anchor='mm',fill='#d5edf7')
    d.text((540,1010),'= 720',font=font(142),anchor='mm',fill='#ffffff')
    d.rounded_rectangle((164,1280,916,1426),radius=36,fill=(23,172,153))
    d.text((540,1351),'次の1秒で、冒頭へ',font=font(62),anchor='mm',fill='#ffffff')
    d.text((540,1624),'架空データ / 効果未検証',font=font(36),anchor='mm',fill='#b1cedb')
    d.text((540,1856),'REVIEW ONLY  •  PUBLICATION NOT APPROVED',font=font(26),anchor='mm',fill='#94b0bb')
    im.save(path)

def execute(source, output, genre='ai_productivity'):
    validate_contract(genre,SUBS)
    if genre!='ai_productivity':raise ValueError('Only ai_productivity has an inspected source MP4')
    source=Path(source);output=Path(output)
    if not source.is_file() or sha256(source)!=SOURCE_SHA256:raise ValueError('source missing or SHA mismatch')
    output.parent.mkdir(parents=True,exist_ok=True)
    card=output.parent/'cta_card.png';srt=output.parent/'captions.srt'
    make_card(card);make_srt(srt)
    # Last 1s is the FIRST 1s reversed, so the final frame converges to the first frame.
    # The middle CTA is original and all visual content remains synthetic and review-only.
    filt=('[0:v]split=2[base][first];'
          '[base]trim=start=0:end=19,setpts=PTS-STARTPTS[body];'
          '[first]trim=start=0:end=1,setpts=PTS-STARTPTS,reverse,setpts=PTS-STARTPTS[tail];'
          '[body][tail]concat=n=2:v=1:a=0[loop];'
          '[loop][1:v]overlay=0:0:enable=between(t\\,18\\,18.999):shortest=1,format=yuv420p[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-i',str(card),'-i',str(srt),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0','-map','2:s:0',
         '-c:v','libx264','-preset','ultrafast','-crf','19','-r','30','-c:a','copy','-c:s','mov_text',
         '-t','20','-movflags','+faststart',str(output)]
    p=subprocess.run(cmd,capture_output=True,text=True)
    (output.parent/'render.log').write_text('command: '+repr(cmd)+'\nreturncode: '+str(p.returncode)+'\n'+p.stderr,encoding='utf-8')
    if p.returncode:raise RuntimeError(p.stderr[-3000:])
    return {'cycle':578,'source_sha256':sha256(source),'output_sha256':sha256(output),'genre':genre,
            'changed_seconds':[18,20],'improvement':'CTA card plus reverse-first-second hook loop',
            'subtitles':len(SUBS),'japanese_narration':'ABSENT','voice_caption_semantic_sync':'UNVERIFIED',
            'asset_rights':'INHERITED_UNVERIFIED','quality':'HUMAN_REVIEW','publication':'NOT_APPROVED','cost_jpy':0}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--genre',default='ai_productivity')
    args=p.parse_args();report=execute(args.source,args.output,args.genre)
    (Path(args.output).parent/'qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
