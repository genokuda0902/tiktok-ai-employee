"""Synthetic review-only TikTok story, no private assets, no automatic posting."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STAGES=[('BEFORE','集計がバラバラ','120 + 180 = ?','確認に時間がかかる'),('ACTION','計算式を入力','=SUM(B2:B3)','数字をまとめて確認'),('AFTER','合計がひと目で','300','入力値は架空のサンプル')]
def render(output=None):
    output=Path(output or ROOT/'cycle1250_REVIEW_ONLY.mp4')
    output.parent.mkdir(parents=True,exist_ok=True)
    frames=[]
    for k,(en,head,formula,foot) in enumerate(STAGES):
        im=Image.new('RGB',(720,1280),(9,19,38)); d=ImageDraw.Draw(im)
        d.rounded_rectangle((42,65,678,1195),radius=38,fill=(20,36,62),outline=(58,91,128),width=3)
        d.text((75,110),'AI WORKFLOW  /  DEMO',font=ImageFont.truetype(BOLD,28),fill='#69D8F5')
        d.text((75,215),en,font=ImageFont.truetype(BOLD,45),fill='#9BDCF3')
        d.text((75,295),head,font=ImageFont.truetype(BOLD,49),fill='white')
        d.rounded_rectangle((75,415,645,900),radius=20,fill=(242,247,250))
        for j,label in enumerate(['項目','数値','A','120','B','180','合計',formula]):
            x=95 if j%2==0 else 350; y=455+(j//2)*98
            d.text((x,y),label,font=ImageFont.truetype(BOLD if j>5 else FONT,30 if j!=7 else 28),fill=(17,37,62))
        d.text((75,980),foot,font=ImageFont.truetype(FONT,28),fill='#D7E8F6')
        d.text((75,1080),'REVIEW ONLY / 投稿未承認',font=ImageFont.truetype(BOLD,23),fill='#F6B8B8')
        p=output.parent/f'cycle1250_scene{k}.png'; im.save(p);frames.append(p)
    concat=output.parent/'cycle1250_scenes.txt'
    concat.write_text(''.join(f"file '{p}'\\nduration 4\\n" for p in frames)+f"file '{frames[-1]}'\\n".replace('\\n','\n').replace('\\n','\n'))
    # Ensure the ffmpeg concat file contains real newlines.
    concat.write_text(''.join("file '"+str(p)+"'\nduration 4\n" for p in frames)+"file '"+str(frames[-1])+"'\n")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','21','-movflags','+faststart','-t','12',str(output)],check=True)
    return output
if __name__=='__main__':print(render())
