"""Cycle860: factual, data-driven chart insert for a PRIVATE review MP4.

This is a reimplementation, NOT original v33. Source rights and Japanese speech
are NOT approved; never auto-post or upload the source video to public GitHub.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
COLORS = {'ai_work':('#32d5ed','#ffd074'), 'sales_business':('#4be5ac','#ffd074'),
          'beauty':('#ff90bd','#ffd074'), 'romance':('#ff83a9','#a4c5ff'),
          'saving':('#56e7b3','#e6d26b'), 'career':('#86a6ff','#f5bf7c'),
          'wellness':('#63e6bd','#f6a5bb'), 'science':('#68d6ff','#d2a1ff'),
          'travel_food':('#f5ba79','#8ee3bb'),
          'product_comparison_lifestyle':('#a9b6ff','#f1b0a2')}
POLICY = {'review_only': True, 'publication_approved': False,
          'automatic_posting': False, 'external_upload': False,
          'source_rights_reviewed': False, 'contains_personal_data': False,
          'fictional_workflow_example': True}
ROI=(86,476,908,758); START=170; FRAMES=81; TOTAL_FRAMES=691
# The *same fictional* table is visibly present in scene 5 of cycle858.
DATA={'months':['4月','5月','6月'], 'A':[12,16,18], 'B':[8,9,12]}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def totals(data=DATA):
    if set(data)!={'months','A','B'}:raise ValueError('invalid dataset keys')
    if not 2<=len(data['months'])<=6 or any(len(data[k])!=len(data['months']) for k in ('A','B')):
        raise ValueError('invalid dataset length')
    if any(not isinstance(v,int) or v<0 or v>999 for k in ('A','B') for v in data[k]):
        raise ValueError('invalid fictional value')
    if any(not isinstance(x,str) or not x or len(x)>8 for x in data['months']):
        raise ValueError('invalid month')
    return sum(data['A']),sum(data['B'])

def ease(x):
    x=max(0,min(1,x));return x*x*(3-2*x)

def font(sz):
    return ImageFont.truetype(FONT,sz) if Path(FONT).is_file() else ImageFont.load_default()

def draw_frame(frame, genre='ai_work', data=DATA):
    if genre not in GENRES:raise ValueError('unknown genre')
    if not 0<=frame<FRAMES:raise ValueError('invalid frame')
    a,b=totals(data)
    w,h=ROI[2:]; im=Image.new('RGB',(w,h),(8,22,34));d=ImageDraw.Draw(im)
    # Cinematic dark background: glow, grid, then factual chart.
    glow=Image.new('RGBA',(w,h),(0,0,0,0));g=ImageDraw.Draw(glow)
    g.ellipse((400,-280,1100,390),fill=(20,125,170,45));g.ellipse((-250,450,350,950),fill=(240,155,70,22))
    glow=glow.filter(ImageFilter.GaussianBlur(90));im=Image.alpha_composite(im.convert('RGBA'),glow)
    d=ImageDraw.Draw(im)
    for x in range(80,w,96):d.line((x,70,x,h-70),fill=(25,48,63),width=1)
    for y in range(95,h-75,96):d.line((70,y,w-70,y),fill=(25,48,63),width=1)
    c1,c2=COLORS[genre]
    d.rounded_rectangle((44,36,w-44,h-37),radius=32,outline=(55,113,132),width=3)
    d.text((82,76),'完成形の見本をつくる。',font=font(41),fill=(241,250,252))
    d.text((83,145),'例：架空の営業データをグラフ化',font=font(29),fill=(161,194,204))
    d.rounded_rectangle((85,204,310,252),radius=22,fill=(20,55,69))
    d.text((106,210),'営業A',font=font(24),fill=c1)
    d.rounded_rectangle((325,204,548,252),radius=22,fill=(49,45,47))
    d.text((346,210),'営業B',font=font(24),fill=c2)
    maxv=max(max(data['A']),max(data['B']),1)
    base=565;chart_h=238;group_w=205
    phase_a=ease((frame+1)/26)
    phase_b=ease((frame-25)/27)
    for i,month in enumerate(data['months']):
        gx=150+i*group_w
        for series,idx,color,progress in (('A',0,c1,phase_a),('B',1,c2,phase_b)):
            value=data[series][i];bh=round(chart_h*value/maxv*progress)
            x=gx+idx*62
            if bh>1:
                d.rounded_rectangle((x,base-bh,x+49,base),radius=10,fill=color)
                if bh>28:d.text((x+6,base-bh+3),str(value),font=font(27),fill=(9,22,30))
        d.text((gx+29,base+18),month,font=font(34),fill=(220,232,236))
    d.line((100,base,810,base),fill=(116,158,170),width=3)
    if frame>=54:
        t=ease((frame-53)/16)
        # Transparent overlay keeps numerical totals tied to source values.
        panel=Image.new('RGBA',(w,h),(0,0,0,0));p=ImageDraw.Draw(panel)
        p.rounded_rectangle((80,626,w-80,719),radius=24,fill=(9,42,54,round(235*t)),outline=(60,184,207,round(255*t)),width=3)
        p.text((113,647),f'合計   A {a}     B {b}',font=font(36),fill=(240,247,249,round(255*t)))
        im=Image.alpha_composite(im,panel)
    else:
        d.text((113,647),'元データ → 完成イメージ',font=font(31),fill=(163,205,216))
    return im.convert('RGB')

def frames_to_disk(directory,genre='ai_work',data=DATA):
    out=Path(directory);out.mkdir(parents=True,exist_ok=True)
    if list(out.iterdir()):raise ValueError('refuse nonempty frame directory')
    for i in range(FRAMES):draw_frame(i,genre,data).save(out/f'chart_{i:03}.png')
    return out

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)],text=True))

def validate(source,output,manifest,genre):
    source=Path(source);output=Path(output)
    if genre not in GENRES:raise ValueError('unknown genre')
    if not source.is_file():raise FileNotFoundError('missing private input')
    if output.exists() or output.resolve()==source.resolve():raise ValueError('refuse overwrite')
    if manifest!={**POLICY,'source_sha256':digest(source)}:raise ValueError('private manifest policy/hash mismatch')
    streams=probe(source)['streams'];v=next((s for s in streams if s['codec_type']=='video'),None)
    a=next((s for s in streams if s['codec_type']=='audio'),None)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],v.get('nb_frames'),a['codec_name'],a['sample_rate'])!=('h264',1080,1920,'30/1',str(TOTAL_FRAMES),'aac','48000'):
        raise ValueError('expected 691-frame 1080x1920 H264/AAC48k source')
    return source,output

def render(source,output,manifest,genre='ai_work'):
    source,output=validate(source,output,manifest,genre)
    with tempfile.TemporaryDirectory(prefix='cycle860_chart_') as tmp:
        frames_to_disk(tmp,genre)
        # Time-align the 81 original image frames with frames 170..250 of the source.
        # Do not touch the header or the burned-in Japanese caption region.
        filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[insert];'
              f'[0:v][insert]overlay=x={ROI[0]}:y={ROI[1]}:enable=\'between(n,{START},{START+FRAMES-1})\':'
              'eof_action=pass:repeatlast=0:format=auto[v]')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
             '-framerate','30','-start_number','0','-i',str(Path(tmp)/'chart_%03d.png'),
             '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30',
             '-frames:v',str(TOTAL_FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=210)
    if not output.is_file() or output.stat().st_size<100000:raise RuntimeError('incomplete output')
    return {'source_sha256':digest(source),'output_sha256':digest(output),'genre':genre,
            'frames_replaced':FRAMES,'start_frame':START,'end_frame':START+FRAMES-1,
            'source_values':DATA,'totals':totals(), 'policy':POLICY}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source',required=True);ap.add_argument('--output',required=True)
    ap.add_argument('--manifest',required=True);ap.add_argument('--report',required=True)
    ap.add_argument('--genre',default='ai_work');args=ap.parse_args()
    result=render(args.source,args.output,json.loads(Path(args.manifest).read_text()),args.genre)
    Path(args.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))