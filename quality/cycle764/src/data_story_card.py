"""cycle764: Original, review-only 9:16 data-story cards for ten genres.

Edits only frames 96..194 of a supplied review MP4; inherited audio is copied.
This is an original reimplementation, not recovered v33 source or real AI UI.
"""
from __future__ import annotations
import argparse, hashlib, json, random, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1080,1920,30
STAGES=((96,128),(129,161),(162,194))
GENRES={
 'AI・仕事効率化':'#49e8d7','美容・身だしなみ':'#f4acd4',
 '恋愛・心理':'#f88ba6','お金・節約':'#edc979',
 '営業・ビジネス':'#82c0ff','転職・キャリア':'#a7b1ff',
 '健康・生活改善':'#87d6aa','雑学・科学':'#80ddec',
 '旅行・グルメ':'#f0b58d','商品比較・暮らし':'#d4b4f8'}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BASELINE_SHA='8eb243e7ef1cfcc4436a55696ac1484d83e8a26106e3a3a74898ba3376c183c5'
MONTHS=('1月','2月','3月','4月')


def sha256(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()


def check(manifest,source,expected_sha=BASELINE_SHA):
 if manifest.get('status')!='HUMAN_REVIEW' or manifest.get('post_policy')!='employee_manual_after_approval':raise ValueError('approval gate')
 if manifest.get('asset_origin')!='original_synthetic_pillow' or manifest.get('synthetic_data') is not True:raise ValueError('asset/data gate')
 if manifest.get('genre') not in GENRES:raise ValueError('unknown genre')
 sales=manifest.get('sales')
 if sales!=[120000,150000,200000,180000] or sum(sales)!=650000:raise ValueError('unsupported evidence')
 if sha256(source)!=expected_sha:raise ValueError('baseline SHA mismatch')


def f(size,bold=True):return ImageFont.truetype(FONT if bold else REG,size)
def col(s):return tuple(bytes.fromhex(s.lstrip('#')))

def card(stage,genre='AI・仕事効率化',sales=(120000,150000,200000,180000)):
 if stage not in range(3) or genre not in GENRES or tuple(sales)!=(120000,150000,200000,180000):raise ValueError('unsupported stage/genre/data')
 accent=col(GENRES[genre]); im=Image.new('RGB',(W,H)); d=ImageDraw.Draw(im)
 for y in range(H):
  q=y/H; d.line((0,y,W,y),fill=(int(6+9*q),int(16+19*q),int(37+29*q)))
 # Original depth: restrained blurred studio lights, no imported media.
 layer=Image.new('RGBA',(W,H)); g=ImageDraw.Draw(layer); rng=random.Random(764)
 for _ in range(20):
  x=rng.randrange(-100,1100); y=rng.randrange(80,1390); r=rng.randrange(25,105)
  g.ellipse((x-r,y-r,x+r,y+r),fill=(*accent,rng.randrange(12,38)))
 im=Image.alpha_composite(im.convert('RGBA'),layer.filter(ImageFilter.GaussianBlur(42)))
 d=ImageDraw.Draw(im)
 def box(coords,fill,outline=None,r=22,width=2):d.rounded_rectangle(coords,radius=r,fill=fill,outline=outline,width=width)
 def tx(x,y,s,size,color=(243,248,255),bold=True,anchor=None):d.text((x,y),s,font=f(size,bold),fill=color,anchor=anchor)
 box((65,75,487,150),(8,54,70),accent,23,3)
 tx(93,93,'AI時短ラボ / DATA 01',35)
 tx(70,215,'まずは4か月の',79)
 tx(70,327,'売上データを用意。',70,accent)
 tx(72,429,'※ 練習用の架空データです',34,(185,211,230),False)
 # Glass panel and one large table; eliminate duplicated mini-UI/caption layers.
 shadow=Image.new('RGBA',(W,H));sd=ImageDraw.Draw(shadow)
 sd.rounded_rectangle((76,530,938,1290),radius=36,fill=(0,0,0,180))
 im.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(28)));d=ImageDraw.Draw(im)
 box((65,505,935,1280),(10,32,55),accent,35,3)
 box((87,527,914,624),(18,63,82),None,20)
 tx(119,549,'月別売上データ',47)
 tx(838,555,'SAMPLE',25,accent,True,'mt')
 tx(130,652,'月',32,(165,201,219))
 tx(410,652,'売上（円）',32,(165,201,219))
 for i,(month,value) in enumerate(zip(MONTHS,sales)):
  y=711+i*111
  active=(stage==0 and i<2) or (stage==1 and i>=2) or (stage==2 and i==2)
  box((100,y,899,y+96),(24,81,94) if active else (14,43,64),accent if active else (41,84,105),17,3 if active else 1)
  tx(137,y+18,month,42)
  tx(380,y+19,f'{value:,}',41,accent if active else (232,244,252))
  box((704,y+33,704+int(150*value/200000),y+55),accent if active else (60,115,135),None,8)
 box((100,1172,900,1245),(6,74,83) if stage==2 else (16,57,72),accent,18,3)
 tx(130,1184,'合計',38)
 tx(846,1182,'650,000 円',43,accent if stage==2 else (240,247,252),True,'rt')
 # Short, consistent cue #2. No extra competing captions in bottom area.
 box((65,1360,932,1575),(3,18,39),accent,31,3)
 tx(108,1390,'VOICE / JP',28,accent)
 tx(497,1430,'まず、架空の4か月',56,(248,252,255),True,'mt')
 tx(497,1495,'データを用意。',57,(248,252,255),True,'mt')
 tx(72,1621,'操作イメージ / 架空データ / 社内確認用',25,(171,190,211),False)
 # TikTok UI reserve: y >= 1680 and rightmost 140px have no semantic text.
 return im.convert('RGB')


def render(source,out,manifest,assets,expected_sha=BASELINE_SHA):
 source=Path(source);out=Path(out);assets=Path(assets)
 check(manifest,source,expected_sha)
 out.parent.mkdir(parents=True,exist_ok=True);assets.mkdir(parents=True,exist_ok=True)
 for i in range(3):card(i,manifest['genre'],manifest['sales']).save(assets/f'stage{i}.png')
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
 for i in range(3):args+=['-loop','1','-framerate','30','-i',str(assets/f'stage{i}.png')]
 filt='[0:v]format=yuv420p[b];'
 last='b'
 for i,(lo,hi) in enumerate(STAGES):
  filt+=f"[{last}][{i+1}:v]overlay=0:0:enable='between(n,{lo},{hi})':shortest=1[v{i}];"
  last=f'v{i}'
 filt+=f'[{last}]format=yuv420p[out]'
 args+=['-filter_complex',filt,'-map','[out]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-r','30','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(out)]
 p=subprocess.run(args,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(p.stderr[-4000:])
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--assets',required=True)
 a=p.parse_args();render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.assets)
