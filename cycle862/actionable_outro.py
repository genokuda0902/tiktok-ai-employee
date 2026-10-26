"""cycle862: review-only actionable outro; 10-genre visual template, no posting.

New 2-second editorial CTA is drawn locally. Inset images are derived only from the
private, rights-unapproved source MP4 and must never be committed or published.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FPS=30
TOTAL=691
START=631
N=60
ROI=(40,350,1000,1090)  # y ends at 1440; subtitles start below 1490
GENRES=('ai_work','sales_business','beauty','romance','saving','career','wellness','science','travel_food','product_comparison_lifestyle')
ACCENTS=dict(zip(GENRES,('#35D7EA','#4BE5AC','#FF90BD','#FF83A9','#56E7B3','#86A6FF','#63E6BD','#68D6FF','#F5BA79','#A9B6FF')))
POLICY={'review_only':True,'publication_approved':False,'automatic_posting':False,'external_upload':False,'source_rights_reviewed':False,'contains_personal_data':False,'fictional_workflow_example':True}
COPY={
'ai_work':('この手順、保存して試す',('繰り返し作業を選ぶ','指示を具体的に書く','出力を自分で確認')),
'sales_business':('次の商談で試す',('相手の課題を聞く','提案を一つに絞る','次の約束を決める')),
'beauty':('明日のケアで試す',('肌の状態を確認','使う量を見直す','変化を記録する')),
'romance':('次の会話で試す',('相手の話を聞く','気持ちを言葉にする','反応を確かめる')),
'saving':('今月の支出を見直す',('固定費を確認','一つだけ減らす','来月また比較する')),
'career':('明日の仕事で試す',('優先順位を決める','小さく実行する','結果を振り返る')),
'wellness':('今日の習慣を見直す',('無理なく始める','続けた日を記録','体調を確認する')),
'science':('一つ実験してみる',('仮説を立てる','条件を揃える','結果を記録する')),
 'travel_food':('次のお出かけに保存',('候補を調べる','営業時間を確認','無理なく計画する')),
 'product_comparison_lifestyle':('購入前に比較する',('必要条件を決める','候補を比べる','仕様を再確認する'))}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def font(n):
 return ImageFont.truetype(FONT,n) if Path(FONT).exists() else ImageFont.load_default()

def smooth(t):
 t=max(0.,min(1.,float(t)));return t*t*(3-2*t)

def validate(source,out,manifest,genre):
 source,out=Path(source),Path(out)
 if genre not in GENRES:raise ValueError('unsupported genre')
 if not source.is_file():raise FileNotFoundError(source)
 if out.exists() or source.resolve()==out.resolve():raise ValueError('refuse overwrite')
 if manifest!={**POLICY,'source_sha256':sha(source)}:raise ValueError('source hash / review policy mismatch')
 return source,out

def probe(path):
 return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(path)],text=True))

def check_streams(path):
 s=probe(path)['streams'];v=next((x for x in s if x['codec_type']=='video'),None);a=next((x for x in s if x['codec_type']=='audio'),None)
 if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v.get('nb_frames') or 0),a['codec_name'],a['sample_rate'])!=('h264',1080,1920,'30/1',691,'aac','48000'):raise ValueError('unexpected streams')

def source_shots(source,folder):
 shots=[]
 for index,frame in enumerate((365,526)):
  p=Path(folder)/f'source_{index}.png'
  subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-ss',f'{frame/FPS:.6f}','-i',str(source),'-frames:v','1','-y',str(p)],check=True,timeout=30)
  with Image.open(p) as im:
   shots.append(im.convert('RGB').crop((75,535,980,1200)).resize((414,290),Image.Resampling.LANCZOS))
 return shots

def draw(frame,shots,genre='ai_work'):
 if genre not in GENRES or not 0<=frame<N:raise ValueError('invalid genre/frame')
 if len(shots)!=2:raise ValueError('two source images required')
 W,H=ROI[2:];accent=ACCENTS[genre];title,steps=COPY[genre]
 im=Image.new('RGB',(W,H));d=ImageDraw.Draw(im)
 for y in range(H):
  t=y/H;d.line((0,y,W,y),fill=(round(8+11*t),round(20+17*t),round(34+19*t)))
 glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow);g.ellipse((480,-240,1170,510),fill=(30,180,240,78));glow=glow.filter(ImageFilter.GaussianBlur(85))
 im=Image.alpha_composite(im.convert('RGBA'),glow);d=ImageDraw.Draw(im)
 d.rounded_rectangle((24,22,976,1060),radius=42,outline=(51,104,129),width=3)
 d.rounded_rectangle((57,55,410,115),radius=22,fill=(10,59,78));d.text((80,63),'保存用チェックリスト',font=font(32),fill=accent)
 d.text((57,143),title,font=font(51),fill='#FFFFFF')
 # Original (unapproved) real-UI screenshots; no synthetic claims.
 for k,shot in enumerate(shots):
  x=57+k*460;y=250
  mask=Image.new('L',shot.size,0);ImageDraw.Draw(mask).rounded_rectangle((0,0,shot.width-1,shot.height-1),radius=20,fill=255)
  im.paste(shot,(x,y),mask);d=ImageDraw.Draw(im)
  d.rounded_rectangle((x,y,x+414,y+290),radius=20,outline=accent,width=3)
  d.rounded_rectangle((x+10,y+10,x+185,y+49),radius=12,fill=(10,45,62))
  d.text((x+22,y+14),'実操作 / 架空' if k==0 else '編集 / 架空',font=font(20),fill='#FFFFFF')
 # Three staggered, genuine text reveals, not a fake interaction.
 for k,step in enumerate(steps):
  y=579+103*k;visible=smooth((frame-(6+k*12))/10)
  if visible<=0:continue
  right=57+int(886*visible)
  d.rounded_rectangle((57,y,right,y+82),radius=21,fill=(16,62,79),outline=(58,137,154),width=2)
  if visible>.80:
   d.ellipse((81,y+21,123,y+63),fill=accent)
   d.text((91,y+22),str(k+1),font=font(26),fill='#09212E')
   d.text((154,y+16),step,font=font(39),fill='#FFFFFF')
 # Final CTA button pulses, while preserving the original subtitle card below ROI.
 v=smooth((frame-38)/12);pulse=1+0.025*smooth((frame-49)/10)
 if v>0:
  mid=500;hw=int(405*v*pulse)
  d.rounded_rectangle((mid-hw,916,mid+hw,1021),radius=34,fill=accent)
  if v>.88:d.text((330,936),'保存して実践  ✓',font=font(46),fill='#08212F')
 return im.convert('RGB')

def render(source,out,manifest,genre='ai_work'):
 source,out=validate(source,out,manifest,genre);check_streams(source)
 with tempfile.TemporaryDirectory(prefix='cycle862_') as tmp:
  shots=source_shots(source,tmp);frames=Path(tmp)/'frames';frames.mkdir()
  for i in range(N):draw(i,shots,genre).save(frames/f'out_{i:03d}.png')
  filt=(f'[1:v]format=yuva420p,setpts=PTS-STARTPTS+{START}/(30*TB)[new];'
        f'[0:v][new]overlay=x={ROI[0]}:y={ROI[1]}:enable=\'between(n,{START},{START+N-1})\':eof_action=pass:repeatlast=0:format=auto[v]')
  cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),'-framerate','30','-start_number','0','-i',str(frames/'out_%03d.png'),'-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20','-pix_fmt','yuv420p','-r','30','-frames:v',str(TOTAL),'-c:a','copy','-movflags','+faststart',str(out)]
  subprocess.run(cmd,check=True,timeout=220)
 check_streams(out)
 return {'input_sha256':sha(source),'output_sha256':sha(out),'frame_range':[START,START+N-1],'changed_frames':N,'genre':genre,'reused_real_ui_stills':True,'new_visuals':'locally rendered CTA graphics','policy':POLICY}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--genre',default='ai_work');a=p.parse_args()
 result=render(a.source,a.output,json.loads(Path(a.manifest).read_text()),a.genre);Path(a.report).write_text(json.dumps(result,ensure_ascii=False,indent=2))