"""Review-only correction of a misleading 46->75 visual into auditable 46+29=75.

Fictional data only. No new speech claims, media uploads, posting or rights approval.
The scene06 overlay is generic to ten genre color themes and preserves lower subtitles.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from quality.cycle1082.chart_bridge import ACCENTS, SAMPLE, FONT, sha256, probe, validate

W,H,FPS,START,END,SAFE_Y = 1080,1920,30,429,520,1280


def clamp(v):
    return max(0.0,min(1.0,v))


def smooth(v):
    v=clamp(v)
    return v*v*(3-2*v)


def text(draw,xy,s,size=34,color='#f0f8ff'):
    draw.text(xy,str(s),font=ImageFont.truetype(FONT,size),fill=color)


def frame(index, data=SAMPLE, genre='ai_work'):
    totals=validate(data)
    if genre not in ACCENTS: raise ValueError('unsupported genre')
    if not 0<=index<END-START: raise ValueError('frame outside scene06')
    accent=ACCENTS[genre]
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(im)
    # Fully cover the old, potentially misleading "before 46 / after 75" graphic.
    d.rounded_rectangle((36,135,1044,1236),radius=33,fill='#071b2c',outline='#3a6677',width=3)
    d.rounded_rectangle((67,168,1013,318),radius=22,fill='#103247')
    d.rounded_rectangle((88,192,270,236),radius=15,fill=accent)
    text(d,(103,196),'数字の検算',27,'#071b2c')
    text(d,(91,249),'差があれば、内訳を1つずつ確認',34)
    text(d,(91,339),'架空データの検算例  /  営業A ＋ 営業B',29,'#c5dce8')

    names=[s['name'] for s in data['series']]
    # Dynamic data is computed from the input, never hard-coded as 46 or 75.
    values=[totals[0],totals[1],sum(totals)]
    labels=[names[0],names[1],'合計']
    x_positions=[80,408,736]
    colors=['#123d50','#123d50','#0d4b50']
    for k,(x,value,label) in enumerate(zip(x_positions,values,labels)):
        progress=smooth((index-(k*15+2))/19)
        d.rounded_rectangle((x,418,x+260,786),radius=24,fill=colors[k],outline=(accent if k==2 else '#426f7f'),width=4)
        text(d,(x+27,454),f'0{k+1}  {label}',30,'#d1e6ee')
        if progress>0:
            # Count-up animation is illustrative; the final value is computed.
            n=round(value*progress)
            text(d,(x+37,528),n,96,('#ffffff' if k<2 else accent))
            d.rounded_rectangle((x+25,703,x+235,723),radius=9,fill='#204557')
            d.rounded_rectangle((x+25,703,x+25+int(210*progress),723),radius=9,fill=accent)
            if progress>=1: text(d,(x+90,738),'確認済',24,'#bde9dd')
        if k<2:
            text(d,(x+270,576),'+' if k==0 else '=',55,accent)
    if index>=60:
        p=smooth((index-60)/15)
        d.rounded_rectangle((88,833,993,1004),radius=21,fill='#0d3846',outline=accent,width=3)
        text(d,(112,851),'検算結果',31,'#c5dce8')
        text(d,(112,906),f'{names[0]} {values[0]} ＋ {names[1]} {values[1]} ＝ 合計 {values[2]}',39,'#ffffff')
        d.rounded_rectangle((100,1028,980,1120),radius=17,fill='#173343')
        text(d,(121,1048),'元データと一致  /  修正前後の効果を示す数値ではありません',25,'#d5e5ed')
    text(d,(97,1168),'FICTIONAL DATA  ·  HUMAN REVIEW ONLY',21,'#b8ceda')
    assert im.crop((0,SAFE_Y,W,H)).getbbox() is None
    return im


def render(source,output,source_sha,data=SAMPLE,genre='ai_work',smoke=False):
    validate(data)
    if genre not in ACCENTS: raise ValueError('unsupported genre')
    if sha256(source)!=source_sha: raise ValueError('source SHA mismatch: fail closed')
    p=probe(source)
    if (p['codec'],p['width'],p['height'],p['fps'],p['audio'],p['sample_rate'])!=('h264',W,H,'30/1','aac',48000):
        raise ValueError('unexpected source video/audio parameters')
    if p['duration']<END/FPS or (not smoke and abs(p['duration']-23.033333)>0.08):
        raise ValueError('unexpected source duration')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory() as t:
        t=Path(t)
        for i in range(END-START): frame(i,data,genre).save(t/f'overlay_{i:03}.png',compress_level=1)
        filt=(f'[1:v]format=rgba,setpts=PTS-STARTPTS+{START/FPS}/TB[ov];'
              f'[0:v][ov]overlay=0:0:shortest=0:eof_action=pass:repeatlast=0:'
              f"enable='between(n,{START},{END-1})'[v]")
        subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-framerate','30',
                        '-i',str(t/'overlay_%03d.png'),'-filter_complex',filt,
                        '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
                        '-crf','19','-pix_fmt','yuv420p','-r','30','-c:a','copy',
                        '-movflags','+faststart',str(output)],check=True)
    return probe(output)


def smoke():
    with tempfile.TemporaryDirectory() as t:
        t=Path(t);src=t/'synthetic.mp4';out=t/'rendered.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i','testsrc2=size=1080x1920:rate=30:duration=18',
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=18',
                        '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
                        '-c:a','aac','-shortest',str(src)],check=True)
        render(src,out,sha256(src),smoke=True)
        subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-f','null','-'],check=True)
        print('PASS synthetic 18-second audio/video render and full decode')

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--source');a.add_argument('--source-sha');a.add_argument('--out')
    a.add_argument('--genre',default='ai_work',choices=ACCENTS)
    a.add_argument('--data-json');a.add_argument('--smoke',action='store_true')
    x=a.parse_args()
    if x.smoke: smoke()
    else:
        if not x.data_json: raise SystemExit('explicit fictional data JSON required')
        data=json.loads(Path(x.data_json).read_text(encoding='utf-8'))
        print(json.dumps(render(x.source,x.out,x.source_sha,data,x.genre),ensure_ascii=False,indent=2))
