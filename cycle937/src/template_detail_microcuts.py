#!/usr/bin/env python3
"""cycle937: two template detail shots plus an earlier scene08 handoff.

All private media stay local. This is NOT real ChatGPT/Excel capture, nor v33.
A supplied approved template frame is mandatory for any genre; it is never committed.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WIDTH, HEIGHT, FPS, TOTAL_FRAMES = 1080, 1920, 30, 691
SCENE_START, SCENE_END = 522, 609  # scene07 17.4..20.3 seconds
OVERLAY_START, OVERLAY_END = 549, 609  # 19f+19f template shots, 22f early outro
SAFE_Y = 1450  # subtitle content starts below y=1490
POLICY = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
GENRES = {
 'ai_work': ('条件を残す', '出力形式まで残す'),
 'finance': ('記録の範囲を残す', '集計形式まで残す'),
 'health': ('確認条件を残す', '確認項目まで残す'),
 'travel': ('日程と条件を残す', '持ち物形式まで残す'),
 'beauty': ('使用条件を残す', '手順の形式まで残す'),
 'cooking': ('食材の条件を残す', '手順の形式まで残す'),
 'education': ('学習範囲を残す', '確認問題まで残す'),
 'career': ('事実の条件を残す', '下書き形式まで残す'),
 'lifestyle': ('使える時間を残す', '作業順まで残す'),
 'technology': ('機器の条件を残す', '確認手順まで残す'),
}
# These are coordinates in an inherited 1080x1920 fictional template frame.
# For another genre, the supplied frame MUST have the same three-row layout.
CROPS = ((90, 678, 975, 844), (90, 862, 975, 1033))


def digest(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''):h.update(c)
 return h.hexdigest()


def validate(genre, frame=None):
 if genre not in GENRES or len(GENRES)!=10: raise ValueError('unsupported genre')
 if SCENE_END-SCENE_START!=87 or OVERLAY_END-OVERLAY_START!=60:raise RuntimeError('frame geometry mismatch')
 if SAFE_Y>1450 or 'PUBLICATION_NOT_APPROVED' not in POLICY:raise RuntimeError('publication or caption guard missing')
 if not Path(FONT).exists() or not Path(BOLD).exists():raise FileNotFoundError('free Japanese font missing')
 if frame is not None and frame.size!=(WIDTH,HEIGHT):raise ValueError('approved frame must be 1080x1920')


def beat(local_frame):
 if not 0<=local_frame<60:raise ValueError('frame outside editorial sequence')
 return 0 if local_frame<19 else 1 if local_frame<38 else 2


def _font(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)


def make_overlay(local_frame, frame, genre='ai_work', outro_frame=None):
 validate(genre,frame)
 stage=beat(local_frame);within=local_frame%19
 if stage==2:
  if outro_frame is None or outro_frame.size!=(WIDTH,HEIGHT):raise ValueError('approved outro frame required')
  # Subtitle starts scene08 at source frame 587, before its picture changes at 609.
  # Show the inherited review-only outro early; do not manufacture a success state.
  return outro_frame.crop((0,0,WIDTH,SAFE_Y)).convert('RGBA')
 # Original source frame is a still: no invented GUI action or changed source values.
 # An opaque darkened background prevents old text from ghosting under the close-up.
 bg=frame.crop((0,0,WIDTH,SAFE_Y)).filter(ImageFilter.GaussianBlur(25)).convert('RGBA')
 tint=Image.new('RGBA',bg.size,(5,19,34,224));bg=Image.alpha_composite(bg,tint)
 d=ImageDraw.Draw(bg)
 d.rounded_rectangle((34,132,1046,1395),radius=45,fill=(8,28,45,250),outline=(61,130,151,255),width=3)
 d.text((77,183),'保存用テンプレート / 拡大表示',font=_font(48,True),fill='#F5FBFF')
 d.text((78,267),'架空の画面例・実際の保存操作ではありません',font=_font(29),fill='#C5E0E9')
 d.rounded_rectangle((72,344,1008,438),radius=20,fill=(12,87,100,255))
 d.text((110,360),GENRES[genre][stage],font=_font(48,True),fill='#F5FFFF')
 # Show the actual inherited fictional input row, not a retyped claim.
 crop=frame.crop(CROPS[stage]).convert('RGB')
 scale=1.0+0.018*(within/18.0)
 outw=int(882*scale);outh=int(outw*crop.height/crop.width)
 crop=crop.resize((outw,outh),Image.Resampling.LANCZOS)
 card=Image.new('RGBA',(928,422),(239,249,252,255))
 cd=ImageDraw.Draw(card)
 cd.rounded_rectangle((15,16,912,406),radius=22,outline=(48,169,174,255),width=4)
 cd.text((40,32),'架空の入力例 / 拡大',font=_font(32,True),fill='#0A3B50')
 x=(928-outw)//2;y=132+(215-outh)//2
 card.paste(crop,(x,y))
 cd=ImageDraw.Draw(card)
 cd.text((40,367),'入力内容は元データと照合する',font=_font(26),fill='#376376')
 mask=Image.new('L',card.size,0);md=ImageDraw.Draw(mask)
 md.rounded_rectangle((0,0,927,421),radius=30,fill=255)
 card.putalpha(mask)
 shadow=Image.new('RGBA',(958,455),(0,0,0,0))
 sd=ImageDraw.Draw(shadow);sd.rounded_rectangle((15,16,942,440),radius=34,fill=(0,0,0,125))
 shadow=shadow.filter(ImageFilter.GaussianBlur(13))
 bg.alpha_composite(shadow,(61,531))
 bg.alpha_composite(card,(76,547))
 d=ImageDraw.Draw(bg)
 d.rounded_rectangle((79,1062,1000,1166),radius=20,fill=(11,72,86,255))
 d.text((110,1086),'実務では、内容を確認してから保存',font=_font(37,True),fill='#F4FFFF')
 for i in range(2):
  d.rounded_rectangle((430+i*116,1218,525+i*116,1233),radius=8,
                      fill='#5FE6DE' if i==stage else '#315467')
 d.text((84,1331),'※ 未承認・社員確認後に手動投稿',font=_font(23),fill='#BDD5DF')
 return bg


def run(cmd,log):
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
 Path(log).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
 if p.returncode:raise RuntimeError(f'command failed ({p.returncode}): {p.stderr[-1400:]}')


def extract_frame(source,output,at=18.1):
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-ss',str(at),'-i',str(source),'-frames:v','1',str(output)],str(output)+'.log')
 return Image.open(output).convert('RGB')


def render(source,output,workdir,genre='ai_work',expected_source_sha=None):
 validate(genre);source=Path(source);output=Path(output);workdir=Path(workdir)
 if not source.is_file():raise FileNotFoundError(source)
 source_sha=digest(source)
 if expected_source_sha is None or expected_source_sha!=source_sha:raise RuntimeError('FAIL_CLOSED_SOURCE_SHA_REQUIRED_OR_MISMATCH')
 workdir.mkdir(parents=True,exist_ok=True);output.parent.mkdir(parents=True,exist_ok=True)
 still=workdir/'private_template_still.png';frame=extract_frame(source,still)
 outro=extract_frame(source,workdir/'private_outro_still.png',at=20.8)
 validate(genre,frame)
 overlays=workdir/'private_overlays';overlays.mkdir(exist_ok=True)
 for n in range(60):make_overlay(n,frame,genre,outro).save(overlays/f'{n:03d}.png',compress_level=1)
 graph=f"[1:v]setpts=PTS+{OVERLAY_START}/30/TB[ov];[0:v][ov]overlay=0:0:eof_action=pass:enable='between(n,{OVERLAY_START},{OVERLAY_END-1})'[v]"
 run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-framerate','30',
      '-start_number','0','-i',str(overlays/'%03d.png'),'-filter_complex',graph,
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
      '-pix_fmt','yuv420p','-r','30','-frames:v',str(TOTAL_FRAMES),'-c:a','copy',
      '-movflags','+faststart',str(output)],workdir/'encode.log')
 report={'policy':POLICY,'genre':genre,'source_sha256':source_sha,'output_sha256':digest(output),
         'changed_frame_range':[OVERLAY_START,OVERLAY_END-1],
         'new_editorial_cuts':3,'earlier_scene08_handoff_frame':587,'source_visual_captured_from_inherited_private_video':True,
         'real_chatgpt_or_excel_capture':False,'new_narration':False,
         'independent_asr':'NOT_VERIFIED','employee_approval':'NOT_APPROVED',
         'publication_allowed':False}
 (workdir/'render_result.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
 return report

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--source',required=True);a.add_argument('--output',required=True)
 a.add_argument('--workdir',required=True);a.add_argument('--genre',choices=GENRES,default='ai_work');a.add_argument('--expected-source-sha',required=True)
 x=a.parse_args();print(json.dumps(render(x.source,x.output,x.workdir,x.genre,x.expected_source_sha),ensure_ascii=False))
