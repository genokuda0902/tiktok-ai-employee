"""Review-only reimplementation, not recovered v33. Requires Pillow and FFmpeg."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess
ROOT=Path(__file__).parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SCENES=[('01 / BEFORE','作業が多すぎる','毎日の確認に時間がかかる','課題を整理する'),('02 / ACTION','AIに条件を伝える','目的・項目・形式を指定','小さく試して確認する'),('03 / AFTER','確認しやすい形へ','結果は必ず人がチェック','公開前に承認する')]
def render():
    clips=[]
    for i,(tag,title,sub,foot) in enumerate(SCENES):
        im=Image.new('RGB',(720,1280),'#0b1426'); d=ImageDraw.Draw(im)
        d.rounded_rectangle((42,92,678,1170),radius=36,fill='#15253c',outline='#315574',width=3)
        d.rounded_rectangle((70,148,650,213),radius=17,fill='#245978')
        d.text((92,161),tag,font=ImageFont.truetype(REG,27),fill='white')
        d.text((78,335),title,font=ImageFont.truetype(FONT,48),fill='white')
        d.text((78,450),sub,font=ImageFont.truetype(REG,29),fill='#c7dfed')
        for j in range(3):
            y=630+j*100
            d.rounded_rectangle((85,y,635,y+65),radius=14,fill=('#207c9d' if j==i else '#233b56'))
            d.text((105,y+13),['状況を把握','条件を指定','結果を確認'][j],font=ImageFont.truetype(REG,24),fill='white')
        d.text((82,1040),foot,font=ImageFont.truetype(REG,27),fill='#a8e9df')
        d.text((80,1200),'REVIEW ONLY  /  PUBLICATION NOT APPROVED',font=ImageFont.truetype(REG,16),fill='#94a3b8')
        p=ROOT/f'scene{i}.png'; im.save(p)
        clip=ROOT/f'scene{i}.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1','-framerate','24','-i',str(p),'-t','5','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(clip)],check=True)
        clips.append(clip)
    lst=ROOT/'concat.txt'
    lst.write_text(''.join(f"file '{p}'\n" for p in clips))
    out=ROOT/'cycle1261_REVIEW_ONLY.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(lst),'-c','copy','-movflags','+faststart',str(out)],check=True)
    return out
if __name__=='__main__': print(render())
