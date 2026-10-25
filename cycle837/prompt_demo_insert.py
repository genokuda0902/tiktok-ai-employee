"""cycle837: ten-genre, offline-only prompt UI reproduction for human review.

This is a locally drawn demonstration, NOT ChatGPT or a real AI service.
No network, no posting, no access to private data. Do not publish without approval.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cycle833.focal_layout import GENRES, FRAMES

FPS=30
RECT=(62,390,1018,1390)
WIDTH,HEIGHT=1080,1920
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
PROMPTS={
 'ai_work':'この売上データを整理して、重要な点を3つ教えてください。',
 'sales_business':'架空の商談メモを要約して、次の確認事項を3つ教えてください。',
 'beauty':'架空のスキンケア記録から、続けやすい習慣を3つ挙げてください。',
 'romance':'架空の会話例をもとに、相手に伝わる言い方を3つ提案してください。',
 'saving':'架空の家計表を3項目に整理して、改善候補を示してください。',
 'career':'架空の業務記録から、改善できる行動を3つ整理してください。',
 'wellness':'架空の生活記録から、無理のない習慣を3つ提案してください。',
 'science':'架空の観察結果から、考えられる説明を3つ挙げてください。',
 'travel_food':'架空の旅行予定を整理して、移動の注意点を3つ示してください。',
 'productivity':'架空の作業リストから、優先すべき仕事を3つ整理してください。',
}

def scene_window(genre,scene=3,rect=RECT):
    if genre not in GENRES or scene not in range(len(FRAMES)) or type(scene)!=int:
        raise ValueError('Unknown genre/scene')
    l,t,r,b=rect
    if not (0<=l<r<=WIDTH and 0<=t<b<=1400<1452):
        raise ValueError('Caption/CTA safe zone must not be covered')
    return sum(FRAMES[:scene]),sum(FRAMES[:scene+1])

def check_manifest(m):
    required={'source_kind':'locally_rendered_ui','data_classification':'fictional',
              'contains_personal_data':False,'review_only':True,
              'publication_approved':False,'service_connection':False}
    if not isinstance(m,dict) or any(m.get(k)!=v for k,v in required.items()):
        raise ValueError('Fail closed: fictional, disconnected review-only UI required')

def make_demo(out:Path,genre='ai_work',scene=3):
    from PIL import Image,ImageDraw,ImageFont
    start,end=scene_window(genre,scene)
    prompt=PROMPTS[genre]
    frames=end-start
    accent=GENRES[genre][0]
    fw,fh=RECT[2]-RECT[0],RECT[3]-RECT[1]
    def font(size):return ImageFont.truetype(FONT,size)
    def label(d,xy,text,size,color='#e9f6f9'):
        d.text(xy,text,font=font(size),fill=color)
    def wrap(text,n):return [text[i:i+n] for i in range(0,len(text),n)]
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24',
         '-s',f'{fw}x{fh}','-r',str(FPS),'-i','-','-an','-c:v','libx264',
         '-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-movflags','+faststart',str(out)]
    p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for i in range(frames):
            progress=i/max(frames-1,1)
            im=Image.new('RGB',(fw,fh),'#0c1d2b')
            d=ImageDraw.Draw(im)
            d.rounded_rectangle((24,22,fw-24,fh-24),radius=30,fill='#122c3d',outline='#386477',width=3)
            d.rounded_rectangle((24,22,fw-24,106),radius=30,fill='#1d394b')
            d.rectangle((24,75,fw-24,106),fill='#1d394b')
            for k,c in enumerate(('#ef8b83','#f5c26b','#76d4a6')):
                d.ellipse((56+29*k,51,72+29*k,67),fill=c)
            label(d,(174,39),'LOCAL WORKFLOW / 04',28,'#e8f9f7')
            label(d,(54,142),'AIへの指示を具体化する',49)
            label(d,(56,217),'架空のデータを使った操作イメージ',26,'#9abcc7')
            d.rounded_rectangle((52,295,fw-52,757),radius=26,fill='#f3f8f9')
            label(d,(83,327),'指示入力',29,'#174357')
            d.rounded_rectangle((82,398,fw-82,601),radius=19,fill='#ffffff',outline='#a4c7d1',width=3)
            n=min(len(prompt),int(max(0,progress-.10)/.72*len(prompt)))
            shown=prompt[:n]
            for j,line in enumerate(wrap(shown,22)[:3]):
                label(d,(111,428+53*j),line,33,'#163746')
            if n<len(prompt) and i%20<12:
                line_count=(len(shown)-1)//22 if shown else 0
                cur=shown[line_count*22:]
                xx=111+int(d.textlength(cur,font=font(33)))
                yy=430+53*line_count
                d.line((xx,yy,xx,yy+38),fill='#0f9d9b',width=4)
            d.rounded_rectangle((84,626,476,690),radius=14,fill='#e0f3ef')
            label(d,(103,640),'架空の売上表.csv',26,'#21645b')
            active=n==len(prompt)
            d.rounded_rectangle((fw-275,622,fw-83,699),radius=19,fill=accent if active else '#aec3c9')
            label(d,(fw-248,641),'実行 →',32,'#082a32')
            d.rounded_rectangle((52,787,fw-52,902),radius=19,fill='#1c4555')
            if progress<.3:st='目的・条件・出力形式を整理'
            elif progress<.77:st='指示文を入力しています…'
            else:st='入力完了｜内容を確認'
            label(d,(81,816),st,31,'#a7eee1')
            label(d,(55,935),'ローカル再現UI / 実際のAI送信なし / 公開未承認',21,'#9cb8c3')
            p.stdin.write(im.tobytes())
    finally:
        p.stdin.close()
    if p.wait()!=0:raise RuntimeError('ffmpeg failed while generating UI demonstration')
    return out

def compose(source:Path,demo:Path,out:Path,manifest:dict,genre='ai_work',scene=3):
    check_manifest(manifest)
    start,end=scene_window(genre,scene)
    source,demo,out=map(Path,(source,demo,out))
    if not source.is_file() or not demo.is_file():raise FileNotFoundError('Missing local source or demo')
    if out.resolve() in (source.resolve(),demo.resolve()):raise ValueError('Refusing input overwrite')
    d=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration',
         '-of','default=noprint_wrappers=1:nokey=1',str(demo)],text=True))
    if d+.025<(end-start)/FPS:raise ValueError('Demo too short')
    l,t,r,b=RECT
    fc=(f'[1:v]trim=duration={(end-start)/FPS:.6f},setpts=PTS-STARTPTS,'
        f'format=rgba,fade=t=in:st=0:d=0.14:alpha=1,'
        f'fade=t=out:st={(end-start)/FPS-.17:.6f}:d=0.17:alpha=1,'
        f'setpts=PTS+{start/FPS:.6f}/TB[ui];'
        f'[0:v][ui]overlay={l}:{t}:eof_action=pass:format=auto,format=yuv420p[v]')
    out.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(demo),
         '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264',
         '-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-r',str(FPS),
         '-frames:v',str(sum(FRAMES)),'-c:a','copy','-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True)
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--genre',default='ai_work');a.add_argument('--scene',type=int,default=3)
    a.add_argument('--demo',required=True,type=Path);a.add_argument('--source',type=Path)
    a.add_argument('--out',type=Path);a.add_argument('--manifest',type=Path)
    v=a.parse_args();make_demo(v.demo,v.genre,v.scene)
    if v.source and v.out and v.manifest:
        compose(v.source,v.demo,v.out,json.loads(v.manifest.read_text()),v.genre,v.scene)
