"""Review-only: real LibreOffice Writer screenshot, fictional prompt, 10-genre overlays.

The screenshot must be captured locally from a genuine application. This module
never claims that the static screenshot is a live screen recording or ASR proof.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, START, COUNT = 1080, 1270, 30, 520, 89
PALETTES = {
    'ai_work': '#24D9D0', 'money': '#6EE6A7', 'health': '#74D7D2',
    'history': '#F1C57C', 'science': '#80C7FA', 'language': '#B4D4FA',
    'career': '#79C7FB', 'lifestyle': '#F1B7D5', 'travel': '#98D7F8',
    'education': '#B5C4FA',
}
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
STEPS = ('保存', '再利用', '人が確認')

def stage(i):
    if not 0 <= i < COUNT:
        raise ValueError('frame out of range')
    return 0 if i < 28 else 1 if i < 59 else 2

def render_frame(i, screenshot, genre='ai_work'):
    if genre not in PALETTES:
        raise ValueError('unapproved genre')
    s = stage(i)
    screenshot = Image.open(screenshot).convert('RGB') if not isinstance(screenshot, Image.Image) else screenshot.convert('RGB')
    if screenshot.width < 1400 or screenshot.height < 800:
        raise ValueError('genuine 1600x900 app capture required')
    accent = PALETTES[genre]
    im = Image.new('RGB', (W, H), '#071829')
    d = ImageDraw.Draw(im)
    f = lambda n: ImageFont.truetype(FONT, n)
    for y in range(H):
        d.line((0, y, W, y), fill=(7 + y//250, 24 + y//130, 41 + y//110))
    d.rounded_rectangle((40, 38, 1040, 1174), radius=32, fill='#0C2C42', outline='#335A6D', width=3)
    d.text((77, 75), '使える指示を、テンプレート化', font=f(50), fill='#F5FAFC')
    d.text((80, 158), '実際のWriter画面で保存内容を確認', font=f(28), fill='#A9CAD8')
    for j, label in enumerate(STEPS):
        x = 79 + 318*j
        d.rounded_rectangle((x, 223, x+293, 285), radius=16,
                            fill='#11616B' if j == s else '#153A4D',
                            outline=accent if j == s else '#426172', width=3 if j == s else 1)
        d.text((x+23, 230), f'{j+1:02d}  {label}', font=f(29), fill='#FFFFFF')
    d.rounded_rectangle((65, 314, 1015, 922), radius=22, fill='#F5F7F8', outline=accent, width=4)
    toolbar = screenshot.crop((58, 50, 1550, 150)).resize((920, 67))
    page = screenshot.crop((352, 276, 1200, 665)).resize((920, 500))
    im.paste(toolbar, (80, 333))
    im.paste(page, (80, 404))
    d = ImageDraw.Draw(im)
    # The active section is emphasized without modifying the actual UI capture.
    y = (535, 600, 670)[s]
    d.rounded_rectangle((154, y, 938, y+63), radius=13, outline=accent, width=6)
    d.rounded_rectangle((77, 956, 1003, 1083), radius=20, fill='#0A4252')
    notes = ('指示を文書として残す', '次の作業で内容を使い回す', '数値・条件は人が最終確認')
    d.text((108, 973), notes[s], font=f(36), fill='#FFFFFF')
    d.rounded_rectangle((80, 1115, 1000, 1127), radius=6, fill='#295268')
    d.rounded_rectangle((80, 1115, 80 + int(920*(i+1)/COUNT), 1127), radius=6, fill=accent)
    d.text((81, 1142), '実アプリ静止画 / 架空データ / REVIEW ONLY', font=f(23), fill='#B7D1DC')
    return im

def frames(screenshot, directory, genre='ai_work'):
    directory = Path(directory); directory.mkdir(parents=True, exist_ok=True)
    for i in range(COUNT):
        render_frame(i, screenshot, genre).save(directory / f'frame_{i:03d}.png')

def compose(source, screenshot, output, work, genre='ai_work'):
    source, output = Path(source), Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    folder = Path(work) / 'frames'; frames(screenshot, folder, genre)
    cmd = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', str(source),
           '-framerate', '30', '-start_number', '0', '-i', str(folder/'frame_%03d.png'),
           '-filter_complex', f'[1:v]setpts=PTS+{START/FPS:.9f}/TB[insert];[0:v][insert]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
           '-map', '[v]', '-map', '0:a:0', '-c:v', 'libx264', '-preset', 'veryfast',
           '-crf', '19', '-pix_fmt', 'yuv420p', '-r', '30', '-c:a', 'copy',
           '-movflags', '+faststart', str(output)]
    subprocess.run(cmd, check=True)

def smoke():
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        fake = Image.new('RGB', (1600, 900), 'white')
        ImageDraw.Draw(fake).text((400, 400), 'SYNTHETIC CI ONLY', fill='black')
        for i in range(15): render_frame(i, fake).save(root/f'frame_{i:03d}.png')
        mp4 = root/'synthetic.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
          '-framerate','30','-i',str(root/'frame_%03d.png'),
          '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=0.5',
          '-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast',
          '-pix_fmt','yuv420p','-c:a','aac',str(mp4)],check=True)
        data=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(mp4)]))
        assert {x['codec_name'] for x in data['streams']} == {'h264','aac'}
        subprocess.run(['ffmpeg','-v','error','-i',str(mp4),'-f','null','-'],check=True)
        print('PASS synthetic CI H264/AAC decode; private MP4 not tested in CI')

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source'); p.add_argument('--screenshot'); p.add_argument('--out'); p.add_argument('--work')
    p.add_argument('--genre', default='ai_work'); p.add_argument('--smoke', action='store_true')
    a=p.parse_args()
    if a.smoke: smoke()
    else: compose(a.source,a.screenshot,a.out,a.work,a.genre)
