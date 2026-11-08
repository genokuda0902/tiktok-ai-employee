"""Review-only five-scene synthetic video. Requires Pillow, FFmpeg and Noto CJK fonts."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
P=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('集計に10分？','Excelの合計を一瞬で','BEFORE'),('まず範囲を選択','B2からB5まで','STEP 01'),('SUM関数を入力','=SUM(B2:B5)','STEP 02'),('結果を確認','12 + 18 + 24 + 16 = 70','AFTER'),('保存して試そう','架空データの操作例','REVIEW ONLY')]
def render():
    P.mkdir(parents=True,exist_ok=True)
    for i,(head,sub,tag) in enumerate(SCENES):
        im=Image.new('RGB',(720,1280),(8,16,33));d=ImageDraw.Draw(im)
        d.rounded_rectangle((45,180,675,1040),radius=32,fill=(24,39,63))
        d.rectangle((45,180,675,194),fill=(26,193,201))
        d.text((70,245),tag,font=ImageFont.truetype(FONT,32),fill=(65,219,220))
        d.text((70,380),head,font=ImageFont.truetype(FONT,47),fill='white')
        d.text((70,510),sub,font=ImageFont.truetype(REG,30),fill=(232,237,244))
        for j in range(5):
            d.rounded_rectangle((70+j*116,930,165+j*116,942),radius=5,fill=(45,220,205) if j<=i else (74,87,110))
        d.text((70,1100),'FICTIONAL DATA  •  HUMAN REVIEW',font=ImageFont.truetype(REG,21),fill=(160,175,194))
        im.save(P/f'frame{i}.png')
    (P/'captions.srt').write_text(''.join(f'{i+1}\\n00:00:{i*3:02d},000 --> 00:00:{(i+1)*3:02d},000\\n{a}。{b}\\n\\n' for i,(a,b,c) in enumerate(SCENES)).replace('\\n','\n'),encoding='utf-8')
    with (P/'concat.txt').open('w') as f:
        for i in range(5): f.write(f"file 'frame{i}.png'\\nduration 3\\n".replace('\\n','\n'))
        f.write("file 'frame4.png'\n")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(P/'concat.txt'),'-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','ultrafast','-movflags','+faststart',str(P/'cycle1312_REVIEW_ONLY.mp4')],check=True)
if __name__=='__main__': render()
