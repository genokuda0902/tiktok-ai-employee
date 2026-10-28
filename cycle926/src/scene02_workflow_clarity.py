#!/usr/bin/env python3
"""cycle926 — review-only fictional task workflow visual in scene 02.

Original editorial artwork. Existing user-session video and Japanese audio remain
local/private. Never upload inherited media or automatically post. This is NOT
an authentic app recording, original v33 recreation, or publication approval.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
WIDTH, HEIGHT, FPS = 1080, 1920, 30
CAPTION_SAFE_Y = 1460
SCENE_START, SCENE_END = 87, 174  # [2.900s, 5.800s)
STAGES = ((87,116),(116,145),(145,174))
GENRES = {
 'ai_work': ('月次の売上集計',('数字を入力','合計を確認','報告にまとめる'),'#3AE2D1'),
 'finance': ('支出メモの整理',('支出を記録','分類する','見直す'),'#85C9FF'),
 'health': ('生活習慣の記録',('記録する','傾向を確認','相談の準備'),'#8EE6B6'),
 'travel': ('旅行の準備',('行き先を決める','持ち物を整理','予定を確認'),'#A1BAFF'),
 'beauty': ('朝のケア記録',('使った物を記録','順番を整理','振り返る'),'#F0B2D4'),
 'cooking': ('献立の計画',('食材を確認','献立を選ぶ','買い物を整理'),'#FFC28C'),
 'education': ('復習メモの整理',('要点を書く','問題を選ぶ','答えを確認'),'#C8B8FF'),
 'career': ('面談準備の整理',('論点を整理','質問を考える','確認する'),'#FFD88B'),
 'lifestyle': ('家事の段取り',('作業を洗い出す','順番を決める','完了を確認'),'#F4B8C4'),
 'technology': ('端末設定の確認',('設定を調べる','手順を整理','動作を確認'),'#98E5E9'),
}
FONT_BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_REG = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'

def stage_for_frame(frame):
 if not SCENE_START <= frame < SCENE_END: raise ValueError('outside scene 02')
 return 0 if frame < STAGES[0][1] else (1 if frame < STAGES[1][1] else 2)

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()

def validate():
 assert len(GENRES)==10
 assert STAGES[0][0]==SCENE_START and STAGES[-1][1]==SCENE_END
 assert all(STAGES[i][1]==STAGES[i+1][0] for i in range(2))
 assert CAPTION_SAFE_Y < HEIGHT
 for topic,steps,accent in GENRES.values():
  assert topic and len(steps)==3 and all(steps)
  assert accent.startswith('#') and len(accent)==7
 return True

def render_stage(stage, genre='ai_work'):
 from PIL import Image,ImageDraw,ImageFont,ImageFilter
 if genre not in GENRES: raise ValueError('unknown genre')
 if stage not in (0,1,2): raise ValueError('unknown stage')
 topic,steps,accent=GENRES[genre]
 c=tuple(bytes.fromhex(accent[1:]))
 im=Image.new('RGB',(WIDTH,CAPTION_SAFE_Y),(5,16,31));d=ImageDraw.Draw(im)
 for y in range(CAPTION_SAFE_Y):
  # Subtle deep blue gradient, no external images.
  d.line((0,y,WIDTH,y),fill=(5+int(y/CAPTION_SAFE_Y*6),16+int(y/CAPTION_SAFE_Y*10),31+int(y/CAPTION_SAFE_Y*15)))
 def font(n,bold=False):return ImageFont.truetype(FONT_BOLD if bold else FONT_REG,n)
 def txt(pos,s,size,color,bold=False):d.text(pos,s,font=font(size,bold),fill=color,stroke_width=0)
 def rr(box,rad,fill,outline=None,width=1):d.rounded_rectangle(box,radius=rad,fill=fill,outline=outline,width=width)
 # Safe top navigation.
 txt((72,66),'AI WORK / 08',30,'#C0D9EB',True)
 rr((758,63,1000,112),18,'#14324A','#27536C',2)
 txt((790,71),'02 / 08',28,'#E5F6FF',True)
 rr((70,150,1010,288),32,'#0E3147','#35718A',2)
 txt((104,166),'STEP 01 / 発見',26,accent,True)
 txt((104,208),'繰り返す作業を1つ選ぶ',49,'#FFFFFF',True)
 txt((76,320),'架空の作業例  /  操作イメージ',25,'#91B6C8')
 # Main card.
 rr((70,382,1010,1338),42,'#112B40','#335A70',3)
 rr((105,425,975,559),26,'#0B4257','#32677D',2)
 txt((136,444),'毎月の繰り返し作業',26,'#9ADDE3')
 txt((136,482),topic,47,'#FFFFFF',True)
 # timeline cards: clear consistent typography and spacing.
 for i,step in enumerate(steps):
  top=601+i*188
  active=i==stage
  fill='#123C4D' if active else '#173043'
  outline=accent if active else '#36556A'
  rr((112,top,968,top+155),24,fill,outline,5 if active else 2)
  rr((142,top+39,218,top+115),22,accent if active else '#29485C')
  txt((163,top+51),str(i+1),40,'#072534' if active else '#BBD7E2',True)
  txt((254,top+43),step,43,'#FFFFFF' if active else '#B6D0DD',True)
  if active:
   rr((845,top+53,941,top+104),16,'#255A62')
   txt((857,top+60),'確認',25,'#D8FFFF',True)
 # bottom one-line interpretation; no fabricated metrics.
 rr((114,1203,966,1296),20,'#082337')
 msg=['最初は「何を繰り返すか」を決める','工程を分けると、改善点が見える','小さな作業から改善を始める'][stage]
 txt((139,1223),msg,31,'#D4F6F3',True)
 # Mark review-only within picture. Caption/footer in source is not replaced.
 txt((78,1372),'FICTIONAL DEMO  •  HUMAN REVIEW ONLY',21,'#7B9AAA')
 return im

def ffmpeg_render(source,output,overlays):
 # PNGs are full-width but only top 1460px, so inherited Japanese caption
 # pixels at y>=1460 remain untouched prior to encoding.
 args=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
 for p in overlays: args += ['-loop','1','-framerate','30','-i',str(p)]
 filters=[];v='0:v'
 for i,(start,end) in enumerate(STAGES):
  out=f'v{i+1}'
  filters.append(f'[{v}][{i+1}:v]overlay=x=0:y=0:enable=between(n\\,{start}\\,{end-1}):shortest=1:format=auto[{out}]')
  v=out
 args += ['-filter_complex',';'.join(filters),'-map',f'[{v}]','-map','0:a:0',
          '-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p',
          '-r','30','-frames:v','691','-c:a','copy','-movflags','+faststart',str(output)]
 return subprocess.run(args,capture_output=True,text=True)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--genre',choices=GENRES,default='ai_work');ap.add_argument('--workdir',type=Path,required=True)
 a=ap.parse_args();validate();a.workdir.mkdir(parents=True,exist_ok=True);a.output.parent.mkdir(parents=True,exist_ok=True)
 images=[]
 for i in range(3):
  p=a.workdir/f'scene02_stage{i+1}.png';render_stage(i,a.genre).save(p);images.append(p)
 proc=ffmpeg_render(a.source,a.output,images)
 (a.workdir/'ffmpeg.log').write_text(proc.stderr,encoding='utf-8')
 if proc.returncode:raise RuntimeError(f'ffmpeg failed {proc.returncode}: {proc.stderr[-2000:]}')
 report={'status':POLICY,'base_sha256':sha256(a.source),'output_sha256':sha256(a.output),'genre':a.genre,'modified_frames':[SCENE_START,SCENE_END-1], 'reference':'user 16-panel storyboard (not original v33 video)', 'audio':'inherited; semantic transcription not verified', 'upload_public':False}
 (a.workdir/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
