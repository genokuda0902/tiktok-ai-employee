from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import subprocess, json
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
BOLD='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SCENES=[('入力前に確認','個人情報・機密情報は入れない'),('依頼を具体化','目的・条件・出力形式を伝える'),('結果を検証','数字・固有名詞を人が確認'),('小さく始める','今日の1作業で試してみる')]
FPS=12; W,H=720,1280; SEC=3
def render(out=None):
    out=Path(out) if out else ROOT/'cycle1466_REVIEW_ONLY.mp4'
    frames=ROOT/'frames';frames.mkdir(exist_ok=True)
    captions=[]
    for n,(heading,caption) in enumerate(SCENES):
        captions.append({'start':n*SEC,'end':(n+1)*SEC,'text':caption,'spoken':False})
        for f in range(FPS*SEC):
            im=Image.new('RGB',(W,H),'#091425');d=ImageDraw.Draw(im)
            progress=(f+1)/(FPS*SEC);x=int(40+8*progress)
            d.rounded_rectangle((x,120,680,1140),radius=30,fill='#172e49',outline='#386e85',width=3)
            d.rectangle((x,120,x+int((680-x)*progress),131),fill='#32d7d1')
            d.text((78,225),f'0{n+1} / 04',font=ImageFont.truetype(BOLD,40),fill='#48d9e3')
            d.text((78,355),heading,font=ImageFont.truetype(BOLD,49),fill='white')
            d.rounded_rectangle((70,565,650,795),radius=20,fill='#27445c')
            d.text((88,635),caption,font=ImageFont.truetype(BOLD,30),fill='white')
            d.text((80,1025),'REVIEW ONLY / 音声未実装',font=ImageFont.truetype(FONT,25),fill='#b1c6d0')
            im.save(frames/f'{n*FPS*SEC+f:04}.png')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(frames/'%04d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
    (ROOT/'captions.json').write_text(json.dumps(captions,ensure_ascii=False,indent=2))
    (ROOT/'qa.json').write_text(json.dumps({'narration_ja':False,'captions_spoken_sync':False,'rights_approved':False,'staff_approved':False,'publication_approved':False},indent=2))
    return out
if __name__=='__main__':print(render())
