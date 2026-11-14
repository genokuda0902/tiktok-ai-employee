from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def font(n,b=False): return ImageFont.truetype(BOLD if b else FONT,n)
def render():
 out=ROOT/'cycle1445_REVIEW_ONLY.mp4'; fps=18; duration=12
 cmd=['ffmpeg','-y','-hide_banner','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s','540x960','-r',str(fps),'-i','-','-vf','scale=1080:1920:flags=lanczos,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','22','-movflags','+faststart',str(out)]
 p=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for f in range(fps*duration):
   t=f/fps; stage=min(2,int(t//4))
   im=Image.new('RGB',(540,960),'#101a2b'); d=ImageDraw.Draw(im)
   d.rounded_rectangle((26,85,514,754),radius=25,fill='#edf4f7')
   d.rounded_rectangle((42,151,498,650),radius=16,fill='white')
   d.text((31,24),'AI × 仕事術  /  SAFE REVIEW',font=font(24,True),fill='#eaf5ff')
   d.text((55,107),['01  よくある悩み','02  数式を入力','03  結果を検算'][stage],font=font(29,True),fill='#16465c')
   for x in [64,185,315,476]: d.line((x,230,x,563),fill='#b5cbd0',width=2)
   for y in [230,295,362,429,496,563]: d.line((64,y,476,y),fill='#b5cbd0',width=2)
   for i,v in enumerate(['1,200','2,300','3,200']): d.text((330,302+i*67),v,font=font(24),fill='#213a4a')
   for i,s in enumerate(['B2','B3','B4']): d.text((85,302+i*67),s,font=font(21),fill='#567080')
   d.rectangle((315,496,476,563),outline='#079e91',width=4)
   if stage==0: d.text((75,598),'手計算はミスの原因に',font=font(24,True),fill='#334c5b')
   elif stage==1:
    n=min(11,max(0,int((t-4)*5)))
    d.text((72,598),'=SUM(B2:B4)'[:n]+'▏',font=font(25,True),fill='#06766b')
   else:
    d.text((326,508),'6,700',font=font(24,True),fill='#06766b')
    d.text((72,598),'1,200+2,300+3,200=6,700',font=font(19,True),fill='#06766b')
   captions=['合計を毎回、手で入力していませんか？','SUM関数で、合計を自動計算。','結果が正しいか、最後に確認。']
   d.rounded_rectangle((26,776,514,876),radius=16,fill='#174658')
   d.rounded_rectangle((26,887,514,895),radius=4,fill='#36556a')
   d.rounded_rectangle((26,887,26+int(488*(f+1)/(fps*duration)),895),radius=4,fill='#2bc4b5')
   d.text((41,808),captions[stage],font=font(21,True),fill='white')
   d.text((28,918),'独自作画・架空データ｜音声未実装｜社内確認専用',font=font(16),fill='#ffca9e')
   p.stdin.write(im.tobytes())
 finally: p.stdin.close()
 if p.wait(): raise RuntimeError('ffmpeg failed')
 (ROOT/'captions.srt').write_text('1\n00:00:00,000 --> 00:00:04,000\n合計を毎回、手で入力していませんか？\n\n2\n00:00:04,000 --> 00:00:08,000\nSUM関数で、合計を自動計算。\n\n3\n00:00:08,000 --> 00:00:12,000\n結果が正しいか、最後に確認。\n',encoding='utf8')
 subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
 return out
if __name__=='__main__': print(render())
