"""Cycle1062: fictional real-Calc static screenshot in scene03 (review only).

Source audio/captions are preserved. This is NOT a live screen recording.
Never commit private screenshots, MP4s or extracted voice.
"""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from quality.cycle1058.real_writer_focus import PALETTES

W, H, FPS = 1080, 1270, 30
START, COUNT = 174, 82
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SOURCE_CROP = (57, 275, 580, 480)
TABLE_RECT = (85, 436, 995, 887)
PROTECTED_TABLE = (132, 505, 958, 856)
STEPS = ('画面で確認', '数字を比較', '完成見本にする')
NOTES = ('架空の4〜6月データを開く', 'A 12+16+18=46 / B 8+9+12=29', '完成形の見本として残す')

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def stage(i):
    if not 0 <= i < COUNT:
        raise ValueError('frame index out of range')
    return min(2, i // 28)

def render_frame(i, screenshot, genre='ai_work'):
    if genre not in PALETTES:
        raise ValueError('unknown or unapproved genre')
    s = stage(i)
    shot = Image.open(screenshot).convert('RGB') if not isinstance(screenshot, Image.Image) else screenshot.convert('RGB')
    if shot.size != (1600,900):
        raise ValueError('1600x900 sanitized Calc screenshot required')
    accent = PALETTES[genre]
    im = Image.new('RGB',(W,H),'#071827')
    d = ImageDraw.Draw(im)
    font = lambda n: ImageFont.truetype(FONT,n)
    d.rounded_rectangle((38,40,1042,1170),radius=32,fill='#0C293B',outline='#335B70',width=3)
    d.text((75,82),'完成形の見本を用意する',font=font(52),fill='#F6FAFC')
    d.text((79,166),'LibreOffice Calc / 実アプリ画面・架空データ',font=font(26),fill='#A8CBD8')
    for j,label in enumerate(STEPS):
        x=78+j*324
        d.rounded_rectangle((x,245,x+302,325),radius=14,
          fill='#0E5965' if j==s else '#173B50',
          outline=accent if j==s else '#36596B',width=3 if j==s else 1)
        d.text((x+18,265),f'{j+1:02d} {label}',font=font(25),fill='#FFFFFF')
    d.rounded_rectangle((66,386,1015,930),radius=22,fill='#F5F7F8',outline='#497285',width=3)
    crop=shot.crop(SOURCE_CROP).resize((TABLE_RECT[2]-TABLE_RECT[0],TABLE_RECT[3]-TABLE_RECT[1]),Image.Resampling.LANCZOS)
    im.paste(crop,TABLE_RECT[:2])
    d=ImageDraw.Draw(im)
    y=(562,652,772)[s]
    d.rounded_rectangle((96,y-22,119,y+22),radius=9,fill=accent)
    d.rounded_rectangle((80,958,1000,1070),radius=18,fill='#0B4455')
    d.text((104,987),NOTES[s],font=font(29 if s==1 else 33),fill='#FFFFFF')
    d.rounded_rectangle((82,1110,998,1121),radius=5,fill='#294E62')
    d.rounded_rectangle((82,1110,82+int(916*(i+1)/COUNT),1121),radius=5,fill=accent)
    d.text((84,1140),'STATIC SCREENSHOT / FICTIONAL DATA / REVIEW ONLY',font=font(20),fill='#AECAD6')
    return im

def compose(source,screenshot,output,work,source_sha256,screenshot_sha256,genre='ai_work'):
    if genre not in PALETTES:
        raise ValueError('unapproved genre')
    for p,expected in ((source,source_sha256),(screenshot,screenshot_sha256)):
        if not expected or len(expected)!=64 or sha256(p)!=expected:
            raise ValueError('missing/mismatched private input SHA-256')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    folder=Path(work)/'frames';folder.mkdir(parents=True,exist_ok=True)
    shot=Image.open(screenshot).convert('RGB')
    for i in range(COUNT):
        render_frame(i,shot,genre).save(folder/f'frame_{i:03d}.png')
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-framerate',str(FPS),'-start_number','0','-i',str(folder/'frame_%03d.png'),
      '-filter_complex',f'[1:v]setpts=PTS+{START/FPS:.9f}/TB[insert];[0:v][insert]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
      '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
      '-movflags','+faststart',str(output)],check=True)

def smoke():
    with tempfile.TemporaryDirectory() as td:
        p=Path(td);shot=Image.new('RGB',(1600,900),'white')
        for i in range(15):
            render_frame(i,shot).save(p/f'f_{i:03d}.png')
        mp4=p/'synthetic.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
          '-framerate','30','-i',str(p/'f_%03d.png'),'-f','lavfi',
          '-i','sine=frequency=440:sample_rate=48000:duration=0.5',
          '-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast',
          '-pix_fmt','yuv420p','-c:a','aac',str(mp4)],check=True)
        streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(mp4)]))['streams']
        assert {x['codec_name'] for x in streams}=={'h264','aac'}
        subprocess.run(['ffmpeg','-v','error','-i',str(mp4),'-f','null','-'],check=True)
        print('PASS synthetic 0.5s H264/AAC; private full MP4 not tested by CI')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for arg in ('source','screenshot','out','work','source-sha256','screenshot-sha256'):
        p.add_argument('--'+arg)
    p.add_argument('--genre',default='ai_work')
    p.add_argument('--smoke',action='store_true')
    a=p.parse_args()
    if a.smoke: smoke()
    else: compose(a.source,a.screenshot,a.out,a.work,a.source_sha256,a.screenshot_sha256,a.genre)
