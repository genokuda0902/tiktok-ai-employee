from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import subprocess,math
O=Path(__file__).parent; W,H=540,960; FPS=12; DUR=31.2
regular='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def font(n,b=False):return ImageFont.truetype(bold if b else regular,n)
def text(d,xy,s,n=24,color='#eaf3ff',b=False):d.text(xy,s,font=font(n,b),fill=color)
def box(d,coords,color,r=12,outline=None):d.rounded_rectangle(coords,radius=r,fill=color,outline=outline,width=2)
def screen(d):
 box(d,(18,110,522,840),'#101e30',20,'#31516c');box(d,(35,127,505,178),'#233a50',10);text(d,(51,138),'AI時短ラボ  /  操作デモ',19,'#8fe9d8',True)
 text(d,(32,47),'毎日のExcel集計、',34,b=True);text(d,(32,88),'AIでここまで変わる。',27,'#76e7d1',True)
 text(d,(31,865),'※画面と数値は架空のデモです',17,'#9db5c9')
def excel(d,x0=43,y0=238):
 box(d,(x0,y0,x0+452,y0+420),'#f6f9fc',9)
 d.rectangle((x0,y0,x0+452,y0+43),fill='#176c48');text(d,(x0+15,y0+7),'Excel  |  売上集計_サンプル.xlsx',16,'white',True)
 d.rectangle((x0,y0+43,x0+452,y0+82),fill='#e5edf3');text(d,(x0+12,y0+50),'ホーム    挿入    数式    データ',15,'#253e50')
 for j in range(6):
  yy=y0+87+j*48;d.line((x0+10,yy+42,x0+442,yy+42),fill='#d6e2ea',width=1)
  vals=[['月','売上','件数'],['1月','120','12'],['2月','150','15'],['3月','190','19'],['4月','250','25'],['合計','710','71']][j]
  for k,v in enumerate(vals):text(d,(x0+23+k*145,yy+6),v,18,'#18384c',j==0 or j==5)
 return x0,y0
for i in range(round(DUR*FPS)):
 t=i/FPS; im=Image.new('RGB',(W,H),'#081522');d=ImageDraw.Draw(im)
 d.ellipse((320,-150,750,350),fill='#102e40');d.ellipse((-280,700,170,1200),fill='#0b2b32')
 screen(d)
 if t<4.5:
  text(d,(54,208),'こんな作業、まだ毎日？',29,'#f3fbff',True);excel(d,43,290)
  if t>1:box(d,(75,705,467,765),'#f2c06b',10);text(d,(95,717),'転記 → 集計 → グラフ',22,'#172637',True)
 elif t<10:
  excel(d,43,218);progress=min(1,(t-4.5)/4)
  x=110+int(progress*295);y=380+int(math.sin(progress*math.pi)*65)
  d.polygon([(x,y),(x+4,y+31),(x+12,y+23),(x+20,y+43),(x+27,y+40),(x+17,y+19),(x+30,y+17)],fill='#163f69')
  if t>7.8:box(d,(68,685,474,761),'#176d55');text(d,(89,699),'データをまとめてコピー',23,b=True)
 elif t<16:
  box(d,(43,215,497,720),'#f6f8fa',16)
  box(d,(43,215,497,266),'#f6f8fa',12);d.ellipse((61,227,89,255),fill='#0b8c67');text(d,(102,227),'ChatGPT  /  デモ',21,'#172637',True)
  prompt='この表を月別に集計して\n変化がわかるグラフを作って'
  box(d,(65,305,477,420),'#e8edf1',12)
  n=max(0,min(len(prompt),int((t-10)*10)));text(d,(80,320),prompt[:n],21,'#203447',True)
  if t>13:
   d.ellipse((66,464,95,493),fill='#0b8c67');text(d,(106,464),'集計結果を整理しました。',20,'#22394a')
   text(d,(107,509),'増加傾向が確認できます。',19,'#22394a')
  text(d,(61,748),'Excel → ChatGPT',28,'#76e7d1',True)
 elif t<22.5:
  box(d,(43,220,497,724),'#f7f9fc',12);text(d,(65,239),'売上推移  /  デモデータ',23,'#1a394d',True)
  vals=[120,150,190,250];labels=['1月','2月','3月','4月'];p=min(1,(t-16)/3.2)
  for k,(v,l) in enumerate(zip(vals,labels)):
   h=int(v*1.15*p);x=92+k*98
   d.rectangle((x,615-h,x+54,615),fill='#168c71');text(d,(x+5,630),l,19,'#244055');
   if p>.8:text(d,(x+4,590-h),str(v),18,'#1e485b',True)
  d.line((72,615,465,615),fill='#7895a9',width=3)
  if t>19.4:box(d,(80,690,462,749),'#176c56');text(d,(103,703),'数字の変化が一目でわかる',20,b=True)
 elif t<27:
  text(d,(59,229),'BEFORE',32,'#ffbd8c',True);box(d,(51,293,489,426),'#29374a');text(d,(81,319),'転記・集計・グラフ作成',23,b=True);text(d,(81,367),'同じ作業を繰り返す',20,'#b5c8d8')
  text(d,(59,472),'AFTER',32,'#8ce9d0',True);box(d,(51,537,489,671),'#155b52');text(d,(81,561),'AIで整理・可視化',25,b=True);text(d,(81,614),'人は結果を確認する',21)
 else:
  text(d,(57,247),'まずは、',41,b=True);text(d,(57,327),'いつもの集計を',37,b=True);text(d,(57,405),'ひとつだけ。',43,'#7ae8d2',True)
  box(d,(56,555,482,656),'#176c57',17);text(d,(90,579),'保存して、あとで試す',27,b=True)
  text(d,(91,711),'AI時短ラボ  /  第1回',22,'#9bb9ca')
 im.save(O/f'frame_{i:04d}.jpg',quality=88)
cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate',str(FPS),'-i',str(O/'frame_%04d.jpg'),'-i','/mnt/data/AI_Jitan_v33_REAL_SPREADSHEET.mp4','-filter:v','scale=720:1280:flags=lanczos,fps=30,format=yuv420p','-map','0:v','-map','1:a:0','-t',str(DUR),'-c:v','libx264','-preset','veryfast','-crf','20','-c:a','aac','-b:a','160k','-movflags','+faststart',str(O/'first_post_review.mp4')]
subprocess.run(cmd,check=True)
print('OUTPUT',O/'first_post_review.mp4')