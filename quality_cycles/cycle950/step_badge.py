"""Offline chapter badge for a fixed 23.033s 9:16 image-slide demo.
No network, posting, new captions or narration. Review only.
"""
from dataclasses import dataclass
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont

FPS=30
WIDTH,HEIGHT=1080,1920
FRAME_COUNT=691
BADGE_X,BADGE_Y=750,34
BADGE_W,BADGE_H=320,130
SCENE_EDGES=(0,87,174,261,348,435,522,609,691)
GENRE_ACCENTS={
    'ai_productivity':'#35d0c0','business':'#59b7e5',
    'education':'#f0b95b','finance':'#71c9a3',
    'technology':'#7cc8ff','lifestyle':'#ffb5b7',
    'health':'#6ed8c6','travel':'#edbd77',
    'food':'#e8a474','entertainment':'#b6a1f2',
}

@dataclass(frozen=True)
class BadgeConfig:
    genre: str='ai_productivity'
    frame_count: int=FRAME_COUNT
    def validate(self):
        if self.genre not in GENRE_ACCENTS:
            raise ValueError('unsupported genre; fail closed')
        if self.frame_count != FRAME_COUNT:
            raise ValueError('unexpected frame count; source-specific geometry')
        if BADGE_X<0 or BADGE_Y<0 or BADGE_X+BADGE_W>WIDTH or BADGE_Y+BADGE_H>250:
            raise ValueError('badge must stay in top-right safe region')

def scene_for_frame(frame):
    if not 0<=frame<FRAME_COUNT:
        raise ValueError('frame outside known source')
    for i in range(8):
        if SCENE_EDGES[i]<=frame<SCENE_EDGES[i+1]:
            return i+1,(frame-SCENE_EDGES[i])/(SCENE_EDGES[i+1]-SCENE_EDGES[i])
    raise AssertionError('unreachable')

def font(size,bold=False):
    base='/usr/share/fonts/opentype/noto/'
    candidates=[base+('NotoSansCJK-Bold.ttc' if bold else 'NotoSansCJK-Regular.ttc'),
                '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']
    for path in candidates:
        try: return ImageFont.truetype(path,size)
        except OSError: pass
    return ImageFont.load_default()

def render_badge(frame,genre='ai_productivity'):
    BadgeConfig(genre).validate()
    scene,progress=scene_for_frame(frame)
    image=Image.new('RGBA',(BADGE_W,BADGE_H),(0,0,0,0))
    d=ImageDraw.Draw(image)
    accent=GENRE_ACCENTS[genre]
    d.rounded_rectangle((9,16,308,112),radius=22,
                        fill=(1,17,38,249),outline=accent,width=2)
    d.rounded_rectangle((24,32,32,68),radius=4,fill=accent)
    d.text((44,35),'STEP',font=font(20,True),fill=(176,209,223,255))
    d.text((143,27),f'{scene:02d} / 08',font=font(32,True),fill=(250,253,255,255))
    left,top,right=24,88,291
    d.rounded_rectangle((left,top,right,top+7),radius=3,fill=(54,77,100,255))
    active=left+max(4,int((right-left)*progress))
    d.rounded_rectangle((left,top,active,top+7),radius=3,fill=accent)
    return image

def render(source:Path,output:Path,genre='ai_productivity'):
    BadgeConfig(genre).validate()
    if not source.is_file(): raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-f','rawvideo','-pixel_format','rgba','-video_size',f'{BADGE_W}x{BADGE_H}',
         '-framerate',str(FPS),'-i','pipe:0',
         '-filter_complex',f'[0:v][1:v]overlay={BADGE_X}:{BADGE_Y}:shortest=1:format=auto[v]',
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','17','-pix_fmt','yuv420p','-r',str(FPS),'-fps_mode','cfr',
         '-frames:v',str(FRAME_COUNT),'-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
    try:
        for f in range(FRAME_COUNT): proc.stdin.write(render_badge(f,genre).tobytes())
        proc.stdin.close()
        code=proc.wait()
        if code: raise RuntimeError(f'ffmpeg failed: {code}')
    except BaseException:
        if proc.stdin and not proc.stdin.closed: proc.stdin.close()
        proc.kill()
        proc.wait()
        raise
    return output

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('source',type=Path)
    parser.add_argument('output',type=Path)
    parser.add_argument('--genre',choices=GENRE_ACCENTS,default='ai_productivity')
    args=parser.parse_args()
    render(args.source,args.output,args.genre)
