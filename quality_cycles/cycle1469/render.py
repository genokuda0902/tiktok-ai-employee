"""Cycle1469 reproducible review-only 8-second video; Pillow and ffmpeg required."""
from pathlib import Path
import json, subprocess
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parent
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
W,H,FPS=720,1280,12
SCENES=[('01','その作業、何分かかる？','まず時間を記録',0,2),('02','AIへの依頼を具体的に','目的・条件・形式を入力',2,4),('03','出力を比較して確認','数字と事実を照合',4,6),('04','最後は人が判断','公開には社員承認が必要',6,8)]
def make(out=ROOT/'cycle1469_REVIEW_ONLY.mp4'):
    out=Path(out); frames=ROOT/'frames';frames.mkdir(exist_ok=True)
    for k in range(FPS*8):
        t=k/FPS; idx=min(3,int(t//2)); num,head,sub,start,end=SCENES[idx]
        im=Image.new('RGB',(W,H),'#071422');d=ImageDraw.Draw(im)
        d.rounded_rectangle((38,125,682,1080),radius=28,fill='#122a3b')
        d.text((70,185),'AI WORKFLOW / DEMO',font=ImageFont.truetype(FONT,27),fill='#55d9cd')
        d.text((70,295),head,font=ImageFont.truetype(FONT,34),fill='white')
        d.rounded_rectangle((70,420,650,740),radius=20,fill='#f0f4f8')
        for j in range(4):
            y=455+j*65;d.rounded_rectangle((94,y,626,y+42),radius=6,fill=('#c5e9e6' if j==idx else '#d6dfe7'))
            d.rectangle((110,y+14,110+int((j+2)*57*(0.3+0.7*((t-start)/2))),y+24),fill='#367b92')
        d.rounded_rectangle((70,810,650,942),radius=15,fill='#02080e')
        d.text((90,852),sub,font=ImageFont.truetype(FONT,29),fill='white')
        d.rectangle((70,1010,70+int(580*(k+1)/(FPS*8)),1021),fill='#50e4ce')
        d.text((70,1140),'REVIEW ONLY • 音声なし • 投稿禁止',font=ImageFont.truetype(FONT,22),fill='#e4b9a7')
        im.save(frames/f'{k:04d}.png')
    subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',str(frames/'%04d.png'),'-c:v','libx264','-preset','veryfast','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],check=True)
    (ROOT/'captions.json').write_text(json.dumps([{'start':s,'end':e,'text':sub,'speech_verified':False} for _,_,sub,s,e in SCENES],ensure_ascii=False,indent=2),encoding='utf8')
    return out
if __name__=='__main__':print(make())
