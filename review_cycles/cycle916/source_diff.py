"""Cycle916: original source-versus-draft correction animation, internal review only.
Generates 75 original RGB frames for 14.5–17.0s (scene06).
No network, posting, secrets, private inputs or copyrighted reference artwork.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS, FRAMES, START_FRAME, OVERLAY_Y = 1080, 1130, 30, 75, 435, 300
CAPTION_Y = 1490
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
 'ai_work':('売上データ', '#3DE4E3'),
 'business':('営業記録', '#7AAEFF'),
 'learning':('学習記録', '#B3A4FF'),
 'health':('生活記録', '#7AE0B7'),
 'beauty':('ケア記録', '#FFA9C9'),
 'travel':('旅程記録', '#78D5FF'),
 'money':('支出記録', '#91DCA6'),
 'cooking':('材料記録', '#FFC88A'),
 'pets':('お世話記録', '#F6D58B'),
 'entertainment':('企画記録', '#D6ACFF'),
}
def font(size, bold=False):
 return ImageFont.truetype(BOLD if bold else FONT, size)
def ease(x):
 x=max(0.,min(1.,x));return x*x*(3-2*x)
def stage(frame):
 if not 0 <= frame < FRAMES: raise ValueError('invalid frame')
 return min(2,frame//25)
def validate(genre):
 if genre not in GENRES:raise ValueError('invalid genre')
 if OVERLAY_Y+H>=CAPTION_Y:raise ValueError('caption collision')
 if len(GENRES)!=10 or START_FRAME!=435 or FRAMES!=75:raise ValueError('unsafe settings')
 return True
def background():
 im=Image.new('RGBA',(W,H),'#06172B')
 glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow)
 g.ellipse((-200,-230,600,560),fill=(29,183,236,48))
 g.ellipse((540,300,1280,1160),fill=(79,100,238,32))
 im=Image.alpha_composite(im,glow.filter(ImageFilter.GaussianBlur(110)))
 d=ImageDraw.Draw(im)
 for x in range(0,W,80):d.line((x,0,x,H),fill=(28,57,77,90),width=1)
 for y in range(0,H,80):d.line((0,y,W,y),fill=(28,57,77,90),width=1)
 d.rounded_rectangle((48,55,1032,1080),radius=44,fill='#0D243B',outline='#37617B',width=3)
 d.rounded_rectangle((83,92,997,183),radius=25,fill='#183E56')
 d.text((118,113),'元データで差分を確認',font=font(44,True),fill='#FFFFFF')
 d.rounded_rectangle((85,224,995,949),radius=32,fill='#F4F8FC',outline='#A9D3E1',width=3)
 d.text((119,255),'STEP 1 / AIの下書き',font=font(34,True),fill='#3C6075')
 d.rounded_rectangle((116,321,962,510),radius=23,fill='#FFFFFF',outline='#D3E1E9',width=3)
 d.text((153,342),'6月・記録A',font=font(41,True),fill='#24435B')
 d.text((153,413),'下書き',font=font(33),fill='#6A8393')
 d.text((400,386),'17',font=font(88,True),fill='#D75164')
 d.text((550,408),'→',font=font(65,True),fill='#7293A5')
 d.text((700,386),'18',font=font(88,True),fill='#20A59B')
 d.text((120,549),'STEP 2 / 元データと照合',font=font(34,True),fill='#3C6075')
 d.rounded_rectangle((118,610,960,769),radius=21,fill='#E5F4FA',outline='#B3DDEB',width=3)
 d.text((155,627),'元データ（架空の例）',font=font(32,True),fill='#27566B')
 d.text((160,696),'6月 / 記録A',font=font(37,True),fill='#24435B')
 d.text((742,683),'18',font=font(62,True),fill='#0C8E84')
 d.text((120,801),'STEP 3 / 確認してから反映',font=font(34,True),fill='#3C6075')
 d.rounded_rectangle((117,865,960,924),radius=15,fill='#E6F7EF')
 d.text((154,871),'数値を照合して、修正内容を確認',font=font(35,True),fill='#19645E')
 d.text((113,993),'架空データの編集例・実績や成果を示すものではありません',font=font(27),fill='#B9CFDC')
 return im
_BG=None
def render(frame, genre='ai_work'):
 global _BG
 validate(genre)
 if not 0<=frame<FRAMES:raise ValueError('invalid frame')
 if _BG is None:_BG=background()
 name,accent=GENRES[genre]
 im=_BG.copy();d=ImageDraw.Draw(im)
 phase=stage(frame)
 d.rounded_rectangle((740,113,963,164),radius=15,fill=accent)
 d.text((757,119),f'{phase+1} / 3',font=font(29,True),fill='#08273B')
 d.rounded_rectangle((146,520,930,534),radius=8,fill='#E7EEF2')
 d.rounded_rectangle((146,520,146+int(784*ease((frame+1)/FRAMES)),534),radius=8,fill=accent)
 if phase==0:
  d.rounded_rectangle((371,372,514,475),radius=18,outline='#E25565',width=8)
  d.rounded_rectangle((135,612,943,756),radius=20,fill=(245,248,251,225))
  d.text((165,644),'まずは下書きの数値を確認',font=font(39,True),fill='#244D63')
 elif phase==1:
  d.rounded_rectangle((715,673,861,757),radius=17,outline='#F2AE47',width=8)
  d.rounded_rectangle((390,382,510,467),radius=17,outline='#E25565',width=6)
 else:
  d.rounded_rectangle((689,371,859,471),radius=18,outline='#16B69E',width=8)
  d.rounded_rectangle((137,860,939,931),radius=18,outline=accent,width=5)
  d.text((845,790),'✓',font=font(56,True),fill='#119D87')
 d.text((105,1029),name+' / 編集上の比較演出',font=font(25),fill='#B3CAD8')
 return im.convert('RGB')
def generate(directory:Path,genre:str):
 validate(genre);directory.mkdir(parents=True,exist_ok=True)
 for i in range(FRAMES):render(i,genre).save(directory/f'{i:03d}.png',compress_level=1)
 return FRAMES
def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--genre',choices=GENRES,default='ai_work')
 a=p.parse_args();print(generate(a.out,a.genre))
if __name__=='__main__':main()
