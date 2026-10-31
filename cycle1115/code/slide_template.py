#!/usr/bin/env python3
"""Offline Japanese slide core. Original vector graphics only; review-only output."""
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SIZE=(1080,1920)
GENRES={
    'ai_work':'#58E5D8','business':'#71B8FF','money':'#F6CA76',
    'learning':'#A4A1FF','health':'#6FE5B4','lifestyle':'#F5A5BF',
    'psychology':'#CE9CF6','science':'#8FDDFB','history':'#E4BA8C',
    'travel':'#81D8D3'
}
SCENES=[
 ('AI時短の始め方','最初の一歩で、結果が変わる','AIで仕事を速くするなら、','最初の一歩が大事。'),
 ('繰り返しを見つける','同じ作業は、改善の入口','まず、繰り返している','作業を書き出す。'),
 ('完成形を先に見せる','見本があると、指示が伝わる','次に、完成形の見本を','用意する。'),
 ('指示は3要素で','目的・条件・形式を分ける','指示は、目的と条件を','具体的に伝える。'),
 ('出力は必ず確認','AIの回答をそのまま使わない','最初の出力は、','必ず自分で確かめる。'),
 ('修正は1つずつ','曖昧な指示を、具体的に','違いがあれば、修正点を','一つずつ伝える。'),
 ('使える指示を保存','次回から、迷わない','使える指示は、','テンプレートに残す。'),
 ('小さな時短を習慣に','今日から1つ、始めよう','小さな時短を、','毎日の習慣にしよう。')
]
TIMES=[0,3.133333,5.6,8.233333,11.,13.733333,16.633333,19.166667,22.5]
REVEALS=[1.885,3.952,6.633,9.067,12.391,14.898,17.977,20.564]
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def font(n,bold=False):
    return ImageFont.truetype(BOLD if bold else REG,n)

def slide(index,genre='ai_work',reveal=True):
    if genre not in GENRES:raise ValueError('unknown genre')
    if not 0<=index<8:raise ValueError('scene out of range')
    accent=GENRES[genre]
    title,sub,line1,line2=SCENES[index]
    im=Image.new('RGB',SIZE,'#06192B')
    d=ImageDraw.Draw(im)
    for x in range(0,1080,90):d.line((x,0,x,1920),fill='#11273B')
    for y in range(0,1920,90):d.line((0,y,1080,y),fill='#11273B')
    d.rounded_rectangle((85,85,412,151),radius=20,fill='#103444',outline=accent,width=2)
    d.text((108,100),'AI / WORKFLOW',font=font(28,True),fill=accent)
    d.text((834,100),f'{index+1:02} / 08',font=font(30,True),fill='white')
    d.text((90,212),title,font=font(70,True),fill='white')
    d.text((90,327),sub,font=font(34),fill='#C3DBE4')
    d.line((90,432,990,432),fill=accent,width=2)
    # Large original diagram with no borrowed photographs or personal data.
    d.rounded_rectangle((85,545,994,1225),radius=36,fill='#102E40',outline='#376374',width=3)
    d.text((130,600),'TODAY / KEY POINT',font=font(31,True),fill=accent)
    steps=['選ぶ','書き出す','見本','目的・条件・形式','確認','1つずつ','保存','習慣']
    d.text((130,720),steps[index],font=font(90,True),fill='white')
    d.rounded_rectangle((130,935,950,1045),radius=24,fill='#1C515E')
    d.text((165,951),sub,font=font(32,True),fill='#E6FCFA')
    # Right 180px and bottom 270px reserved as app UI safe zone.
    d.rounded_rectangle((68,1365,872,1648),radius=26,fill='#041526',outline=accent,width=3)
    d.rounded_rectangle((89,1386,99,1625),radius=5,fill=accent)
    d.text((123,1394),'ナレーション',font=font(26,True),fill=accent)
    d.text((123,1450),line1,font=font(48,True),fill='white')
    if reveal:d.text((123,1530),line2,font=font(48,True),fill=accent)
    d.text((90,1760),'AI時短術 / 実務で使える基本',font=font(25),fill='#B6CCD8')
    d.text((90,1811),'確認用サンプル・社員承認前・投稿禁止',font=font(21),fill='#8EA7B7')
    return im

def render(source,output,genre='ai_work',seconds=2):
    """Synthetic CI renderer: static original slide + copied source audio."""
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    image=output.with_suffix('.png')
    slide(0,genre,True).save(image)
    cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate','30','-i',str(image),
         '-i',str(source),'-map','0:v:0','-map','1:a:0','-t',str(seconds),
         '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
         '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'output':str(output),'genre':genre,'review':'NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--seconds',type=float,default=2)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,a.seconds),ensure_ascii=False))
