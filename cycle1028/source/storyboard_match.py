#!/usr/bin/env python3
"""Cycle1028: review-only caption-to-visual storyboard alignment.

The inherited clip is PRIVATE and never committed. We replace only the
scene03 illustration (not its narration/captions) with a synthetic, clearly
labelled 'finished example' in two beats. No claim of speech/semantic QA.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES = {
 'ai_work':('完成形の見本','月別集計の完成イメージ','月','営業A','営業B'),
 'beauty':('完成形の見本','比較表の完成イメージ','項目','比較A','比較B'),
 'romance_psychology':('完成形の見本','整理表の完成イメージ','視点','観点A','観点B'),
 'money_saving':('完成形の見本','支出表の完成イメージ','月','費用A','費用B'),
 'sales_business':('完成形の見本','営業集計の完成イメージ','月','部門A','部門B'),
 'career':('完成形の見本','条件比較の完成イメージ','項目','条件A','条件B'),
 'health_lifestyle':('完成形の見本','習慣記録の完成イメージ','日','記録A','記録B'),
 'science_trivia':('完成形の見本','仮説比較の完成イメージ','項目','仮説A','仮説B'),
 'travel_food':('完成形の見本','候補比較の完成イメージ','項目','候補A','候補B'),
 'product_comparison_lifestyle':('完成形の見本','商品比較の完成イメージ','項目','商品A','商品B'),
}
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
START,MID,END=5.95,7.20,8.52

def cmd(args, binary=False):
 p=subprocess.run([str(v) for v in args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode: raise RuntimeError('command failed: '+ ' '.join(str(v) for v in args[:5])+'\n'+p.stderr.decode(errors='replace')[-3000:])
 return p.stdout if binary else p.stdout.decode()

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

def probe(path):return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def audio_hash(path):return hashlib.sha256(cmd(['ffmpeg','-v','error','-i',path,'-map','0:a:0','-c','copy','-f','adts','-'],True)).hexdigest()

def font(size,bold=False):
 f=FONT_BOLD if bold else FONT_REG
 if not Path(f).exists():raise RuntimeError('Noto CJK font missing')
 return ImageFont.truetype(f,size)

def panel(genre,beat):
 if genre not in GENRES:raise ValueError('unknown genre')
 title,sub,c1,c2,c3=GENRES[genre]
 S=2;W,H=920,1240
 # Draw 2x then downsample for clean smartphone typography.
 im=Image.new('RGBA',(W*S,H*S),(0,0,0,0));d=ImageDraw.Draw(im)
 def rect(box,fill,r=0,outline=None,width=1):
  coords=tuple(int(x*S) for x in box)
  d.rounded_rectangle(coords,radius=r*S,fill=fill,outline=outline,width=width*S)
 def txt(pos,s,size,fill,bold=False):d.text((pos[0]*S,pos[1]*S),s,font=font(size*S,bold),fill=fill,stroke_width=0)
 rect((0,0,W,H),(5,18,35,248),35,outline=(62,194,214,210),width=3)
 rect((25,25,895,155),(14,48,70,255),25)
 rect((48,51,62,115),(39,229,205,255),6)
 txt((83,44),title,52,'#ffffff',True)
 txt((84,119),'架空のサンプル・実操作映像ではありません',22,'#9cbac9')
 rect((48,177,872,257),(13,38,59,255),17)
 txt((76,192),sub,39,'#e9f9ff',True)
 rect((750,190,847,241),(27,97,114,255),16)
 txt((767,195),f'{beat}/2',30,'#b8fff0',True)
 # spreadsheet output card
 rect((48,292,872,874),(244,250,251,255),22)
 rect((48,292,872,374),(22,94,101,255),22)
 txt((79,308),'完成イメージ  /  SAMPLE',34,'#ffffff',True)
 cols=[(75,278,c1),(286,503,c2),(510,725,c3),(733,844,'確認')]
 for x0,x1,label in cols:
  rect((x0,400,x1,468),(214,237,240,255),8)
  txt((x0+16,410),label,31,'#123a4a',True)
 rows=[('4月','12','8','✓'),('5月','16','9','✓'),('6月','18','12','✓')]
 if beat==2:rows.append(('合計','46','29','✓'))
 for i,row in enumerate(rows):
  y=487+i*89
  bg=(236,248,248,255) if i%2==0 else (255,255,255,255)
  if i==3:bg=(194,245,230,255)
  rect((75,y,845,y+76),bg,6)
  for j,((x0,x1,_),value) in enumerate(zip(cols,row)):
   txt((x0+15,y+16),value,34,'#174052',bold=(i==3 or j==0))
 # show placeholder until completion, then proof
 rect((48,910,872,1120),(14,43,62,255),20)
 if beat==1:
  txt((82,939),'01  必要な列と見出しを決める',40,'#ffffff',True)
  txt((82,1013),'出力の形を先に示す',33,'#9ce9e0')
 else:
  txt((82,939),'02  合計・確認欄まで見せる',40,'#ffffff',True)
  txt((82,1013),'AIに「この形で」と伝える',33,'#9ce9e0')
 rect((50,1162,870,1183),(22,58,74,255),10)
 rect((50,1162,460 if beat==1 else 870,1183),(36,223,194,255),10)
 inner=im.resize((W,H),Image.Resampling.LANCZOS)
 backdrop=Image.new('RGBA',(1080,H),(4,16,29,255))
 backdrop.alpha_composite(inner,(80,0))
 return backdrop

def filter_graph(start,mid,end):
 if not 0<=start<mid<end:raise ValueError('invalid scene window')
 # Local alpha fades avoid a flash at shot boundaries. Subtitle region y>=1490 is never touched.
 d=min(0.14,(mid-start)/6,(end-mid)/6)
 f1=f'[1:v]format=rgba,fade=t=in:st={start:.3f}:d={d:.3f}:alpha=1,fade=t=out:st={mid-d:.3f}:d={d:.3f}:alpha=1[p1]'
 f2=f'[2:v]format=rgba,fade=t=in:st={mid:.3f}:d={d:.3f}:alpha=1,fade=t=out:st={end-d:.3f}:d={d:.3f}:alpha=1[p2]'
 return ';'.join([f1,f2,f"[0:v][p1]overlay=x=0:y=100:enable='between(t,{start:.3f},{mid:.3f})':eof_action=pass[v1]",f"[v1][p2]overlay=x=0:y=100:enable='between(t,{mid:.3f},{end:.3f})':eof_action=pass[vout]"])

def render(source,output,report,genre,expected_source_sha,review_only=False,synthetic_ci=False):
 if not review_only:raise ValueError('review gate required')
 if genre not in GENRES:raise ValueError('unknown genre')
 source,output,report=map(lambda p:Path(p).resolve(),(source,output,report))
 if not source.is_file() or source==output or output.exists() or report.exists():raise ValueError('source missing or output exists')
 if len(expected_source_sha)!=64 or sha(source)!=expected_source_sha:raise ValueError('source SHA mismatch')
 p=probe(source);v=[s for s in p['streams'] if s['codec_type']=='video'];a=[s for s in p['streams'] if s['codec_type']=='audio']
 if len(p['streams'])!=2 or len(v)!=1 or len(a)!=1:raise ValueError('one A/V stream each required')
 if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],a[0]['codec_name'],int(a[0]['sample_rate']))!=('h264',1080,1920,'30/1','aac',48000):raise ValueError('invalid A/V format')
 start,mid,end=(0.12,0.96,1.84) if synthetic_ci else (START,MID,END)
 if float(p['format']['duration'])<end-0.015:raise ValueError('duration too short')
 output.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
 with tempfile.TemporaryDirectory() as tmp:
  files=[]
  for i in (1,2):
   f=Path(tmp)/f'panel{i}.png';panel(genre,i).save(f);files.append(f)
  cmd(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',source,
       '-loop','1','-framerate','30','-i',files[0],'-loop','1','-framerate','30','-i',files[1],
       '-filter_complex',filter_graph(start,mid,end),'-map','[vout]','-map','0:a:0',
       '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-threads','2',
       '-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart','-t',str(float(p['format']['duration'])),output])
 cmd(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
 q=probe(output);vv=next(s for s in q['streams'] if s['codec_type']=='video')
 unchanged=audio_hash(source)==audio_hash(output)
 if not unchanged:raise RuntimeError('audio bitstream changed')
 if (vv['width'],vv['height'],vv['r_frame_rate'])!=(1080,1920,'30/1'):raise RuntimeError('format changed')
 result={'source_sha256':sha(source),'output_sha256':sha(output),'genre':genre,'duration_seconds':float(q['format']['duration']),
         'frames':int(vv.get('nb_frames',0)),'video':'H.264 1080x1920 30fps','audio':'AAC 48kHz jpn-tagged',
         'audio_bitstream_unchanged':True,'full_av_decode':'PASS','change':'scene03 narration-aligned finished spreadsheet example, two progressive beats',
         'change_window_seconds':[start,end],'protected_subtitle_y_min':1490,'new_overlay_y_range':[100,1340],
         'fictional_sample':True,'independent_japanese_asr':'NOT_PERFORMED','caption_semantic_sync':'NOT_VERIFIED',
         'source_rights':'NOT_VERIFIED','employee_approval':'NOT_APPROVED','publication':'NOT_APPROVED'}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('source','output','report','expected-source-sha'):p.add_argument('--'+name,required=True)
 p.add_argument('--genre',choices=sorted(GENRES),default='ai_work');p.add_argument('--review-only',action='store_true');p.add_argument('--synthetic-ci',action='store_true')
 a=p.parse_args();print(json.dumps(render(a.source,a.output,a.report,a.genre,a.expected_source_sha,a.review_only,a.synthetic_ci),ensure_ascii=False))
