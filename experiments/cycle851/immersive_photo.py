"""Offline, review-only immersive photo-story compositor for ten genres.
Alternative to cycle850 boxed-photo layout. No posting, network, purchases or merges.
Source images and narration require human rights review before publication.
"""
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance

W,H,FPS,FRAME_COUNT=1080,1920,30,691
CARD=(42,190,1038,1550)
CW,CH=CARD[2]-CARD[0],CARD[3]-CARD[1]
ACCENTS={
 'ai_work':'#4AE6D7','sales_business':'#FFCA75','beauty':'#F2ACF5',
 'romance':'#FF9DB9','saving':'#6FE1B0','career':'#FFC19D',
 'wellness':'#B3E484','science':'#8CCAFF','travel_food':'#84D9F3',
 'product_comparison_lifestyle':'#E5B2FF'
}
REVIEW_ONLY={'publication_approved':False,'employee_approved':False,
             'rights_confirmed':False,'automatic_posting':False}
SCENES=[
 ('AIで仕事を','もっと速く','まずは小さな作業から'),
 ('繰り返す作業を','見つけよう','毎日の定型作業を1つ書く'),
 ('完成形の見本を','先に用意','理想の出力を具体的に示す'),
 ('目的と条件を','具体的に伝える','目的・条件・形式をそろえる'),
 ('AIの回答を','自分で確認','数字・日付・根拠をチェック'),
 ('修正点は','一つずつ','直すポイントを1つに絞る'),
 ('良い指示は','保存して再利用','使えた指示を残しておく'),
 ('小さな時短を','毎日の習慣に','明日も1つ、続けてみる'),
]
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def font(n,bold=True):return ImageFont.truetype(FONT if bold else FONT_REG,n)
def validate(photos,beats,genre):
 if genre not in ACCENTS or len(ACCENTS)!=10:raise ValueError('genre configuration invalid')
 if len(photos)!=8 or not all(Path(x).is_file() for x in photos):raise ValueError('exactly 8 source images required')
 if len(beats)!=24:raise ValueError('24 caption beats required')
 end=0
 for b in beats:
  a,z=float(b['start']),float(b['end'])
  if a<end or z<=a or z>23.04:raise ValueError('invalid caption timing')
  end=z
 if any(REVIEW_ONLY.values()):raise ValueError('publication safety policy invalid')
 return True
def photo_card(path):
 src=Image.open(path).convert('RGB')
 backdrop=ImageOps.fit(src,(CW,CH),method=Image.Resampling.LANCZOS)
 backdrop=backdrop.filter(ImageFilter.GaussianBlur(28))
 backdrop=ImageEnhance.Color(backdrop).enhance(.85)
 sharp=ImageOps.contain(src,(CW-38,CH-120),method=Image.Resampling.LANCZOS)
 sharp=sharp.filter(ImageFilter.UnsharpMask(radius=1.25,percent=95,threshold=4))
 backdrop.paste(sharp,((CW-sharp.width)//2,(CH-sharp.height)//2))
 return backdrop
def alpha_gradient(layer,top,bottom,color,alpha_start,alpha_end):
 d=ImageDraw.Draw(layer);r,g,b=color
 for y in range(top,bottom):
  t=(y-top)/max(1,bottom-top-1)
  a=int(alpha_start+(alpha_end-alpha_start)*t)
  d.line((0,y,W,y),fill=(r,g,b,a))
def foreground(idx,genre):
 accent=ACCENTS[genre]
 out=Image.new('RGBA',(W,H),(7,19,30,255));d=ImageDraw.Draw(out)
 d.rectangle(CARD,fill=(0,0,0,0))
 alpha_gradient(out,190,810,(3,14,24),215,10)
 alpha_gradient(out,1080,1550,(3,14,24),0,225)
 d=ImageDraw.Draw(out)
 d.rounded_rectangle((66,66,338,132),radius=30,fill=(8,32,45,255))
 d.text((95,78),'AI  /  WORK',font=font(29),fill=accent)
 d.text((898,82),f'{idx+1:02d} / 08',font=font(29),fill='white')
 for j in range(8):
  d.rounded_rectangle((67+j*119,154,156+j*119,165),radius=6,
                      fill=accent if j<=idx else '#344F5D')
 d.rounded_rectangle((78,244,287,300),radius=20,fill=(8,27,40,240))
 d.text((103,251),f'STEP  {idx+1:02d}',font=font(28),fill=accent)
 title1,title2,action=SCENES[idx]
 d.text((75,336),title1,font=font(72),fill='white',stroke_width=3,stroke_fill='#07131E')
 size=78 if len(title2)<9 else 67
 d.text((75,436),title2,font=font(size),fill=accent,stroke_width=3,stroke_fill='#07131E')
 d.rounded_rectangle((74,1192,1006,1288),radius=22,fill=(7,25,36,238))
 d.rectangle((98,1212,107,1266),fill=accent)
 d.text((135,1210),action,font=font(43),fill='white')
 d.rounded_rectangle((65,1384,1015,1594),radius=28,fill=(7,25,39,245),
                     outline=(88,130,143,255),width=2)
 d.rectangle((89,1418,99,1565),fill=accent)
 d.rounded_rectangle((67,1650,1013,1788),radius=25,fill='#0C2836')
 d.text((94,1674),'今日からできること',font=font(27),fill=accent)
 d.text((94,1720),action,font=font(36),fill='white')
 d.text((75,1845),'HUMAN REVIEW  /  PUBLICATION NOT APPROVED',
        font=font(19,False),fill='#91A6AE')
 return out
def ass_time(s):
 cs=round(s*100);h,cs=divmod(cs,360000);m,cs=divmod(cs,6000);ss,cs=divmod(cs,100)
 return f'{h}:{m:02d}:{ss:02d}.{cs:02d}'
def write_ass(beats,path):
 header=('[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n'
 '[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n'
 'Style: Default,Noto Sans CJK JP,72,&H00FFFFFF,&H00FFFFFF,&H00000E19,&H00000000,-1,0,0,0,100,100,0,0,1,3,0,5,50,50,0,1\n'
 '[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')
 lines=[]
 for b in beats:
  value=str(b['text']).replace('{','').replace('}','')
  lines.append(f"Dialogue: 0,{ass_time(float(b['start']))},{ass_time(float(b['end']))},Default,,0,0,0,,{{\\an5\\pos(540,1490)}}{value}")
 Path(path).write_text(header+'\n'.join(lines)+'\n',encoding='utf-8')
def render(photos,beats_path,narration_video,output,workdir,genre='ai_work'):
 beats=json.loads(Path(beats_path).read_text(encoding='utf-8'))
 validate(photos,beats,genre)
 wd=Path(workdir);wd.mkdir(parents=True,exist_ok=True)
 for i,p in enumerate(photos):
  photo_card(p).save(wd/f'card_{i+1:02d}.png')
  foreground(i,genre).save(wd/f'fg_{i+1:02d}.png')
 write_ass(beats,wd/'captions.ass')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-filter_complex_threads','2']
 for i in range(8):
  frames=96 if i==7 else 94
  duration=f'{frames/FPS:.9f}'
  cmd+=['-loop','1','-framerate','30','-t',duration,'-i',str(wd/f'card_{i+1:02d}.png')]
  cmd+=['-loop','1','-framerate','30','-t',duration,'-i',str(wd/f'fg_{i+1:02d}.png')]
 cmd+=['-i',str(narration_video)]
 filt=[]
 for i in range(8):
  frames=96 if i==7 else 94
  p=f'min(on/{frames-1},1)';dr=1 if i%2==0 else -1
  z=f'1+0.032*{p}'
  x=f'(iw-iw/zoom)*(0.5+{dr}*0.10*{p})'
  y=f'(ih-ih/zoom)*(0.5-0.06*{p})'
  filt.extend([
   f'[{2*i}:v]zoompan=z=\'{z}\':x=\'{x}\':y=\'{y}\':d=1:s={CW}x{CH}:fps=30,format=rgba,pad=1080:1920:42:190:color=#07131e[card{i}]',
   f'[{2*i+1}:v]format=rgba[fg{i}]',
   f'[card{i}][fg{i}]overlay=0:0:format=auto:shortest=1,format=yuv420p,setsar=1[s{i}]'
  ])
 prev='s0'
 for i in range(1,8):
  filt.append(f'[{prev}][s{i}]xfade=transition=fade:duration=0.3:offset={i*85/30:.6f}[x{i}]');prev=f'x{i}'
 ass=str((wd/'captions.ass').resolve()).replace(':','\\:')
 filt.append(f'[{prev}]ass={ass}[v]')
 cmd+=['-filter_complex',';'.join(filt),'-map','[v]','-map','16:a:0',
       '-frames:v',str(FRAME_COUNT),'-c:v','libx264','-preset','ultrafast',
       '-crf','21','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
 subprocess.run(cmd,check=True)
 return Path(output)
if __name__=='__main__':
 p=argparse.ArgumentParser()
 p.add_argument('--photos',nargs=8,required=True)
 p.add_argument('--beats',required=True)
 p.add_argument('--narration-video',required=True)
 p.add_argument('--output',required=True)
 p.add_argument('--workdir',required=True)
 p.add_argument('--genre',default='ai_work')
 a=p.parse_args();print(render(a.photos,a.beats,a.narration_video,a.output,a.workdir,a.genre))
