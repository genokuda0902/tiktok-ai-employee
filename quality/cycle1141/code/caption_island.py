"""Review-only, zero-cost caption-island stabilizer for 10 TikTok genres.
Composites the unzoomed subtitle band over the moving background.
No transcription, posting, paid API, or private-media upload.
"""
from __future__ import annotations
import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image

GENRES = ('ai_workflow', 'business', 'finance', 'health', 'beauty',
          'travel', 'education', 'lifestyle', 'technology', 'entertainment')
WIDTH, HEIGHT, FPS = 1080, 1920, 30
CROP_TOP, LOCK_TOP = 1220, 1350

def alpha_at(y, crop_top=CROP_TOP, lock_top=LOCK_TOP):
    if lock_top <= crop_top:
        raise ValueError('lock_top must be greater than crop_top')
    return round(255 * max(0., min(1., (y-crop_top)/(lock_top-crop_top))))

def make_mask(path, crop_top=CROP_TOP, lock_top=LOCK_TOP,
              width=WIDTH, height=HEIGHT):
    if not (0 < crop_top < lock_top < height):
        raise ValueError('Invalid subtitle safe-area bounds')
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    im = Image.new('L', (width, height-crop_top))
    for y in range(height-crop_top):
        im.paste(alpha_at(crop_top+y, crop_top, lock_top),
                 (0,y,width,y+1))
    im.save(path)
    return path

def probe(path):
    data = json.loads(subprocess.check_output([
        'ffprobe','-v','error','-show_streams','-show_format',
        '-of','json',str(path)], text=True))
    v = next(s for s in data['streams'] if s['codec_type']=='video')
    a = next(s for s in data['streams'] if s['codec_type']=='audio')
    return {'width':int(v['width']), 'height':int(v['height']),
            'fps':v['avg_frame_rate'],
            'frames':int(v.get('nb_frames',round(float(data['format']['duration'])*FPS))),
            'duration':float(data['format']['duration']),
            'audio_codec':a['codec_name'],
            'audio_sample_rate':int(a['sample_rate'])}

def validate_pair(moving, stable):
    a,b = probe(moving),probe(stable)
    for s in (a,b):
        if (s['width'],s['height'],s['fps']) != (WIDTH,HEIGHT,'30/1'):
            raise ValueError('Both videos must be 1080x1920/30fps')
        if (s['audio_codec'],s['audio_sample_rate']) != ('aac',48000):
            raise ValueError('AAC/48kHz required')
    if a['frames'] != b['frames'] or abs(a['duration']-b['duration']) > .02:
        raise ValueError('Source frame alignment mismatch')
    return a

def render(moving, stable, output, genre='ai_workflow',
           crop_top=CROP_TOP, lock_top=LOCK_TOP):
    if genre not in GENRES:
        raise ValueError('Unsupported genre')
    moving,stable,output = Path(moving),Path(stable),Path(output)
    if not moving.is_file() or not stable.is_file():
        raise FileNotFoundError('Both MP4 inputs required')
    source = validate_pair(moving,stable)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='caption_island_') as tmp:
        mask=make_mask(Path(tmp)/'feather.png',crop_top,lock_top)
        h=HEIGHT-crop_top
        graph=(f'[1:v]crop={WIDTH}:{h}:0:{crop_top},format=rgb24[cap];'
               '[2:v]format=gray[mask];'
               '[cap][mask]alphamerge[island];'
               f'[0:v][island]overlay=0:{crop_top}:format=auto:shortest=1,'
               'format=yuv420p[v]')
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',
             '-i',str(moving),'-i',str(stable),
             '-loop','1','-framerate',str(FPS),'-i',str(mask),
             '-filter_complex',graph,'-map','[v]','-map','0:a:0',
             '-c:v','libx264','-preset','veryfast','-crf','20',
             '-threads','4','-pix_fmt','yuv420p','-r',str(FPS),
             '-frames:v',str(source['frames']),'-c:a','copy',
             '-map_metadata','0','-map_chapters','0',
             '-movflags','+faststart',str(output)]
        subprocess.run(cmd,check=True)
    return {'genre':genre,'frames':source['frames'],
            'subtitle_meaning':'NOT VERIFIED',
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('moving')
    p.add_argument('stable')
    p.add_argument('output')
    p.add_argument('--genre',choices=GENRES,default='ai_workflow')
    a=p.parse_args()
    print(json.dumps(render(a.moving,a.stable,a.output,a.genre),indent=2))
