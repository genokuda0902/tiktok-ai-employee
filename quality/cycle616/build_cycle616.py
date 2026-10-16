"""Render existing scene card above the provisional organic UI caption region.
No uploads, no paid API, no publishing. Rights and human quality review pending.
Requires ffmpeg, Pillow, source MP4 and 10-genre JSON from the ZIP.
"""
import argparse,json,subprocess,tempfile
from pathlib import Path
from layout import BG_START,CROP,DEST,SAFE_BOTTOM,make_plate,make_mask
ROOT=Path(__file__).resolve().parent
def render(source,output,genre='雑学・科学'):
    source,output=Path(source),Path(output)
    cfg=json.loads((ROOT/'assets/genres.json').read_text(encoding='utf8'))['genres']
    if len(cfg)!=10 or genre not in cfg:raise ValueError('10-genre configuration required')
    if not source.exists():raise FileNotFoundError(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    bg=output.parent/'safezone_clean_plate.png'
    mask=output.parent/'card_alpha_mask.png'
    make_plate(bg);make_mask(mask)
    w,h=CROP[2]-CROP[0],CROP[3]-CROP[1]
    graph=('[0:v]split=2[original][card_src];'
        f'[card_src]crop={w}:{h}:{CROP[0]}:{CROP[1]},format=rgba[card_rgba];'
        '[2:v]format=gray[mask];[card_rgba][mask]alphamerge[card];'
        f'[original][1:v]overlay=0:{BG_START}:shortest=1[clean];'
        f'[clean][card]overlay={DEST[0]}:{DEST[1]}:shortest=1,format=yuv420p[v]')
    def run(args):
        subprocess.run(args,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=240)
    with tempfile.TemporaryDirectory() as td:
        silent=Path(td)/'silent.mp4'
        run(['ffmpeg','-v','error','-y','-i',str(source),
          '-loop','1','-framerate','30','-i',str(bg),
          '-loop','1','-framerate','30','-i',str(mask),
          '-filter_complex',graph,'-map','[v]','-an',
          '-c:v','libx264','-preset','veryfast','-crf','17',
          '-r','30','-frames:v','468',str(silent)])
        run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(source),
          '-map','0:v:0','-map','1:a:0','-c','copy','-movflags','+faststart',str(output)])
    return {'status':'HUMAN_REVIEW','publication':'NOT_APPROVED','genre':genre,
            'safe_bottom_y':SAFE_BOTTOM,'card_bottom_y':DEST[1]+h}
if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--input',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='雑学・科学')
    args=p.parse_args()
    print(json.dumps(render(args.input,args.output,args.genre),ensure_ascii=False))
