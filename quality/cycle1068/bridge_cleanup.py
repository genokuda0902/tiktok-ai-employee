"""Original scene-safe bridge cleanup for ten genres. REVIEW ONLY; no publishing.

Cleans only identified stale-composite residue in scene-specific lower gaps,
leaving intentional labels and CTAs intact. Subtitle/audio region y>=1460 is untouched.
Does not alter narration, subtitles, or assert ASR/semantic accuracy.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1080, 1920, 30
BRIDGE_Y, BRIDGE_H = 1080, 380
# None means scene has purposeful lower content and must remain unmodified.
CLEAN_START = (1160, None, 1250, 1270, 1260, None, 1260, None)
SCENES = (
    (0.000, 2.900, '課題を見つける'),
    (2.900, 5.800, '作業を書き出す'),
    (5.800, 8.520, '見本を用意する'),
    (8.520, 11.400, '指示を具体化する'),
    (11.400, 14.280, '出力を検算する'),
    (14.280, 17.340, '修正点を伝える'),
    (17.340, 20.300, '指示を保存する'),
    (20.300, 23.033333, '習慣にしていく'),
)
PALETTES = {
    'ai_work':'#21D7CB','finance':'#EDBE68','education':'#7FAEFF',
    'health':'#7DD6AC','travel':'#F4A9B8','beauty':'#D6A4F7',
    'food':'#FFAB75','career':'#6ED1E9','productivity':'#B8DF74',
    'lifestyle':'#F1C37B',
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
REG='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def scene_at(t):
    for i,(a,b,_) in enumerate(SCENES):
        if a <= t < b: return i
    raise ValueError('timestamp outside scene range')


def render_panel(index, genre='ai_work'):
    if genre not in PALETTES: raise ValueError('unsupported genre')
    if not 0 <= index < len(SCENES): raise ValueError('unsupported scene')
    accent=PALETTES[genre]
    im=Image.new('RGBA',(W,BRIDGE_H),(0,0,0,0))
    if CLEAN_START[index] is None:
        return im
    d=ImageDraw.Draw(im)
    top=CLEAN_START[index]-BRIDGE_Y
    # Fill only the scene-specific residual strip. No occlusion of valid main UI.
    d.rectangle((0,top,W,BRIDGE_H),fill=(5,18,31,255))
    d.rounded_rectangle((36,top+15,1044,BRIDGE_H-18),radius=19,
                        fill='#0B293B',outline='#31556A',width=2)
    d.rounded_rectangle((55,top+32,200,top+85),radius=11,fill=accent)
    label=ImageFont.truetype(FONT,24)
    title=ImageFont.truetype(FONT,32)
    small=ImageFont.truetype(REG,22)
    d.text((75,top+42),f'{index+1:02d}/08',font=label,fill='#082433')
    d.text((226,top+36),SCENES[index][2],font=title,fill='#F5FBFF')
    y=top+110
    for j in range(8):
        x=55+j*121
        d.rounded_rectangle((x,y,x+103,y+10),radius=4,
                            fill=accent if j<=index else '#375265')
    note='説明用の架空データ / 公開前レビュー' if index in (2,4) else '公開前レビュー用 / 実績の保証ではありません'
    d.text((55,BRIDGE_H-63),note,font=small,fill='#A7C2D1')
    return im


def inspect_video(path):
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    vs=next(s for s in info['streams'] if s['codec_type']=='video')
    aud=next(s for s in info['streams'] if s['codec_type']=='audio')
    return {'width':vs['width'],'height':vs['height'],'fps':vs['r_frame_rate'],
            'video_codec':vs['codec_name'],'audio_codec':aud['codec_name'],
            'duration_s':float(info['format']['duration'])}


def compose(source, out, expected_sha, genre='ai_work'):
    if genre not in PALETTES: raise ValueError('unsupported genre')
    if sha256(source)!=expected_sha: raise ValueError('source sha256 mismatch (fail closed)')
    spec=inspect_video(source)
    if (spec['width'],spec['height'],spec['fps'],spec['video_codec'],spec['audio_codec']) != (W,H,'30/1','h264','aac'):
        raise ValueError('unexpected input stream format')
    with tempfile.TemporaryDirectory() as td:
        pngs=[]
        for i in range(len(SCENES)):
            p=Path(td)/f'bridge_{i:02d}.png'; render_panel(i,genre).save(p); pngs.append(p)
        cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source)]
        for p in pngs: cmd += ['-loop','1','-framerate',str(FPS),'-i',str(p)]
        chain=[]; last='0:v'
        for i,(a,b,_) in enumerate(SCENES):
            nxt=f'v{i}'
            chain.append(f'[{last}][{i+1}:v]overlay=x=0:y={BRIDGE_Y}:enable=\'gte(t,{a})*lt(t,{b})\':shortest=0:format=auto[{nxt}]')
            last=nxt
        Path(out).parent.mkdir(parents=True,exist_ok=True)
        cmd+=['-filter_complex',';'.join(chain),'-map',f'[{last}]','-map','0:a:0',
              '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p',
              '-r',str(FPS),'-frames:v',str(round(spec['duration_s']*FPS)),
              '-c:a','copy','-movflags','+faststart',str(out)]
        subprocess.run(cmd,check=True)
    return inspect_video(out)


def smoke():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); source=root/'source.mp4'; dest=root/'out.mp4'
        subprocess.run(['ffmpeg','-v','error','-y','-f','lavfi','-i',
                        'color=c=#081625:s=1080x1920:r=30:d=23.033333',
                        '-f','lavfi','-i','sine=frequency=440:sample_rate=48000:duration=23.033333',
                        '-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',
                        '-c:a','aac','-shortest',str(source)],check=True)
        info=compose(source,dest,sha256(source))
        assert info['video_codec']=='h264' and info['audio_codec']=='aac'
        subprocess.run(['ffmpeg','-v','error','-i',str(dest),'-f','null','-'],check=True)
        print('PASS synthetic 23.033s video, eight overlays, H264/AAC full decode')

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source');ap.add_argument('--out');ap.add_argument('--source-sha256')
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--smoke',action='store_true')
    args=ap.parse_args()
    if args.smoke: smoke()
    else: print(json.dumps(compose(args.source,args.out,args.source_sha256,args.genre),indent=2))
