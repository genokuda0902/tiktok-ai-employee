#!/usr/bin/env python3
"""Rights-safe Japanese first-scene declutter: original PIL art, original AAC copied.

Only scene 01 content region is replaced. Header, original narration, burned caption,
8 chapters, and other scenes are preserved. Not a publication approval.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = {
    'ai_work':'#26D7C7', 'beauty':'#F38AAE', 'romance_psychology':'#B292F4',
    'money_saving':'#EAC253','sales_business':'#5BB7FF','career':'#63D6DF',
    'health_lifestyle':'#58D793','science_trivia':'#DFA6FF',
    'travel_food':'#F5A455','product_comparison_lifestyle':'#55C2F5'
}
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
W,H=1080,1920
PANEL_TOP,PANEL_BOTTOM=150,1370

def font(size,bold=False):
    return ImageFont.truetype(BOLD if bold else REG,size,index=0)

def text_fit(draw, text, max_width, size, bold=False):
    f=font(size,bold)
    bbox=draw.textbbox((0,0),text,font=f)
    if bbox[2]-bbox[0]>max_width:
        raise ValueError(f'text overflow: {text} ({bbox[2]-bbox[0]}>{max_width})')
    return f

def draw_slide(genre='ai_work'):
    if genre not in GENRES: raise ValueError('unsupported genre')
    accent=GENRES[genre]
    im=Image.new('RGBA',(W,H),(0,0,0,0))
    d=ImageDraw.Draw(im)
    for y in range(PANEL_TOP,PANEL_BOTTOM):
        k=(y-PANEL_TOP)/(PANEL_BOTTOM-PANEL_TOP)
        d.line((0,y,W,y),fill=(6+int(3*k),18+int(5*k),35+int(8*k),255))
    for x,y,r in [(930,290,260),(90,900,160)]:
        d.ellipse((x-r,y-r,x+r,y+r),outline=(30,68,86,150),width=2)
    d.rounded_rectangle((55,188,1025,1155),radius=36,fill=(9,28,48,255),outline=(47,93,105,255),width=3)
    d.rounded_rectangle((92,222,340,275),radius=16,fill=(18,62,75,255))
    d.text((114,225),'01  /  FIRST STEP',font=text_fit(d,'01  /  FIRST STEP',300,29,True),fill=accent)
    d.text((92,305),'AIで仕事を速くする',font=text_fit(d,'AIで仕事を速くする',890,67,True),fill='#F5FAFF')
    d.text((92,403),'最初の1つを決める',font=text_fit(d,'最初の1つを決める',890,61,True),fill=accent)
    d.rounded_rectangle((92,503,988,601),radius=22,fill=(17,70,78,255),outline=(40,156,151,255),width=2)
    d.text((126,522),'完成形を先に見る',font=text_fit(d,'完成形を先に見る',820,48,True),fill='#F6FFFF')
    d.text((95,631),'週次報告｜完成サンプル',font=text_fit(d,'週次報告｜完成サンプル',840,38,True),fill='#D7E8F0')
    items=[('1','今週の成果','問い合わせ対応の流れを整理'),
           ('2','気づき','説明が長くなりがちだった'),
           ('3','次の行動','冒頭の案内を短く伝える')]
    for i,(num,head,body) in enumerate(items):
        y=702+i*124
        d.rounded_rectangle((95,y,986,y+106),radius=20,fill=(232,244,247,255))
        d.rounded_rectangle((111,y+17,180,y+88),radius=14,fill=accent)
        d.text((130,y+22),num,font=font(40,True),fill='#061927')
        d.text((205,y+9),head,font=text_fit(d,head,710,37,True),fill='#142838')
        d.text((205,y+56),body,font=text_fit(d,body,730,28),fill='#355266')
    d.text((98,1100),'※架空サンプル・実績ではありません',font=text_fit(d,'※架空サンプル・実績ではありません',830,24),fill='#A5BFC9')
    return im

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(path)],text=True))

def render(source,target,genre='ai_work',preview=None,ffmpeg='ffmpeg'):
    info=probe(source)
    v=next(s for s in info['streams'] if s['codec_type']=='video')
    a=[s for s in info['streams'] if s['codec_type']=='audio']
    if (v['width'],v['height'],v['r_frame_rate']) != (1080,1920,'30/1') or not a:
        raise ValueError('1080x1920/30fps source with audio required')
    chapters=info.get('chapters',[])
    if len(chapters)<2 or abs(float(chapters[1]['start_time'])-2.633)>0.05:
        raise ValueError('source chapter 01 timing mismatch; fail closed')
    png=Path(preview or str(target)+'.overlay.png')
    draw_slide(genre).save(png)
    cmd=[ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(source),'-loop','1','-framerate','30','-i',str(png),
         '-filter_complex',"[0:v:0][1:v:0]overlay=0:0:enable='lt(t,2.633333)':format=auto,format=yuv420p[v]",
         '-map','[v]','-map','0:a:0','-map_metadata','0','-map_chapters','0',
         '-c:v','libx264','-preset','veryfast','-crf','17','-threads','4','-r','30',
         '-c:a','copy','-frames:v',str(int(v.get('nb_frames') or 675)),'-movflags','+faststart',str(target)]
    subprocess.run(cmd,check=True)
    return {'source':str(source),'output':str(target),'genre':genre,'changed_chapter':'01/08',
            'changed_region':[0,PANEL_TOP,W,PANEL_BOTTOM],'audio':'stream copy','status':'HUMAN_REVIEW'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('target',type=Path)
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--preview',type=Path)
    args=p.parse_args()
    print(json.dumps(render(args.source,args.target,args.genre,args.preview),ensure_ascii=False))
if __name__=='__main__':main()
