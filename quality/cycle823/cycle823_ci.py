"""Cycle823: fictional app-UI visual upgrade, eight Japanese review-only slides.
No real screenshots, external assets, personal information or publishing.
"""
import importlib.util, json, shutil, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageChops
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path)
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
prior=load('cycle822_ci',ROOT/'cycle822/cycle822_ci.py')
art=prior.art
CAPTIONS=prior.LINES
INK='#193B50'
def txt(d,x,y,s,n=34,c=INK,anchor='lm'):
 d.text((x,y),s,font=art.font(n),fill=c,anchor=anchor)
def box(d,b,c='#EFF7FA',r=15):
 d.rounded_rectangle(b,radius=r,fill=c)
def ui(im,i,accent):
 d=ImageDraw.Draw(im)
 box(d,(64,482,1016,1130),'#FFFFFF',42)
 box(d,(95,513,985,1100),'#FFFFFF',26)
 box(d,(96,514,984,600),'#15384A',22)
 d.rectangle((96,566,984,601),fill='#15384A')
 for j,c in enumerate(('#F3817E','#EFC86D','#69D5AA')):
  d.ellipse((126+j*34,548,146+j*34,568),fill=c)
 txt(d,265,560,'WORKFLOW / DEMO',28,'#FFFFFF')
 txt(d,945,560,f'{i+1:02} / 08',28,'#FFFFFF','rm')
 if i==0:
  txt(d,140,666,'仕事を整理してからAIへ',40)
  for j,(a,b) in enumerate((('資料','情報収集'),('文章','下書き'),('確認','最終確認'))):
   x=145+j*270;box(d,(x,745,x+240,981))
   box(d,(x+75,770,x+165,859),accent,18)
   txt(d,x+120,814,str(j+1),48,'#FFFFFF','mm')
   txt(d,x+120,911,a,40,INK,'mm')
   txt(d,x+120,954,b,28,INK,'mm')
 elif i==1:
  txt(d,145,660,'繰り返しの作業を発見',40)
  for j,s in enumerate(('日報の集計','定型メール','議事録の整理','予定の転記')):
   y=710+j*91;box(d,(146,y,936,y+73))
   box(d,(168,y+20,201,y+53),accent,8)
   txt(d,228,y+38,s,34)
 elif i==2:
  txt(d,145,660,'完成見本｜議事録',40)
  for j,(a,b) in enumerate((('日時','10月25日'),('議題','仕事の効率化'),('決定','日報を自動集計'),('確認','人が最終チェック'))):
   y=714+j*82;box(d,(146,y,935,y+69),'#E7F3F7' if j%2==0 else '#F6FAFC')
   txt(d,177,y+35,a,30,'#627C8A');txt(d,420,y+35,b,31)
 elif i==3:
  txt(d,145,660,'指示文を3つに分ける',40)
  for j,(a,b) in enumerate((('目的','議事録をまとめる'),('条件','200文字・箇条書き'),('見本','表と同じ形式'))):
   y=710+j*114;box(d,(145,y,935,y+96))
   box(d,(166,y+18,290,y+77),accent,12)
   txt(d,228,y+48,a,31,'#FFFFFF','mm');txt(d,315,y+48,b,33)
 elif i==4:
  txt(d,145,665,'AIの回答を確認',40)
  for j,(s,ok) in enumerate((('日付が正しい','✓'),('数字が合っている','!'),('出典を確認した','✓'))):
   y=742+j*105;box(d,(145,y,934,y+84))
   box(d,(165,y+20,212,y+65),accent if ok=='✓' else '#E88C77',12)
   txt(d,189,y+43,ok,30,'#FFFFFF','mm');txt(d,240,y+42,s,33)
 elif i==5:
  txt(d,145,665,'修正前 → 修正後',40)
  for x,col,head,ls in ((145,'#FFF0EE','修正前',('長すぎる','結論がない','表がない')),(562,'#E8F8F3','修正後',('要点3つ','結論が先','表で整理'))):
   box(d,(x,734,x+372,1010),col)
   txt(d,x+186,783,head,38,INK,'mm')
   for j,s in enumerate(ls):txt(d,x+30,848+j*57,'• '+s,29)
 elif i==6:
  txt(d,145,665,'保存した指示の一覧',40)
  for j,s in enumerate(('日報の要約','メールの下書き','議事録の整理')):
   y=736+j*106;box(d,(145,y,935,y+84))
   txt(d,175,y+41,s,34)
   box(d,(769,y+20,906,y+65),accent,12)
   txt(d,837,y+43,'保存',27,'#FFFFFF','mm')
 else:
  txt(d,145,662,'毎日10分の時短なら',40)
  txt(d,540,740,'1週間で約50分',44,INK,'mm')
  d.line((178,996,924,996),fill='#BCD5E0',width=5)
  for j,h in enumerate((80,112,148,177,216)):
   x=200+j*150;box(d,(x,986-h,x+98,986),accent if j==4 else '#A6DDE9')
   txt(d,x+49,1023,('月','火','水','木','金')[j],28,INK,'mm')
  txt(d,540,1080,'※計算例。実測ではありません',26,'#607E8B','mm')
 txt(d,938,1113,'架空の画面 / DEMO',20,'#678594','rm')
def prepare(root):
 prior.prepare(root)
 src=root/'source'
 for i in range(8):
  p=src/f'scene_{i+1:02}.png'
  im=Image.open(p).convert('RGBA')
  ui(im,i,art.PALETTES['ai_work'])
  im.convert('RGB').save(p,optimize=True)
 (src/'asset_provenance823.json').write_text(json.dumps({'original_procedural_ui':True,'fictional':True,'no_external_images':True,'publication_approved':False},ensure_ascii=False))
def render(root):
 p=prior.render(root)
 out=root/'output'/'cycle823_UI_DEMO_JAPANESE_HUMAN_REVIEW.mp4'
 shutil.copy2(p,out)
 return out
def verify(root):
 p=root/'output'/'cycle823_UI_DEMO_JAPANESE_HUMAN_REVIEW.mp4'
 info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(p)]))
 v=next(x for x in info['streams'] if x['codec_type']=='video')
 a=next(x for x in info['streams'] if x['codec_type']=='audio')
 ass=(root/'output'/'captions817.ass').read_text()
 images=[Image.open(root/'source'/f'scene_{i:02}.png').convert('RGB') for i in range(1,9)]
 checks={'1080x1920':(v['width'],v['height'])==(1080,1920),'30fps':v['r_frame_rate']=='30/1',
 '775frames':int(v['nb_frames'])==775,'aac48k':a['codec_name']=='aac' and a['sample_rate']=='48000',
 '24captions':ass.count('Dialogue: 0,')==24,
 '8images':len(images)==8 and all(x.size==(1080,1920) for x in images),
 'full_decode':subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],capture_output=True).returncode==0,
 'provenance':(root/'source'/'asset_provenance823.json').exists()}
 report={'cycle':823,'checks':checks,'passed':sum(checks.values()),'total':len(checks),'review_only':True}
 (root/'output'/'qa823_ci.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 if not all(checks.values()):raise AssertionError(report)
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,required=True)
 parser.add_argument('--step',choices=('prepare','render','verify'),required=True)
 args=parser.parse_args();{'prepare':prepare,'render':render,'verify':verify}[args.step](args.root)
