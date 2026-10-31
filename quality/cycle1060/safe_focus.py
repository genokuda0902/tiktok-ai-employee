"""Cycle1060: readable Writer focus rail without covering Japanese source text.

REVIEW ONLY. Requires local genuine, sanitized Writer screenshot and private
approved-for-review source MP4. Does not assert rights or publication approval.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from quality.cycle1058.real_writer_focus import (render_frame as prior_render,
    PALETTES, W, H, FPS, START, COUNT, stage)

# Page text begins around x=150; rail remains in the blank left margin.
RAIL_X = (106, 129)
RAIL_CENTERS = (510, 573, 636)
PROTECTED_TEXT = (150, 440, 938, 765)

def render_frame(i, screenshot, genre='ai_work'):
    if genre not in PALETTES:
        raise ValueError('unknown/unapproved genre')
    src = Image.open(screenshot).convert('RGB') if not isinstance(screenshot, Image.Image) else screenshot.convert('RGB')
    if src.width < 1400 or src.height < 800:
        raise ValueError('1600x900 sanitized app screenshot required')
    base = prior_render(i, src, genre)
    # Restore *unaltered* application pixels after removing previous outline.
    page = src.crop((352, 276, 1200, 665)).resize((920, 500))
    base.paste(page, (80, 404))
    draw = ImageDraw.Draw(base)
    y = RAIL_CENTERS[stage(i)]
    # Mark active line in the left whitespace, never on top of source text.
    draw.rounded_rectangle((RAIL_X[0], y-25, RAIL_X[1], y+25),
                           radius=9, fill=PALETTES[genre])
    return base

def compose(source, screenshot, out, work, genre='ai_work'):
    source, out = Path(source), Path(out)
    if not source.is_file(): raise FileNotFoundError(source)
    if not Path(screenshot).is_file(): raise FileNotFoundError(screenshot)
    if genre not in PALETTES: raise ValueError('unapproved genre')
    folder=Path(work)/'frames'; folder.mkdir(parents=True,exist_ok=True)
    src=Image.open(screenshot).convert('RGB')
    for i in range(COUNT):
        render_frame(i,src,genre).save(folder/f'frame_{i:03d}.png')
    out.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
        '-framerate',str(FPS),'-start_number','0','-i',str(folder/'frame_%03d.png'),
        '-filter_complex',f'[1:v]setpts=PTS+{START/FPS:.9f}/TB[insert];[0:v][insert]overlay=0:0:eof_action=pass:shortest=0:format=auto[v]',
        '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
        '-crf','19','-pix_fmt','yuv420p','-r',str(FPS),'-c:a','copy',
        '-movflags','+faststart',str(out)],check=True)

def smoke():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d); s=Image.new('RGB',(1600,900),'white')
        for i in range(15): render_frame(i,s).save(p/f'f_{i:03d}.png')
        out=p/'synthetic.mp4'
        subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-framerate','30','-i',str(p/'f_%03d.png'),
            '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=0.5',
            '-map','0:v','-map','1:a','-c:v','libx264','-preset','ultrafast',
            '-pix_fmt','yuv420p','-c:a','aac',str(out)],check=True)
        streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-of','json',str(out)]))['streams']
        assert {x['codec_name'] for x in streams}=={'h264','aac'}
        subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
        print('PASS synthetic H264/AAC only; private 23s MP4 NOT tested in CI')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--source');ap.add_argument('--screenshot');ap.add_argument('--out');ap.add_argument('--work');ap.add_argument('--genre',default='ai_work');ap.add_argument('--smoke',action='store_true');a=ap.parse_args()
    if a.smoke: smoke()
    else: compose(a.source,a.screenshot,a.out,a.work,a.genre)
