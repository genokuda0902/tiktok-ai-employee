#!/usr/bin/env python3
"""Cycle1030: review-only correction focus over existing Calc evidence.

Transparent focus rings reveal the wrong draft 45 and verified 46 without
covering the inherited Calc screen. No source media is published or committed.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

GENRES = {
 'ai_work':('数字の誤りを見つける','集計表','元データ 12 + 16 + 18','45','46'),
 'beauty':('結果をそのまま使わない','比較表','条件と根拠を再確認','確認前','確認後'),
 'romance_psychology':('根拠を確認する','整理表','断定表現を見直す','確認前','確認後'),
 'money_saving':('数字を再計算する','支出表','合計と単位を確認','確認前','確認後'),
 'sales_business':('集計を再確認する','営業表','集計条件と合計を確認','確認前','確認後'),
 'career':('条件を照合する','比較表','応募条件と出典を確認','確認前','確認後'),
 'health_lifestyle':('情報の出典を確認','習慣表','個人差と条件を確認','確認前','確認後'),
 'science_trivia':('根拠を確認する','比較表','元の資料と照合','確認前','確認後'),
 'travel_food':('条件を再確認する','候補表','日付と営業時間を確認','確認前','確認後'),
 'product_comparison_lifestyle':('仕様を照合する','商品表','価格と型番を確認','確認前','確認後'),
}
FONT_REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
START,MID,END=14.18,15.46,16.76

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
 """Transparent focus overlays; preserve the real Calc screen below."""
 if genre not in GENRES:raise ValueError('unknown genre')
 W,H,S=1080,1920,2
 im=Image.new('RGBA',(W*S,H*S),(0,0,0,0));d=ImageDraw.Draw(im)
 def rect(box,fill=None,r=0,outline=None,width=1):
  d.rounded_rectangle(tuple(int(x*S) for x in box),radius=r*S,fill=fill,outline=outline,width=width*S)
 def txt(pos,s,size,fill,bold=False):
  d.text((int(pos[0]*S),int(pos[1]*S)),s,font=font(size*S,bold),fill=fill)
 if beat==1:
  rect((305,541,620,704),r=27,outline=(255,112,137,242),width=8)
  rect((637,570,848,633),(80,25,44,234),15,outline=(255,138,153,230),width=2)
  txt((663,579),'要確認',34,'#fff0f0',True)
 else:
  rect((106,668,846,740),r=13,outline=(71,241,189,235),width=7)
  rect((493,674,578,732),r=11,outline=(43,205,160,240),width=5)
  rect((627,751,848,810),(13,91,75,234),14,outline=(81,248,197,225),width=2)
  txt((651,758),'検算 OK',29,'#dffff1',True)
 return im.resize((W,H),Image.Resampling.LANCZOS)

def filter_graph(start,mid,end):
 if not 0<=start<mid<end:raise ValueError('invalid scene window')
 # Local alpha fades avoid a flash at shot boundaries. Subtitle region y>=1490 is never touched.
 d=min(0.14,(mid-start)/6,(end-mid)/6)
 f1=f'[1:v]format=rgba,fade=t=in:st={start:.3f}:d={d:.3f}:alpha=1,fade=t=out:st={mid-d:.3f}:d={d:.3f}:alpha=1[p1]'
 f2=f'[2:v]format=rgba,fade=t=in:st={mid:.3f}:d={d:.3f}:alpha=1,fade=t=out:st={end-d:.3f}:d={d:.3f}:alpha=1[p2]'
 return ';'.join([f1,f2,f"[0:v][p1]overlay=x=0:y=0:enable='between(t,{start:.3f},{mid:.3f})':eof_action=pass[v1]",f"[v1][p2]overlay=x=0:y=0:enable='between(t,{mid:.3f},{end:.3f})':eof_action=pass[vout]"])

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
         'audio_bitstream_unchanged':True,'full_av_decode':'PASS','change':'scene06 transparent focus rings: incorrect 45 then actual Calc SUM 46; original UI preserved',
         'change_window_seconds':[start,end],'protected_subtitle_y_min':1490,'new_overlay_y_range':[541,810],
         'fictional_sample':True,'correction_example':('45→46' if genre=='ai_work' else 'generic review'),'independent_japanese_asr':'NOT_PERFORMED','caption_semantic_sync':'NOT_VERIFIED',
         'source_rights':'NOT_VERIFIED','employee_approval':'NOT_APPROVED','publication':'NOT_APPROVED'}
 report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
 return result

if __name__=='__main__':
 p=argparse.ArgumentParser()
 for name in ('source','output','report','expected-source-sha'):p.add_argument('--'+name,required=True)
 p.add_argument('--genre',choices=sorted(GENRES),default='ai_work');p.add_argument('--review-only',action='store_true');p.add_argument('--synthetic-ci',action='store_true')
 a=p.parse_args();print(json.dumps(render(a.source,a.output,a.report,a.genre,a.expected_source_sha,a.review_only,a.synthetic_ci),ensure_ascii=False))
