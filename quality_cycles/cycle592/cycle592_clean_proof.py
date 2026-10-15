#!/usr/bin/env python3
"""Cycle592 original, synthetic 10-genre proof-slide renderer (review only).

The scene is a simulation, NOT actual AI, ChatGPT, or spreadsheet app footage.
Baseline MP4 remains private/local. This program never posts or uploads media.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import hashlib, json, math, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W,H,FPS=1080,1920,30
START,DURATION=4.0,2.0
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
# Colors vary; the proof logic and safe-zone layout are shared across genres.
GENRE_COLORS={
 'AI・仕事効率化':'#42E4D0','美容・身だしなみ':'#F8A8D6',
 '恋愛・心理':'#FFAEAB','お金・節約':'#F9D87C',
 '営業・ビジネス':'#71CBFF','転職・キャリア':'#BFB1FF',
 '健康・生活改善':'#9CE2AF','雑学・科学':'#7DE1F1',
 '旅行・グルメ':'#F3B883','商品比較・暮らし':'#9CC9FF',
}

@dataclass(frozen=True)
class Scene:
 genre: str='AI・仕事効率化'
 values: tuple[int,...]=(120,150,200,250)
 labels: tuple[str,...]=('1月','2月','3月','4月')
 total: int=720
 disclosure: str='架空データによる再現映像 / 実際のAI操作ではありません'

def validate(s:Scene)->bool:
 if s.genre not in GENRE_COLORS:raise ValueError('unsupported genre')
 if len(s.values)!=4 or len(s.labels)!=4:raise ValueError('four cells required')
 if any(type(x)!=int or x<0 or x>99999 for x in s.values):raise ValueError('invalid value')
 if sum(s.values)!=s.total:raise ValueError('false numeric evidence')
 if not s.disclosure or len(s.disclosure)>50:raise ValueError('missing disclosure')
 if len(set(s.labels))!=4:raise ValueError('labels must be distinct')
 return True

def color(code):return tuple(bytes.fromhex(code[1:]))
def font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def ease(t):t=max(0.,min(1.,t));return t*t*(3-2*t)
def center(d,xy,txt,sz,fill,bold=False):d.text(xy,txt,font=font(sz,bold),fill=fill,anchor='mm')

def draw_frame(idx:int,s:Scene=Scene()):
 validate(s)
 if not 0<=idx<60:raise ValueError('frame outside scene')
 t=idx/FPS; accent=color(GENRE_COLORS[s.genre]); white=(246,251,255); muted=(157,185,203)
 im=Image.new('RGB',(W,H),(7,17,33));d=ImageDraw.Draw(im)
 # Subtle original light-field, no third-party assets.
 for y in range(0,H,12):
  q=y/H;d.rectangle((0,y,W,y+12),fill=(7+int(5*q),17+int(7*q),33+int(12*q)))
 glow=Image.new('RGBA',(W,H),(0,0,0,0));g=ImageDraw.Draw(glow)
 g.ellipse((660+int(30*math.sin(t*2)),-150,1340,530),fill=(*accent,65))
 g.ellipse((-270,1120,340,1780),fill=(45,105,170,42))
 glow=glow.filter(ImageFilter.GaussianBlur(130));im=Image.alpha_composite(im.convert('RGBA'),glow).convert('RGB');d=ImageDraw.Draw(im)
 # Branding and 1-screen hierarchy.
 d.rounded_rectangle((68,88,1012,167),radius=20,fill=(22,55,77),outline=(65,123,150),width=2)
 d.text((101,105),'AI時短ラボ   /   03  解決策',font=font(35,True),fill=white)
 d.text((74,239),'4つの数字。',font=font(89,True),fill=white)
 d.text((74,353),'数式で、検算。',font=font(86,True),fill=accent)
 d.text((80,490),'元データ → 数式 → 結果を、同じ画面で確認',font=font(32),fill=muted)
 # Main original spreadsheet simulation with one visual focus.
 d.rounded_rectangle((70,575,1010,1398),radius=34,fill=(16,39,58),outline=(61,114,142),width=3)
 d.rounded_rectangle((70,575,1010,663),radius=34,fill=(22,74,82))
 d.rectangle((70,625,1010,663),fill=(22,74,82))
 d.ellipse((110,607,131,628),fill=(244,119,114));d.ellipse((145,607,166,628),fill=(249,206,112));d.ellipse((180,607,201,628),fill=(100,206,165))
 d.text((250,594),'月別売上 / DEMO SHEET',font=font(34,True),fill=white)
 # Input table: visible from the start, but focus cue travels row to row.
 d.rounded_rectangle((104,695,976,760),radius=12,fill=(31,66,85))
 d.text((140,709),'月',font=font(31,True),fill=muted)
 d.text((472,709),'B列 / 売上',font=font(31,True),fill=muted)
 d.text((803,709),'検証',font=font(31,True),fill=muted)
 current=min(3,int(t/.31))
 for j,(label,value) in enumerate(zip(s.labels,s.values)):
  y=786+j*105
  active=j==current and t<1.32
  bg=(33,93,104) if active else ((23,55,75) if j%2==0 else (24,50,69))
  d.rounded_rectangle((105,y,976,y+91),radius=12,fill=bg,outline=accent if active else (42,77,96),width=3 if active else 1)
  d.text((143,y+21),label,font=font(39,True),fill=white)
  d.text((486,y+20),str(value),font=font(42,True),fill=accent)
  if t>.3*j+.12:
   d.text((826,y+20),'✓',font=font(44,True),fill=(117,230,174))
 # Formula+result: 720 only after all rows checked.
 d.rounded_rectangle((104,1240,977,1368),radius=20,fill=(11,34,53),outline=accent,width=3)
 d.text((139,1260),'=SUM(B2:B5)',font=font(51,True),fill=white)
 if t>1.22:
  d.rounded_rectangle((730,1253,953,1355),radius=17,fill=accent)
  center(d,(843,1301),str(s.total),69,(7,32,43),True)
 else:
  center(d,(843,1301),'計算中',37,muted,True)
 # A SINGLE editorial caption; never duplicate it or overlap the table.
 d.rounded_rectangle((76,1444,1004,1570),radius=26,fill=(23,89,97),outline=accent,width=3)
 phase='数字を4つ確認' if t<.72 else ('数式で検算' if t<1.26 else '120 + 150 + 200 + 250 = 720')
 center(d,(540,1507),phase,45 if t>=1.26 else 53,white,True)
 d.text((81,1606),s.disclosure,font=font(25),fill=(144,169,187))
 # Keep y>1660 free of essential content to avoid TikTok control UI.
 return im

def call(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError(' '.join(map(str,cmd))+'\n'+p.stderr[-1800:])
 return p.stdout

def render_insert(path:Path,s:Scene):
 validate(s);path.parent.mkdir(parents=True,exist_ok=True)
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pixel_format','rgb24','-video_size',f'{W}x{H}','-framerate',str(FPS),'-i','-','-c:v','libx264','-preset','ultrafast','-crf','18','-pix_fmt','yuv420p',str(path)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
 try:
  for i in range(60):proc.stdin.write(draw_frame(i,s).tobytes())
  proc.stdin.close();error=proc.stderr.read();code=proc.wait()
  if code:raise RuntimeError(error.decode(errors='replace')[-2000:])
 except Exception:
  proc.kill();proc.wait();raise
 return path

def compose(baseline:Path,insert:Path,out:Path):
 if not baseline.is_file():raise FileNotFoundError(baseline)
 graph=f'[1:v]setpts=PTS-STARTPTS+{START}/TB[ins];[0:v][ins]overlay=x=0:y=0:eof_action=pass:format=auto[v]'
 call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(baseline),'-i',str(insert),'-filter_complex',graph,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-r','30','-frames:v','600','-c:a','copy','-movflags','+faststart',str(out)])
 return out

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(call(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,avg_frame_rate,sample_rate:format=duration,size','-of','json',str(p)]))

def main():
 a=argparse.ArgumentParser();a.add_argument('--baseline',type=Path,required=True);a.add_argument('--out',type=Path,required=True);a.add_argument('--insert',type=Path,required=True);a.add_argument('--qa',type=Path,required=True);a.add_argument('--genre',default='AI・仕事効率化');args=a.parse_args()
 s=Scene(genre=args.genre);render_insert(args.insert,s);compose(args.baseline,args.insert,args.out)
 qa={'cycle':592,'baseline_sha256':sha(args.baseline),'output_sha256':sha(args.out),'ffprobe':probe(args.out),'synthetic':True,'genre':s.genre,'genre_count':len(GENRE_COLORS),'numeric_proof':validate(s),'narration_generated':False,'voice_caption_semantic_sync_verified':False,'rights_approved':False,'quality':'HUMAN_REVIEW','publication':'PUBLICATION_NOT_APPROVED'}
 args.qa.write_text(json.dumps(qa,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'output':str(args.out),'sha256':qa['output_sha256']},ensure_ascii=False))
if __name__=='__main__':main()
