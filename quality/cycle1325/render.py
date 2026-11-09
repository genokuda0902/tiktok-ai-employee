# cycle1325: reproducible four-scene review renderer (requires Pillow, ffmpeg, Noto CJK)
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('売上集計、まだ手入力？','表計算の時短を実演'),('まず合計セルを選択','B6 を選ぶ'),('=SUM(B2:B5) を入力','範囲をまとめて合計'),('完成！合計は 48,000円','数式と結果を必ず確認')]
def render():
    frames=ROOT/'frames'; frames.mkdir(exist_ok=True)
    for i,(head,caption) in enumerate(SCENES):
        im=Image.new('RGB',(720,1280),'#0b1424'); d=ImageDraw.Draw(im)
        f=ImageFont.truetype(BOLD,42); s=ImageFont.truetype(FONT,28); tiny=ImageFont.truetype(FONT,26)
        d.rounded_rectangle((36,95,684,1100),radius=28,fill='#17283e')
        d.text((65,145),head,font=f,fill='white')
        d.rounded_rectangle((65,320,655,810),radius=12,fill='#f9fbfd')
        for row in range(6):
            y=385+row*65; d.line((85,y,630,y),fill='#c7d2de',width=2)
        d.line((370,350,370,750),fill='#c7d2de',width=2)
        for row,(a,b) in enumerate([('項目','金額'),('A','12,000'),('B','8,000'),('C','15,000'),('D','13,000'),('合計','48,000')]):
            y=350+row*65
            d.text((105,y),a,font=tiny,fill='#182b42')
            d.text((398,y),b if row!=5 or i==3 else ('=SUM(B2:B5)' if i==2 else ''),font=ImageFont.truetype(FONT,22),fill='#182b42')
        if i in (1,2): d.rectangle((373,675,625,739),outline='#0b9b7e',width=5)
        d.rounded_rectangle((60,930,660,1050),radius=24,fill='#143f58')
        d.text((85,960),caption,font=s,fill='white')
        d.text((65,1135),'REVIEW ONLY  |  未承認・投稿禁止',font=ImageFont.truetype(FONT,20),fill='#d4dae5')
        im.save(frames/f'{i:02}.png')
    concat=ROOT/'concat.txt'
    concat.write_text(''.join("file '"+str((frames/f'{i:02}.png').resolve())+"'\nduration 3\n" for i in range(4))+"file '"+str((frames/'03.png').resolve())+"'\n")
    out=ROOT/'cycle1325_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','ultrafast','-crf','25','-movflags','+faststart',str(out)],check=True)
    return out
if __name__=='__main__': print(render())
