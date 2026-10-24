"""Cycle826: safe-zone captions and a before/after hook using one shared local/CI renderer.

No third-party imagery, real screenshots, personal data, or publication.
Requires Pillow, numpy, ffmpeg; optional OpenCV for perspective (fallback Pillow).
Genre theme catalog is shared; only ai_work has an approved review script.
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops
import numpy as np
import importlib.util
RAIL_PATH=Path(__file__).with_name("action_rail.py")
HOOK_PATH=Path(__file__).with_name("hook826.py")
hook_spec=importlib.util.spec_from_file_location("cycle826_hook",HOOK_PATH)
hook=importlib.util.module_from_spec(hook_spec)
hook_spec.loader.exec_module(hook)
rail_spec=importlib.util.spec_from_file_location("cycle825_action_rail",RAIL_PATH)
rail=importlib.util.module_from_spec(rail_spec)
rail_spec.loader.exec_module(rail)

W,H=1080,1920
COLORS={'ai_work':'#38C6C0','beauty':'#D96C96','love_psychology':'#9B86D9',
 'money_saving':'#D8A24A','sales_business':'#19A58B','career':'#6D8FDF',
 'health_life':'#81B479','science':'#41A6CC','travel_food':'#DF9562',
 'product_life':'#A985D2'}
TITLE=[('その作業、毎日手入力？','AIに任せる前に「分ける」'),('毎日の「繰り返し」を探す','何度もやる作業がヒント'),
 ('完成見本を先に用意','欲しい形を見せる'),('伝えるのは、この3点','目的・条件・見本'),
 ('AIの回答は必ず確認','数字・日付・根拠をチェック'),('修正は一つずつ','どこを直すか明確に'),
 ('良い指示を保存する','次から迷わない仕組み'),('小さな時短を積み重ねる','まずは今日ひとつ')]
SPEECH=['AIで仕事を早くするなら、最初の一歩が大事。','まず、繰り返している作業を書き出す。',
 '次に、完成形の見本を用意する。','指示は、目的と条件を具体的に伝える。',
 '最初の出力は、必ず自分で確かめる。','違いがあれば、修正点を一つずつ伝える。',
 '使える指示は、テンプレートに残す。','小さな時短を、毎日の習慣にしよう。']
PHRASES=[['AIで仕事を','早くするなら、','最初の一歩が大事。'],
 ['まず、繰り返している','作業を','書き出す。'],
 ['次に、完成形の','見本を','用意する。'],
 ['指示は、目的と条件を','具体的に','伝える。'],
 ['最初の出力は、','必ず自分で','確かめる。'],
 ['違いがあれば、','修正点を一つずつ','伝える。'],
 ['使える指示は、','テンプレートに','残す。'],
 ['小さな時短を、','毎日の習慣に','しよう。']]
FRAMES=[100,92,91,98,98,101,89,106]
ACTION=rail.ACTIONS
assert len(COLORS)==10 and sum(FRAMES)==775 and len(ACTION)==8
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def font(size,bold=True):
 return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,size)

def rgb(c):return tuple(bytes.fromhex(c.lstrip('#')))

def gradient(top,bottom,h,w=W):
 a=np.array(rgb(top),dtype=np.float32);b=np.array(rgb(bottom),dtype=np.float32)
 t=np.linspace(0,1,h,dtype=np.float32)[:,None,None]
 v=(a[None,None,:]*(1-t)+b[None,None,:]*t).astype('uint8')
 return Image.fromarray(np.broadcast_to(v,(h,w,3)).copy(),'RGB')

def shadow(im,rect,blur=25,opacity=65,radius=20,offset=(0,14)):
 l=Image.new('RGBA',im.size,(0,0,0,0));d=ImageDraw.Draw(l)
 x1,y1,x2,y2=rect;dx,dy=offset
 d.rounded_rectangle((x1+dx,y1+dy,x2+dx,y2+dy),radius=radius,fill=(8,23,29,opacity))
 im.alpha_composite(l.filter(ImageFilter.GaussianBlur(blur)))

def text(d,xy,s,size,color='#193447',anchor='lm',bold=True):
 d.text(xy,s,font=font(size,bold),fill=color,anchor=anchor)

def rect(d,coords,fill,r=14,outline=None,width=2):
 d.rounded_rectangle(coords,radius=r,fill=fill,outline=outline,width=width)

def screen_content(idx,accent):
 """Fictional, original task-specific content; all values illustrative."""
 im=Image.new('RGB',(780,460),'#F8FBFC');d=ImageDraw.Draw(im)
 rect(d,(0,0,780,54),'#1D394B',7)
 for j,c in enumerate(['#EC8B81','#E5BF72','#68C4A9']):d.ellipse((18+j*27,18,31+j*27,31),fill=c)
 text(d,(118,28),'WORKSPACE  /  架空デモ',20,'#D7E7ED')
 text(d,(749,28),f'{idx+1:02}/08',20,'#B6CDD7','rm')
 if idx==0:
  text(d,(32,92),'AIへ渡す前の作業整理',31)
  for j,(label,sub) in enumerate([('情報を集める','INPUT'),('下書きを作る','DRAFT'),('確認して使う','REVIEW')]):
   x=28+j*248;rect(d,(x,138,x+228,347),'#EAF3F5',17)
   rect(d,(x+76,164,x+150,235),accent,17)
   text(d,(x+113,199),str(j+1),38,'#FFFFFF','mm')
   text(d,(x+114,280),label,24,'#183447','mm')
   text(d,(x+114,314),sub,16,'#65828E','mm',False)
  text(d,(390,409),'作業を分ける → AIを使う',24,'#197E7B','mm')
 elif idx==1:
  text(d,(32,89),'繰り返している作業',30)
  for j,(label,when) in enumerate([('日報の集計','毎日'),('定型メール','毎日'),('会議メモの整理','週3'),('予定の転記','週5')]):
   y=124+j*72;rect(d,(32,y,746,y+62),'#E8F3F5',10)
   d.ellipse((50,y+18,76,y+44),fill=accent if j<2 else '#FFFFFF',outline=accent,width=3)
   text(d,(96,y+32),label,24)
   text(d,(712,y+32),when,20,'#67818B','rm')
 elif idx==2:
  text(d,(32,91),'完成形の見本｜議事録',30)
  for j,(k,v) in enumerate([('日付','10月25日'),('議題','業務の効率化'),('決定','日報集計を簡略化'),('担当','確認後に共有')]):
   y=137+j*65;rect(d,(32,y,746,y+60),'#E9F3F5' if j%2==0 else '#F5F9FA',10)
   text(d,(58,y+30),k,24,'#67818B');text(d,(276,y+30),v,25)
  rect(d,(238,407,542,449),accent,13);text(d,(390,427),'この形式で出力',23,'#FFFFFF','mm')
 elif idx==3:
  text(d,(32,88),'良い指示文の3要素',30)
  for j,(k,v) in enumerate([('目的','会議内容を要約'),('条件','200文字・箇条書き'),('見本','指定の表に合わせる')]):
   y=127+j*99;rect(d,(30,y,748,y+83),'#E8F3F5',15)
   rect(d,(48,y+18,159,y+65),accent,11);text(d,(104,y+41),k,24,'#FFFFFF','mm')
   text(d,(188,y+41),v,25)
  text(d,(390,425),'曖昧な依頼を減らす',25,'#197E7B','mm')
 elif idx==4:
  text(d,(32,90),'AIの出力を検証する',30)
  for j,(s,ok) in enumerate([('日付が正しいか',True),('数字が合っているか',False),('情報の根拠があるか',True)]):
   y=143+j*86;rect(d,(30,y,750,y+73),'#EDF5F6',12)
   rect(d,(53,y+17,95,y+59),'#3AB69D' if ok else '#E48C74',11)
   text(d,(74,y+37),'✓' if ok else '!',27,'#FFFFFF','mm')
   text(d,(118,y+37),s,27)
  text(d,(390,429),'人の確認は省略しない',24,'#197E7B','mm')
 elif idx==5:
  text(d,(32,90),'修正前と修正後を比較',30)
  for j,(label,items,bg,fg) in enumerate([('BEFORE',['結論が不明','情報が長い','表がない'],'#FBEFEB','#CB7C68'),('AFTER',['結論を先に','要点3つ','表で整理'],'#E8F8F3','#168B78')]):
   x=32+j*372;rect(d,(x,134,x+344,388),bg,15)
   text(d,(x+172,174),label,26,fg,'mm')
   for k,s in enumerate(items):text(d,(x+26,228+k*54),'• '+s,24)
  text(d,(390,427),'修正は1つずつ伝える',24,'#197E7B','mm')
 elif idx==6:
  text(d,(32,89),'使える指示は保存',30)
  for j,(s,tag) in enumerate([('日報の要約','毎日'),('メール下書き','営業'),('議事録の整理','会議')]):
   y=133+j*89;rect(d,(30,y,748,y+75),'#E8F3F5',12)
   text(d,(56,y+38),s,25)
   rect(d,(594,y+17,723,y+59),accent,10);text(d,(658,y+37),tag,20,'#FFFFFF','mm')
  text(d,(390,427),'次はゼロから始めない',25,'#197E7B','mm')
 else:
  text(d,(32,89),'時短の積み重ね（計算例）',30)
  d.line((55,365,726,365),fill='#BCD2D7',width=4)
  for j,h in enumerate([82,110,139,168,199]):
   x=83+j*130;rect(d,(x,357-h,x+80,357),'#A1DCD9' if j<4 else accent,11)
   text(d,(x+40,390),'月火水木金'[j],22,'#597984','mm')
  text(d,(390,427),'※ 実測ではありません',21,'#647F89','mm',False)
 return hook.apply_hook(im,accent) if idx==0 else im

def workspace_scene(i,genre='ai_work'):
 if genre not in COLORS:raise ValueError('unknown genre')
 accent=COLORS[genre]; rng=random.Random(82500+i)
 wall=gradient('#F6F2E9','#E3D9C9',920)
 desk=gradient('#B79A78','#7C624B',620)
 im=Image.new('RGB',(W,H),'#0D2130');im.paste(wall,(0,0));im.paste(desk,(0,770))
 d=ImageDraw.Draw(im)
 # Warm wood grain and desk surface. Deterministic and original.
 for j in range(250):
  y=rng.randint(785,1388);x=rng.randint(-150,1000)
  d.line((x,y,x+rng.randint(30,340),y+rng.randint(-2,2)),fill=(133+rng.randint(-9,9),105+rng.randint(-9,9),77+rng.randint(-9,9)),width=rng.randint(1,3))
 # Soft vignette + golden lighting.
 layer=Image.new('RGBA',(W,H),(0,0,0,0));ld=ImageDraw.Draw(layer)
 ld.ellipse((-310,-310,730,800),fill=(255,236,191,40))
 ld.ellipse((850,120,1510,880),fill=(255,255,255,25))
 im=Image.alpha_composite(im.convert('RGBA'),layer.filter(ImageFilter.GaussianBlur(115)))
 d=ImageDraw.Draw(im)
 # notebook with visible page details, at the edge of desk
 shadow(im,(14,912,258,1290),24,55,16)
 d=ImageDraw.Draw(im);d.polygon([(0,927),(251,903),(288,1266),(0,1295)],fill='#EDE7DA')
 for j in range(9):d.line((19,980+j*31,245,963+j*31),fill='#C4D0CE',width=3)
 d.line((48,932,92,1291),fill='#DB9888',width=3)
 # coffee cup, seen from above
 shadow(im,(870,864,1094,1087),29,63,99)
 d=ImageDraw.Draw(im)
 d.ellipse((875,867,1084,1076),fill='#F1EDE5',outline='#C3B5A2',width=10)
 d.ellipse((906,897,1054,1046),fill='#7E5843')
 d.ellipse((922,911,1043,1034),outline='#BE9376',width=6)
 # plant leaves to top right
 for j in range(7):
  cx=1033+rng.randint(-50,100);cy=650+rng.randint(-65,130)
  d.ellipse((cx-25,cy-68,cx+28,cy+32),fill=['#6B8563','#748E65','#53795D'][j%3])
 # laptop shadow and bottom body, slightly trapezoidal
 shadow(im,(91,470,1002,1274),42,93,25,(10,22))
 d=ImageDraw.Draw(im)
 d.polygon([(98,504),(959,504),(991,1106),(117,1106)],fill='#263B43')
 d.polygon([(115,517),(944,517),(972,1083),(132,1083)],fill='#111F2A')
 # Screen perspective; original fictional UI, never real screenshots
 screen=screen_content(i,accent)
 try:
  import cv2
  a=np.array(screen)
  src=np.float32([[0,0],[779,0],[779,459],[0,459]])
  dst=np.float32([[147,539],[914,539],[942,1060],[130,1060]])
  warped=cv2.warpPerspective(a,cv2.getPerspectiveTransform(src,dst),(W,H),flags=cv2.INTER_CUBIC)
  mask=cv2.warpPerspective(np.full((460,780),255,dtype=np.uint8),cv2.getPerspectiveTransform(src,dst),(W,H))
  im.paste(Image.fromarray(warped), (0,0), Image.fromarray(mask))
 except ImportError:
  im.paste(screen.resize((790,520)),(145,540))
 d=ImageDraw.Draw(im)
 d.ellipse((523,520,533,530),fill='#56727C')
 d.polygon([(111,1105),(992,1105),(1060,1232),(30,1232)],fill='#AEB8B7')
 d.polygon([(160,1118),(947,1118),(981,1189),(112,1189)],fill='#344A53')
 for row in range(3):
  for col in range(15):
   x=158+col*51+row*7;y=1127+row*19
   d.rounded_rectangle((x,y,x+43,y+14),radius=3,fill='#637980')
 d.polygon([(410,1194),(680,1194),(698,1220),(391,1220)],fill='#849797')
 d.line((34,1233,1054,1233),fill='#E0E6E4',width=6)
 # editorial top text: opaque soft card for consistent contrast
 shadow(im,(55,170,1024,454),35,40,35,(0,9))
 d=ImageDraw.Draw(im)
 rect(d,(55,170,1024,454),'#FCFAF4',30)
 rect(d,(82,194,328,249),'#193746',23)
 text(d,(205,221),'AI WORK / 08',25,'#FFFFFF','mm')
 text(d,(961,222),f'{i+1:02} / 08',26,'#54717C','rm')
 text(d,(85,326),TITLE[i][0],57,'#173645')
 text(d,(87,406),TITLE[i][1],30,'#58727D',bold=False)
 d.rectangle((83,450,83+int(918*(i+1)/8),458),fill=accent)
 # Shared viewer-facing lower-third is also used by GitHub Actions CI.
 im=rail.apply_action_rail(im,i,genre)
 return im.convert('RGB')

def slides(root:Path,genre='ai_work'):
 p=root/'source';p.mkdir(parents=True,exist_ok=True)
 for i in range(8):workspace_scene(i,genre).save(p/f'scene_{i+1:02}.png',optimize=True)
 timing={'cycle':826,'genre':genre,'sentences':[{'scene':i+1,'text':SPEECH[i],'seconds':sec} for i,sec in enumerate([3.355,3.085,3.025,3.285,3.265,3.36,2.97,3.495])],'voice_engine':'Open JTalk','voice_model':'nitech_jp_atr503_m001.htsvoice','rights_review_required':True,'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
 (p/'voice_timing.json').write_text(json.dumps(timing,ensure_ascii=False,indent=2),encoding='utf8')
 provenance={'cycle':826,'genre':genre,'external_images':False,'real_screenshots':False,
  'personal_data':False,'source':'original Pillow/numpy procedural desk + fictional laptop UI; hook and safe-zone layout; shared local/CI code',
  'font':'system Noto Sans CJK rasterized only','voice':'offline Open JTalk narration / rights review',
  'change_from_cycle825':'move captions/action inside conservative vertical safe area; add original before/after first-frame hook; use identical renderer code for local/CI',
  'posting_allowed':False}
 (p/'asset_provenance826.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2),encoding='utf8')

def ass_time(frame):
 t=frame/30;h=int(t//3600);m=int(t%3600//60);s=int(t%60);cs=int(round((t-int(t))*100))
 if cs==100:s+=1;cs=0
 return f'{h}:{m:02}:{s:02}.{cs:02}'

def make_ass(root:Path):
 """Three progressive emphasis states per scene, timed to video frame boundaries."""
 lines=['[Script Info]','ScriptType: v4.00+','PlayResX: 1080','PlayResY: 1920','WrapStyle: 2',
 '[V4+ Styles]','Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding',
 'Style: Caption,Noto Sans CJK JP,65,&H00FFFFFF,&H00FFFFFF,&H000A2638,&HAA000000,-1,0,0,0,100,100,0,0,1,5,1,5,65,65,0,1',
 '[Events]','Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text']
 start=0
 for i,parts in enumerate(PHRASES):
  n=FRAMES[i]
  for phase in range(3):
   lo=start+round(n*phase/3);hi=start+round(n*(phase+1)/3)
   colored=[]
   for j,p in enumerate(parts):
    col='&H006BEBD9&' if j==phase else '&H00FFFFFF&'
    colored.append(r'{\c'+col+'}'+p)
   # 3 rows, fits safe area; captions are not real forced word alignment.
   content=r'{\an5\pos(540,1540)\fad(90,0)}'+r'\N'.join(colored)
   lines.append(f'Dialogue: 0,{ass_time(lo)},{ass_time(hi)},Caption,,0,0,0,,{content}')
  start+=n
 p=root/'output'/'captions826.ass';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text('\n'.join(lines)+'\n',encoding='utf8');return p

def render(root:Path):
 """Frame-exact 775-frame still-image slideshow, burned ASS captions, inherited JP voice."""
 out=root/'output'/'cycle826_SAFEZONE_HOOK_JAPANESE_HUMAN_REVIEW.mp4'
 make_ass(root)
 concat=root/'output'/'frames826.txt'
 # use image2 input with -loop 1 for each scene; concat via ffmpeg filter to exact frames
 filter_parts=[];inputs=[]
 for i,n in enumerate(FRAMES):
  inputs.extend(['-i',str(root/'source'/f'scene_{i+1:02}.png')])
  direction = f'(iw-iw/zoom)*on/{n}' if i%2==0 else f'(iw-iw/zoom)*(1-on/{n})'
  filter_parts.append(f"[{i}:v]zoompan=z='min(1.0+on*0.00024,1.028)':x='{direction}':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
 filter_parts.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[vcat]')
 ass=root/'output'/'captions826.ass'
 filter_parts.append(f'[vcat]ass={ass}:fontsdir=/usr/share/fonts/opentype/noto[vout]')
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',*inputs,'-i',str(root/'source'/'voice.m4a'),
  '-filter_complex',';'.join(filter_parts),'-map','[vout]','-map','8:a:0',
  '-c:v','libx264','-preset','veryfast','-crf','23','-pix_fmt','yuv420p','-r','30',
  '-c:a','aac','-b:a','160k','-ar','48000','-af','apad',
  '-t',str(775/30),'-movflags','+faststart',str(out)]
 subprocess.run(cmd,check=True);return out

def verify(root:Path):
 p=root/'output'/'cycle826_SAFEZONE_HOOK_JAPANESE_HUMAN_REVIEW.mp4'
 j=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)]))
 v=next(x for x in j['streams'] if x['codec_type']=='video')
 a=next(x for x in j['streams'] if x['codec_type']=='audio')
 imgs=[Image.open(root/'source'/f'scene_{i:02}.png') for i in range(1,9)]
 region=[im.crop((130,540,940,1060)).resize((100,65)) for im in imgs]
 ass=(root/'output'/'captions826.ass').read_text(encoding='utf8')
 decode=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-map','0:v:0','-f','null','-'],capture_output=True)
 checks={
  'mp4_nonempty':p.stat().st_size>1000000,
  '1080x1920':(v['width'],v['height'])==(1080,1920),
  'h264_30fps':v['codec_name']=='h264' and v['r_frame_rate']=='30/1',
  '775_frames':int(v.get('nb_frames',0))==775,
  'aac_48khz':a['codec_name']=='aac' and a['sample_rate']=='48000',
  'audio_25s_plus':float(a.get('duration',j['format']['duration']))>=25.7,
  '24_caption_states':ass.count('Dialogue: 0,')==24,
  'eight_original_images':all(im.size==(1080,1920) for im in imgs) and all(ImageChops.difference(region[k],region[k+1]).getbbox() for k in range(7)),
  'eight_distinct_action_rails':all(ImageChops.difference(imgs[k].crop((80,1330,900,1420)),imgs[k+1].crop((80,1330,900,1420))).getbbox() for k in range(7)),
  'safe_zone_action_rail':all(im.crop((75,1320,890,1430)).getbbox() for im in imgs),
  'hook_has_before_after':ImageChops.difference(screen_content(0,COLORS['ai_work']).crop((25,147,366,377)),screen_content(0,COLORS['ai_work']).crop((414,147,755,377))).getbbox() is not None,
  'all_video_frames_decode':decode.returncode==0,
  'provenance_manifest':(root/'source'/'asset_provenance826.json').exists(),
  'viewer_first_action_rail':all('VOICE + CAPTIONS' not in x and 'HUMAN REVIEW' not in x for x in ACTION),
  'ten_genre_palette':len(COLORS)==10,
  'review_only':not any('PUBLISH_APPROVED' in x for x in (str(root),)),
 }
 report={'cycle':826,'previous_cycle':825,'change':'TikTok bottom safe-zone repositioning plus first-frame BEFORE/AFTER hook, same rendering source for local and CI',
  'genre':'ai_work','checks':checks,'passed':sum(bool(x) for x in checks.values()),'total':len(checks),
  'duration_seconds':float(j['format']['duration']),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
  'review_status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
  'manual_checks_remaining':['voice naturalness','word-level captions','mobile-device playback','voice license','reference-video comparison','employee approval','GitHub billing status'],
  'posting_allowed':False}
 (root/'output'/'qa826.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
 print(json.dumps(report,ensure_ascii=False,indent=2))
 if not all(checks.values()):raise SystemExit(1)
 return report

def contact(root:Path):
 thumbs=[]
 for i in range(1,9):
  im=Image.open(root/'source'/f'scene_{i:02}.png').convert('RGB').resize((270,480))
  thumbs.append(im)
 sheet=Image.new('RGB',(1080,1920))
 for i,im in enumerate(thumbs):sheet.paste(im,((i%4)*270,(i//4)*480))
 # use a 4 x 2 grid of portrait images (1080x960), no huge whitespace
 sheet=sheet.crop((0,0,1080,960))
 sheet.save(root/'output'/'contact_8scenes.jpg',quality=90)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--step',choices=['slides','render','verify','contact'],required=True);ap.add_argument('--genre',default='ai_work')
 args=ap.parse_args();{'slides':lambda:slides(args.root,args.genre),'render':lambda:render(args.root),'verify':lambda:verify(args.root),'contact':lambda:contact(args.root)}[args.step]()