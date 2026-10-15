"""Generate a non-narrated 3-step checklist for the final 1.7 seconds.
Requires baseline video assets/cycle587.mp4 (delivered separately in ZIP).
"""
from pathlib import Path
import argparse, json, os, math, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'assets/cycle587.mp4'
OUTPUT=ROOT/'output/cycle588_SILENT_CHECKLIST_HUMAN_REVIEW.mp4'
W,H,FPS,NFRAMES,Y,CHECKLIST_START=1080,1920,30,468,935,417
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def themes():
    return json.loads((ROOT/'config/genres.json').read_text(encoding='utf8'))['genres']
def rgb(s): return tuple(int(s[i:i+2],16) for i in (1,3,5))
def card(genre='雑学・科学',phase=1.0):
    if genre not in themes(): raise ValueError('unknown genre')
    accent=rgb(themes()[genre]['theme'])
    phase=max(0.0,min(1.0,float(phase)))
    im=Image.new('RGB',(1080,985),(4,15,30))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((56,60,902,820),radius=38,fill=(11,31,49),outline=accent,width=4)
    d.rounded_rectangle((90,98,488,159),radius=16,fill=(19,57,67))
    d.text((111,105),'音声後のチェックリスト',font=ImageFont.truetype(REG,31),fill=accent)
    d.text((92,194),'最初の3ステップ',font=ImageFont.truetype(FONT,60),fill=(251,254,255))
    steps=[('準備する','本体・電源・microSD'),('起動する','OSを入れて画面につなぐ'),('作ってみる','LEDを光らせてみる')] if genre=='雑学・科学' else [('選んでみる','気になるポイントを一つ選ぶ'),('試してみる','小さな一歩を行動にする'),('振り返る','結果をメモして次に活かす')]
    for i,(head,detail) in enumerate(steps):
        top=305+i*150
        d.rounded_rectangle((91,top,863,top+125),radius=20,fill=(16,45,64),outline=(49,78,91),width=2)
        d.ellipse((114,top+27,180,top+93),fill=accent)
        d.text((133,top+29),str(i+1),font=ImageFont.truetype(FONT,35),fill=(7,26,40))
        d.text((211,top+14),head,font=ImageFont.truetype(FONT,39),fill=(251,254,255))
        d.text((211,top+72),detail,font=ImageFont.truetype(REG,31),fill=(199,224,232))
    d.text((99,748),'※この画面はナレーション字幕ではありません',font=ImageFont.truetype(REG,26),fill=(168,199,212))
    d.rounded_rectangle((96,797,865,808),radius=5,fill=(44,68,80))
    d.rounded_rectangle((96,797,96+round(769*phase),808),radius=5,fill=accent)
    d.text((60,858),'図解・CGイメージ   |   音声・字幕は確認待ち',font=ImageFont.truetype(REG,25),fill=(149,181,197))
    return im
def build(source=SOURCE,output=OUTPUT,genre='雑学・科学'):
    if not Path(source).is_file():raise FileNotFoundError(source)
    if len(themes())!=10:raise ValueError('expected 10 genre themes')
    folder=ROOT/'work'/'cta_frames';folder.mkdir(parents=True,exist_ok=True)
    blank=folder/'blank.png';Image.new('RGBA',(1080,985),(0,0,0,0)).save(blank)
    for k in range(9):card(genre,(k+1)/9).save(folder/f'cta_{k:02}.png')
    for i in range(NFRAMES):
        dest=folder/f'{i:04}.png'
        if dest.exists() or dest.is_symlink():dest.unlink()
        origin=blank if i<CHECKLIST_START else folder/f'cta_{min(8,i-CHECKLIST_START):02}.png'
        dest.symlink_to(os.path.relpath(origin,folder))
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(source),'-framerate','30','-start_number','0','-i',str(folder/'%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:935:shortest=1:format=auto,format=yuv420p[v]','-map','[v]','-map','0:a:0','-c:v','libx264','-preset','ultrafast','-threads','2','-crf','19','-r','30','-frames:v','468','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)],check=True)
    return output
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,default=SOURCE)
    p.add_argument('--output',type=Path,default=OUTPUT)
    p.add_argument('--genre',default='雑学・科学')
    a=p.parse_args()
    print(build(a.source,a.output,a.genre))
