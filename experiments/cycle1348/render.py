"""Public-safe, review-only caption-timing demo. Requires Pillow, FFmpeg, Japanese font. No narration."""
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont
OUT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('売上の合計、手計算していませんか？','問題：毎回足し算する',3),('B2からB5の数字を選択','セルを確認する',3),('=SUM(B2:B5) と入力','式を入力する',3),('Enterで合計が表示される','結果を確認する',3)]
def draw_frame(i):
 im=Image.new('RGB',(1080,1920),'#0a1425');d=ImageDraw.Draw(im)
 f=ImageFont.truetype(FONT,60);sm=ImageFont.truetype(FONT,40)
 d.rounded_rectangle((65,250,1015,1400),radius=40,fill='#17263c')
 d.text((90,110),f'Excel時短  {i+1}/4',font=sm,fill='#72e0d2')
 d.text((100,350),SCENES[i][0],font=f,fill='white',stroke_width=1)
 d.rounded_rectangle((115,580,965,1100),radius=18,fill='#edf3f5')
 d.text((170,635),'商品       売上',font=sm,fill='#17263c')
 for j,v in enumerate([1200,2400,1800,3200]):
  d.text((170,720+j*75),f'{j+2}行目        {v:,}',font=sm,fill='#17263c')
 if i>=2:d.text((170,1040),'=SUM(B2:B5)' if i==2 else '合計 8,600',font=sm,fill='#047857')
 d.rounded_rectangle((70,1460,1010,1680),radius=25,fill='#101b2c')
 d.text((100,1510),SCENES[i][1],font=f,fill='#ffffff')
 d.text((100,1770),'REVIEW ONLY / 音声未実装',font=sm,fill='#fca5a5')
 p=OUT/f'scene{i}.png';im.save(p);return p
def main():
 paths=[draw_frame(i) for i in range(len(SCENES))]
 lines=[]
 for p,(_,_,dur) in zip(paths,SCENES):lines.extend([f'file {p.name}',f'duration {dur}'])
 lines.append(f'file {paths[-1].name}')
 (OUT/'frames.txt').write_text('\n'.join(lines)+'\n')
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(OUT/'frames.txt'),'-t','12','-vf','fps=30,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','21','-movflags','+faststart',str(OUT/'cycle1348_REVIEW_ONLY.mp4')],check=True)
if __name__=='__main__':main()
