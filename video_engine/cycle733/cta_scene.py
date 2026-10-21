#!/usr/bin/env python3
"""cycle733: original Japanese CTA scene for a 10-genre portrait video (review only).

No downloaded images, logos, user data or external paid services are used.
Source narration and its timing are preserved by remuxing the AAC stream.
This is a reimplementation, NOT original v33 code or a publishable asset.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS, TOTAL = 1080, 1920, 30, 819
START, END = 729, 819
PHASES = (25, 30, 35)
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
from cta_policy import PALETTES, GENRE_COPY, CTA_TEXT, validate_genre

def validate(genre):
    validate_genre(genre)
    if set(PALETTES) != set(GENRE_COPY): raise AssertionError('Missing genre CTA')
    if sum(PHASES) != END-START or END != TOTAL: raise AssertionError('Timeline invalid')
    if not Path(FONT).is_file(): raise FileNotFoundError(FONT)

def f(size): return ImageFont.truetype(FONT, size)

def centered(d, txt, y, size, color, x1=70, x2=1010):
    ff=f(size)
    box=d.textbbox((0,0),txt,font=ff)
    width=box[2]-box[0]
    if width > x2-x1: raise ValueError('Text too wide: '+txt)
    d.text((x1+(x2-x1-width)//2,y),txt,font=ff,fill=color)

def card(phase, genre='ai_work'):
    """Create fully opaque original 1080x1920 artwork, avoiding old-layer ghosts."""
    validate(genre)
    if phase not in (0,1,2): raise ValueError('Invalid phase')
    accent=PALETTES[genre]
    im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
    for y in range(H):
        q=y/H
        d.line((0,y,W,y),fill=(int(5+12*q),int(19+20*q),int(39+28*q)))
    # Blurred lighting: a cinematic cue, not a claimed photorealistic asset.
    glow=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((-130,120,700,950),fill=(0,173,218,120))
    g.ellipse((540,410,1400,1390),fill=(53,97,255,96))
    im=Image.alpha_composite(im.convert('RGBA'),glow.filter(ImageFilter.GaussianBlur(145))).convert('RGB')
    d=ImageDraw.Draw(im)
    for y in (130,285,1120,1635):
        d.line((72,y,1008,y),fill='#20465F',width=2)
    d.rounded_rectangle((71,151,673,224),radius=20,fill='#123A54',outline='#427B94',width=2)
    d.text((94,166),'AI時短ラボ  /  保存版',font=f(34),fill=accent)
    d.text((74,293),'あとで見返せる、実践メモ',font=f(49),fill='white')

    # Glass panel with layered depth, inset glow, and prominent native Japanese.
    shadow=Image.new('RGBA',(W,H),(0,0,0,0));sd=ImageDraw.Draw(shadow)
    sd.rounded_rectangle((109,444,994,1139),radius=64,fill=(0,0,0,150))
    im=Image.alpha_composite(im.convert('RGBA'),shadow.filter(ImageFilter.GaussianBlur(34)))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((85,407,995,1102),radius=57,fill='#0A314A',outline='#71B7CF',width=6)
    d.rounded_rectangle((110,432,970,1076),radius=43,fill='#0C243A',outline='#2C617B',width=3)
    d.rounded_rectangle((145,470,934,535),radius=18,fill='#164961')
    centered(d,'あとで使える  /  3ステップ',480,33,accent,155,920)

    if phase == 0:
        # Save symbol; hand-drawn glossy vector with highlight and shadow.
        d.ellipse((362,584,727,952),fill='#062038',outline='#285C76',width=10)
        d.ellipse((391,610,698,923),fill='#105471',outline=accent,width=8)
        d.polygon([(481,666),(608,666),(608,837),(544,792),(481,837)],fill=accent)
        d.line((489,681,600,681),fill='#FFFFFF',width=9)
        centered(d,'この手順を保存',972,48,'white')
    elif phase == 1:
        steps=('①  架空データを用意','②  AIへ指示する','③  最後は人が確認')
        for i,s in enumerate(steps):
            y=578+i*147
            d.rounded_rectangle((154,y,926,y+116),radius=26,fill='#17435A',outline=accent if i==2 else '#367A96',width=3)
            d.text((182,y+24),s,font=f(43),fill='white' if i<2 else accent)
    else:
        d.rounded_rectangle((209,590,870,862),radius=58,fill='#136E7A',outline=accent,width=7)
        d.rounded_rectangle((234,615,846,838),radius=44,fill='#0E465B')
        centered(d,'保存しておこう',667,64,'white',244,838)
        d.ellipse((472,895,610,1033),fill='#2FBAAB',outline=accent,width=6)
        d.line((501,955,532,983,580,931),fill='white',width=12,joint='curve')

    # Explicit caption-safe layer, replaces original English CTA and old captions.
    d.rounded_rectangle((72,1215,1008,1540),radius=36,fill='#06192D',outline=accent,width=5)
    d.rounded_rectangle((96,1247,109,1510),radius=7,fill=accent)
    centered(d,CTA_TEXT[0],1280,67,'white',138,964)
    centered(d,CTA_TEXT[1],1395,58,accent,138,964)
    d.text((77,1639),'※ 架空データ / 操作イメージ / 社員承認前',font=f(27),fill='#C0D8E4')
    return im.convert('RGB')

def run(cmd,timeout=300):
    return subprocess.run(cmd,check=True,capture_output=True,text=True,timeout=timeout)

def probe(path,frames=False):
    args=['ffprobe','-v','error']+(['-count_frames'] if frames else [])
    return json.loads(run(args+['-show_streams','-show_format','-of','json',str(path)]).stdout)

def render(source,output,genre='ai_work'):
    validate(genre); source=Path(source); output=Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    base=probe(source,frames=True)
    v=next(s for s in base['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'],v.get('nb_read_frames'))!=(W,H,str(TOTAL)):
        raise ValueError('Source must be 819-frame 1080x1920 video')
    if not any(s['codec_type']=='audio' for s in base['streams']):
        raise ValueError('Missing narration')
    output.parent.mkdir(parents=True,exist_ok=True)
    work=output.parent/'_work';work.mkdir(exist_ok=True)
    clips=[]
    for i,frames in enumerate(PHASES):
        pic=work/f'cta_phase{i}.png';card(i,genre).save(pic)
        clip=work/f'cta_phase{i}.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1',
             '-framerate',str(FPS),'-t','0.033334','-i',str(pic),
             '-vf',f"zoompan=z='min(zoom+0.00025,1.022)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1080x1920:fps=30,format=yuv420p",
             '-frames:v',str(frames),'-an','-c:v','libx264','-preset','veryfast',
             '-crf','21',str(clip)])
        clips.append(clip)
    concat=work/'concat.txt';concat.write_text(''.join("file '"+str(p)+"'\n" for p in clips))
    scene=work/'cta.mp4'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(scene)])
    assert next(s for s in probe(scene,True)['streams'] if s['codec_type']=='video')['nb_read_frames']==str(END-START)
    silent=work/'silent.mp4'
    fc=f'[0:v]trim=start_frame=0:end_frame={START},setpts=PTS-STARTPTS[a];[1:v]setpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=1:a=0,format=yuv420p[out]'
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(scene),
         '-filter_complex',fc,'-map','[out]','-an','-c:v','libx264','-preset','veryfast',
         '-crf','21','-pix_fmt','yuv420p','-frames:v',str(TOTAL),str(silent)])
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(silent),'-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)])
    out=probe(output,True)
    vo=next(s for s in out['streams'] if s['codec_type']=='video')
    if vo['nb_read_frames']!=str(TOTAL): raise AssertionError('Lost frame')
    return {'path':str(output),'sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
            'frames':TOTAL,'changed_frames':[START,END-1],'duration':float(out['format']['duration']),
            'genres_supported':len(PALETTES),'human_review_required':True,
            'publication_approved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai_work');a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre),ensure_ascii=False,indent=2))
