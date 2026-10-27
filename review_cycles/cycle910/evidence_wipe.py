"""cycle910: review-only input->visualization evidence wipe, using source MP4 frames.
No external media, posting, private-media uploads, or claims of real performance gains.
"""
import argparse
import hashlib
import json
import math
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

FPS=30
START_FRAME=588  # scene 08 begins 19.600 s
END_FRAME=691    # source final frame is 690
W,H=1080,1050
OVERLAY_Y=355
SUBTITLE_Y=1490
POLICY='HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
PALETTES={
 'ai_work':('#2de3e0','#ffc857'), 'business':('#60a5fa','#f59e0b'),
 'learning':('#a78bfa','#fbbf24'), 'health':('#4ade80','#fb7185'),
 'beauty':('#f9a8d4','#facc15'), 'travel':('#38bdf8','#fb923c'),
 'money':('#4ade80','#fbbf24'), 'cooking':('#fb923c','#a3e635'),
 'pets':('#fbbf24','#60a5fa'), 'entertainment':('#c084fc','#fb7185')
}
GENRE_LABELS={
 'ai_work':('入力データ','可視化'), 'business':('元情報','整理結果'),
 'learning':('学習メモ','要点整理'), 'health':('元情報','確認事項'),
 'beauty':('確認項目','整理結果'), 'travel':('候補一覧','比較結果'),
 'money':('架空の数値','整理結果'), 'cooking':('材料一覧','工程整理'),
 'pets':('観察メモ','確認事項'), 'entertainment':('元情報','整理結果')
}

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def run(args):
 subprocess.run(args,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)

def frame(path,seconds):
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/'frame.png'
  run(['ffmpeg','-hide_banner','-loglevel','error','-ss',str(seconds),'-i',str(path),'-frames:v','1','-y',str(p)])
  return Image.open(p).convert('RGB').copy()

def font(size,bold=True):
 name='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
 return ImageFont.truetype(name,size)

def fit_crop(im, size):
 ow,oh=size
 s=max(ow/im.width,oh/im.height)
 im=im.resize((math.ceil(im.width*s),math.ceil(im.height*s)),Image.Resampling.LANCZOS)
 x=(im.width-ow)//2;y=(im.height-oh)//2
 return im.crop((x,y,x+ow,y+oh))

def card(draw,base,xywh,photo,label,accent,alpha=1):
 x,y,w,h=xywh
 draw.rounded_rectangle((x,y,x+w,y+h),radius=22,fill=(7,24,45,245),outline=accent,width=5)
 if alpha>0:
  crop=fit_crop(photo,(w-20,h-108)).convert('RGBA')
  crop.putalpha(int(255*alpha))
  base.alpha_composite(crop,(x+10,y+90))
 draw.rounded_rectangle((x+10,y+9,x+w-10,y+77),radius=15,fill=(7,24,45,255))
 draw.text((x+30,y+19),label,font=font(37),fill=accent)

def source_table(draw, x, y, w, h, accent):
    """Verified fictional numbers copied from the cycle908 source scene, not real sales."""
    draw.rounded_rectangle((x,y,x+w,y+h),radius=22,fill=(7,24,45,255),outline=accent,width=5)
    draw.text((x+24,y+17),'入力データ',font=font(37),fill=accent)
    draw.text((x+24,y+88),'月       A       B',font=font(35),fill='white')
    for j,(month,a,b) in enumerate([('4月',12,8),('5月',16,9),('6月',18,12)]):
        yy=y+165+j*105
        draw.rounded_rectangle((x+16,yy,x+w-16,yy+88),radius=12,fill=(17,54,77,255))
        draw.text((x+30,yy+20),f'{month}      {a:2}      {b:2}',font=font(35),fill='white')
    draw.line((x+20,y+510,x+w-20,y+510),fill=accent,width=3)
    draw.text((x+25,y+534),'合計  A 46  /  B 29',font=font(29),fill=accent)

def overlay_frame(i,before,after,genre):
 a,b=PALETTES[genre]
 lab1,lab2=GENRE_LABELS[genre]
 im=Image.new('RGBA',(W,H),(0,0,0,0));d=ImageDraw.Draw(im)
 # Review-only display, no claims of actual time savings or app operation.
 d.rounded_rectangle((28,10,1052,1027),radius=36,fill=(4,14,32,251),outline=(48,105,145,255),width=4)
 d.text((60,36),'入力データ → グラフ化まで',font=font(52),fill='white')
 d.rounded_rectangle((60,112,700,172),radius=13,fill=(15,46,67,255))
 d.text((79,119),'架空データ｜画面は編集用の再現',font=font(27),fill='#d5ecf4')
 # Two evidence pictures, with a left-to-right reveal in the first half.
 progress=max(0,min(1,(i-13)/38))
 source_table(d,55,210,468,622,a)
 card(d,im,(557,210,468,622),after,lab2,b,progress)
 # Cover second photo with a sliding dark curtain; transparent to reveal it.
 cover=int((1-progress)*440)
 if cover>0:
  d.rounded_rectangle((1025-cover,302,1015,822),radius=8,fill=(5,23,40,255))
  d.text((582,520),'確認中…',font=font(37),fill=b)
 # Connector arrow animates after first 0.4 sec.
 if i>=12:
  d.polygon([(523,495),(552,515),(523,535)],fill=b)
 # Evidence labels; these numbers are fictional and already used in the source clip.
 d.rounded_rectangle((95,858,985,949),radius=18,fill=(13,50,69,255))
 if i<45:
  line='元データを見て、結果を照合する'
 elif i<81:
  line='架空データの合計  A 46  /  B 29'
 else:
  line='数字の根拠を確認してから使う'
 d.text((125,877),line,font=font(36),fill='white')
 d.text((65,972),'REVIEW ONLY  •  PUBLICATION NOT APPROVED',font=font(19),fill='#9cb4c7')
 return im

def render(source,output,expected_sha,genre,frames_dir):
 if genre not in PALETTES: raise ValueError('unknown genre')
 if not str(output).endswith('REVIEW_ONLY.mp4'):raise ValueError('output must end in REVIEW_ONLY.mp4')
 if source.resolve()==output.resolve():raise ValueError('cannot overwrite source')
 if sha256(source)!=expected_sha:raise ValueError('source sha256 mismatch')
 if OVERLAY_Y+H>=SUBTITLE_Y:raise ValueError('subtitle safe area violated')
 before=frame(source,5.3).crop((80,420,1000,1350))
 after=frame(source,13.1).crop((80,420,1000,1350))
 frames_dir.mkdir(parents=True,exist_ok=True)
 for i in range(END_FRAME-START_FRAME):
  overlay_frame(i,before,after,genre).save(frames_dir/f'frame_{i:04d}.png',compress_level=1)
 output.parent.mkdir(parents=True,exist_ok=True)
 # Preserve original Japanese AAC packets via -c:a copy.
 run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(source),'-framerate',str(FPS),'-i',str(frames_dir/'frame_%04d.png'),'-filter_complex',f'[1:v]format=rgba,setpts=PTS+{START_FRAME}/{FPS}/TB[ov];[0:v][ov]overlay=x=0:y={OVERLAY_Y}:eof_action=pass:format=auto,format=yuv420p[v]', '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy','-movflags','+faststart','-y',str(output)])
 return {'source_sha256':expected_sha,'output_sha256':sha256(output),'genre':genre,'policy':POLICY,'changed_frames':[START_FRAME,END_FRAME-1], 'subtitle_y_min':SUBTITLE_Y,'overlay_y_max':OVERLAY_Y+H,'independent_japanese_asr':'NOT_VERIFIED','rights':'UNVERIFIED'}

def main():
 p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--source-sha256',required=True);p.add_argument('--genre',default='ai_work');p.add_argument('--frames-dir',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
 a=p.parse_args();report=render(a.source,a.output,a.source_sha256,a.genre,a.frames_dir);a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
