"""Public-safe, review-only Japanese scene renderer. Requires Pillow, ffmpeg, Noto CJK."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json
ROOT=Path(__file__).resolve().parent
W,H=1080,1920
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('入力の表記ゆれ、','見落としていませんか？','BEFORE'),('同じ意味でも','表記がバラバラ','BEFORE'),('入力ルールを統一','確認しやすい形に','AFTER'),('最後は人が確認','安全に業務へ活用','CHECK')]
def render(out):
    out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    frames=out.parent/'frames';frames.mkdir(exist_ok=True)
    for i,(a,b,tag) in enumerate(SCENES):
        im=Image.new('RGB',(W,H),(9,17,34));d=ImageDraw.Draw(im)
        d.rounded_rectangle((72,170,1008,1750),radius=42,fill=(20,34,56),outline=(60,86,114),width=4)
        d.rounded_rectangle((110,235,440,310),radius=22,fill=(18,113,133))
        d.text((135,245),tag,font=ImageFont.truetype(BOLD,38),fill='white')
        d.text((110,450),a,font=ImageFont.truetype(BOLD,67),fill='white')
        d.text((110,575),b,font=ImageFont.truetype(BOLD,58),fill=(125,224,234))
        d.rounded_rectangle((120,840,960,1350),radius=28,fill=(30,49,72))
        rows=['東京都 / 東京','株式会社ABC / (株)ABC','2026-11-22 / 11月22日'] if i<2 else ['東京都','株式会社ABC','2026年11月22日']
        for j,s in enumerate(rows):
            y=905+j*130;d.rounded_rectangle((155,y,925,y+100),radius=18,fill=(43,64,89))
            d.text((185,y+22),s,font=ImageFont.truetype(FONT,37),fill='white')
        d.text((130,1530),'例示データのみ・公開前に確認',font=ImageFont.truetype(FONT,35),fill=(180,192,208))
        d.rounded_rectangle((120,1660,120+int(840*(i+1)/4),1678),radius=9,fill=(65,210,225))
        im.save(frames/f'{i:02}.png')
    concat=out.parent/'concat.txt'
    concat.write_text(''.join(f"file '{(frames/f'{i:02}.png').resolve()}'\\nduration 3\\n" for i in range(4)).replace('\\n','\n')+f"file '{(frames/'03.png').resolve()}'\n")
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',str(concat),'-t','12','-vf','fps=24,format=yuv420p','-c:v','libx264','-preset','veryfast','-crf','25','-movflags','+faststart','-an',str(out)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=codec_type,codec_name,width,height,r_frame_rate','-of','json',str(out)],text=True))
if __name__=='__main__':
    print(json.dumps(render(ROOT/'cycle1633_REVIEW_ONLY.mp4'),indent=2))
