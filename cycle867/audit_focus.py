"""cycle867: original moving source-to-result audit visual, private review only.

Never represents a real AI result or actual sales. Source media is never uploaded.
The 10-genre engine changes editorial title, not the fictional numeric fixture.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess, tempfile
from functools import lru_cache
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS=30
FRAMES=691
START=336
COUNT=86
ROI=(0,132,1080,1358)  # y=132..1489; original burned subtitles begin at y=1490
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
GENRES={
 'ai_work':'AIの答えを検算',
 'sales_business':'集計結果を検算',
 'beauty':'比較数字を検算',
 'romance':'数字と根拠を確認',
 'saving':'支出の合計を検算',
 'career':'実績数字を検算',
 'wellness':'記録の数値を検算',
 'science':'データの合計を検算',
 'travel_food':'比較結果を検算',
 'product_comparison_lifestyle':'比較数字を検算',
}
DATA={'4月':(12,8),'5月':(16,9),'6月':(18,12)}
TOTALS=tuple(sum(v) for v in zip(*DATA.values()))
POLICY=dict(review_only=True,publication_approved=False,automatic_posting=False,
            external_upload=False,source_rights_reviewed=False,fictional_example=True)
SAFE_END_Y=1490


def sha256(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

@lru_cache(maxsize=20)
def font(size,bold=True):
    f=FONT if bold else REG
    if not Path(f).exists():raise FileNotFoundError('Noto CJK font unavailable')
    return ImageFont.truetype(f,size)

def ease(t):
    t=max(0.,min(1.,float(t)))
    return t*t*(3-2*t)

def assert_text_fits(draw, xy, text, size, box, bold=True):
    bounds=draw.textbbox(xy,text,font=font(size,bold))
    if bounds[0]<box[0] or bounds[1]<box[1] or bounds[2]>box[2] or bounds[3]>box[3]:
        raise ValueError('text outside its own box: '+text)

def stage(frame):
    if not 0<=frame<COUNT:raise ValueError('frame out of range')
    return 0 if frame<27 else (1 if frame<56 else 2)

@lru_cache(maxsize=1)
def bg():
    im=Image.new('RGB',(1080,900))
    d=ImageDraw.Draw(im)
    for y in range(900):
        t=y/900
        d.line((0,y,1080,y),fill=(int(5+9*t),int(18+13*t),int(33+24*t)))
    halo=Image.new('RGBA',(1080,900))
    h=ImageDraw.Draw(halo)
    h.ellipse((450,-350,1400,570),fill=(17,130,202,105))
    h.ellipse((-450,470,410,1350),fill=(17,178,153,100))
    halo=halo.filter(ImageFilter.GaussianBlur(110))
    return Image.alpha_composite(im.convert('RGBA'),halo).convert('RGB')

def draw_frame(i,genre='ai_work'):
    if genre not in GENRES:raise ValueError('invalid genre')
    s=stage(i)
    panel=bg().copy();d=ImageDraw.Draw(panel)
    # Single, original proof surface; no reused screenshot, brand, or private footage.
    d.rounded_rectangle((44,30,1036,858),radius=38,fill='#0c263a',outline='#276781',width=3)
    d.rounded_rectangle((75,55,376,117),radius=22,fill='#174a59')
    d.text((102,65),'架空データ / 検証例',font=font(30),fill='#9df5ee')
    title=GENRES[genre]
    assert_text_fits(d,(80,136),title,64,(75,128,1020,223))
    d.text((80,136),title,font=font(64),fill='#ffffff')
    d.text((80,230),'元データ → 計算 → 確認',font=font(34),fill='#b2d9e5')

    # Crisp high-resolution source rows; selection indicator moves over time.
    d.rounded_rectangle((76,309,1004,615),radius=24,fill='#e9f4f7')
    d.rounded_rectangle((76,309,1004,383),radius=22,fill='#0b5267')
    d.rectangle((76,360,1004,383),fill='#0b5267')
    for x,txt in ((112,'月'),(490,'営業A'),(778,'営業B')):
        d.text((x,323),txt,font=font(37),fill='#f5ffff')
    selected=0 if i<16 else (1 if i<28 else 2)
    for j,(month,(a,b)) in enumerate(DATA.items()):
        y=388+j*75
        if j==selected and s==0:
            d.rounded_rectangle((88,y+3,990,y+72),radius=16,fill='#b6f1f1')
        elif j%2:
            d.rectangle((77,y,1003,y+75),fill='#d9e8ed')
        for x,txt in ((112,month),(495,str(a)),(783,str(b))):
            d.text((x,y+9),txt,font=font(41),fill='#0a2a3d')
    # Stage 0: animated source scan; stage 1: show arithmetic; stage 2: validated totals.
    d.rounded_rectangle((76,646,1004,824),radius=24,fill='#092032',outline='#1c7384',width=3)
    if s==0:
        d.text((111,668),'01  元データを読む',font=font(47),fill='#ffffff')
        d.text((113,743),'4月・5月・6月を順番に確認',font=font(33),fill='#70dce5')
        p=ease(i/26)
        d.rounded_rectangle((112,797,112+int(845*p),806),radius=4,fill='#4fe6d4')
    elif s==1:
        d.text((111,662),'02  合計を計算',font=font(47),fill='#ffffff')
        a='12 + 16 + 18 = 46';b='8 + 9 + 12 = 29'
        d.text((114,724),a,font=font(38),fill='#a1efff')
        if i>=40:d.text((114,775),b,font=font(38),fill='#ffd391')
    else:
        d.text((111,663),'03  数字の一致を確認',font=font(43),fill='#ffffff')
        p=ease((i-56)/13)
        d.rounded_rectangle((110,727,966,810),radius=20,fill='#14544e',outline='#40f0cb',width=3)
        d.text((135,742),'営業A  46   /   営業B  29',font=font(40),fill='#ffffff')
        if p>.65:
            d.ellipse((891,669,943,721),fill='#3de8b8')
            d.line((901,695,914,708,935,680),fill='#052a24',width=6,joint='curve')
    # Subtle moving side accent (different from previous chart/static zoom approach).
    y=int(160+20*math.sin(i/8))
    d.rounded_rectangle((1018,y,1026,y+130),radius=4,fill='#55e9e0')
    # Replace the *whole* scene header and visual body, not just the center.
    # Prevents leftover source cards and partial Japanese headlines at the seams.
    im=Image.new('RGB',(1080,1358),'#050e19')
    hd=ImageDraw.Draw(im)
    hd.text((44,25),'AIの回答を確認する',font=font(58),fill='#f5fbff')
    hd.text((44,107),'数字・日付・根拠を見る',font=font(36),fill='#b5c8d7')
    im.paste(panel,(0,198))
    hd=ImageDraw.Draw(im)
    hd.rounded_rectangle((76,1150,1004,1255),radius=22,fill='#0c263a',outline='#2a7782',width=2)
    hd.text((115,1172),'数値は必ず元データと照合',font=font(39),fill='#a9f5eb')
    return im

def media_info(path):
    obj=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))
    v=next((x for x in obj['streams'] if x['codec_type']=='video'),None)
    a=next((x for x in obj['streams'] if x['codec_type']=='audio'),None)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],
       int(v.get('nb_frames') or 0),a['codec_name'],a['sample_rate']) != \
       ('h264',1080,1920,'30/1',691,'aac','48000'):
        raise ValueError('unexpected media format')

def contract(source,output,manifest,genre):
    source,output=Path(source),Path(output)
    if genre not in GENRES or not source.is_file() or source.resolve()==output.resolve() or output.exists():
        raise ValueError('invalid source/output/genre; overwrite prohibited')
    if manifest!={**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('fail-closed manifest / source SHA mismatch')
    media_info(source)
    return source,output

def render(source,output,manifest,genre='ai_work'):
    source,output=contract(source,output,manifest,genre)
    with tempfile.TemporaryDirectory(prefix='cycle867_') as tmp:
        folder=Path(tmp)
        for i in range(COUNT):
            draw_frame(i,genre).save(folder/f'{i:03d}.jpg',quality=93,subsampling=0)
        filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
              f'[0:v][new]overlay=x=0:y={ROI[1]}:enable=\'between(n,{START},{START+COUNT-1})\':'
              f'eof_action=pass:repeatlast=0:format=auto[v]')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
             '-framerate','30','-start_number','0','-i',str(folder/'%03d.jpg'),
             '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
             '-preset','ultrafast','-crf','20','-pix_fmt','yuv420p','-r','30',
             '-frames:v',str(FRAMES),'-c:a','copy','-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True,timeout=240)
    media_info(output)
    return {'source_sha256':sha256(source),'output_sha256':sha256(output),
            'changed_frames':COUNT,'frame_range':[START,START+COUNT-1],
            'caption_safe_end_y':SAFE_END_Y,'genres_supported':len(GENRES),
            'genre_rendered':genre,'fictional_totals':TOTALS,'policy':POLICY}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--manifest',required=True);p.add_argument('--report',required=True)
    p.add_argument('--genre',default='ai_work');a=p.parse_args()
    rep=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre)
    Path(a.report).write_text(json.dumps(rep,ensure_ascii=False,indent=2),encoding='utf-8')