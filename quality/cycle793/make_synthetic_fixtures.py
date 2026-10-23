"""Generate CI-only synthetic Japanese text / sine-tone fixtures (no user assets)."""
import argparse,subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def run(args):
    p=subprocess.run(args,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-3000:])
def build(directory):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    for label in ('clean','obstructed'):
        im=Image.new('RGB',(1080,1920),'#061829')
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((90,1200,990,1650),radius=30,fill='#153f55')
        d.text((130,1260),'架空データの合計',font=ImageFont.truetype(FONT,58),fill='white')
        d.text((130,1410),'650,000円',font=ImageFont.truetype(FONT,95),fill='white')
        if label=='obstructed':
            d.rounded_rectangle((260,1375,860,1500),radius=10,fill='#3a1c07')
            d.text((280,1395),'4か月の合計は65万円',font=ImageFont.truetype(FONT,47),fill='white')
        png=directory/f'{label}.png';im.save(png)
        video=directory/f'{label}_silent.mp4'
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-loop','1',
             '-framerate','30','-i',str(png),'-frames:v','714','-c:v','libx264',
             '-preset','ultrafast','-crf','33','-pix_fmt','yuv420p',str(video)])
        run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(video),
             '-f','lavfi','-i','sine=frequency=392:sample_rate=48000:duration=23.843',
             '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac',
             '-b:a','64k','-movflags','+faststart',str(directory/f'{label}.mp4')])
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output-dir',required=True)
    build(p.parse_args().output_dir)
