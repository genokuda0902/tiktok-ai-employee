"""Cycle1153: gentle edge sharpening confined to diagrams, not Japanese captions.

This generic image-slide finishing filter uses FFmpeg only, keeps AAC packets
bit-for-bit, and refuses to process a crop that overlaps the caption safe zone.
It does not claim ASR or publication readiness. No external media or network.
"""
from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path

GENRE_STRENGTH = {
    'ai-work': 0.52, 'finance': 0.42, 'career': 0.46,
    'health': 0.40, 'learning': 0.55, 'travel': 0.35,
    'technology': 0.52, 'business': 0.48, 'life': 0.40,
    'history': 0.42,
}
DEFAULT_ROI = (64, 460, 952, 840)
DEFAULT_CAPTION_TOP = 1350

def probe(path: str) -> dict:
    result = subprocess.run(['ffprobe','-v','error','-show_streams','-show_format',
                             '-of','json',str(path)],check=True,capture_output=True,text=True)
    return json.loads(result.stdout)

def validate_roi(roi, width, height, caption_top):
    x,y,w,h = roi
    if any(v < 0 for v in (x,y)) or w <= 0 or h <= 0:
        raise ValueError('ROI must have positive width and height')
    if x+w > width or y+h > height:
        raise ValueError('ROI outside video')
    if y+h > caption_top:
        raise ValueError('ROI overlaps protected Japanese caption area')
    return True

def filtergraph(roi, strength):
    x,y,w,h = roi
    if not (0 <= strength <= 1):
        raise ValueError('Strength must be 0..1')
    # Chroma sharpening disabled to avoid false-color halos on thin UI text.
    return (f'[0:v]split=2[untouched][diagram];'
            f'[diagram]crop={w}:{h}:{x}:{y},'
            f'unsharp=5:5:{strength:.2f}:5:5:0[detail];'
            f'[untouched][detail]overlay={x}:{y}:format=auto,'
            'format=yuv420p[v]')

def render(source, output, genre='ai-work', roi=DEFAULT_ROI,
           caption_top=DEFAULT_CAPTION_TOP, preset='veryfast'):
    if genre not in GENRE_STRENGTH:
        raise ValueError('Unknown genre')
    info = probe(source)
    video = next(s for s in info['streams'] if s['codec_type']=='video')
    width,height = video['width'],video['height']
    validate_roi(roi,width,height,caption_top)
    audio = next((s for s in info['streams'] if s['codec_type']=='audio'),None)
    if audio is None:
        raise ValueError('Japanese narration audio stream required')
    output = Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    cmd = ['ffmpeg','-hide_banner','-loglevel','error','-y',
           '-i',str(source),'-filter_complex',filtergraph(roi,GENRE_STRENGTH[genre]),
           '-map','[v]','-map','0:a:0','-map_metadata','0',
           '-c:v','libx264','-preset',preset,'-crf','18','-pix_fmt','yuv420p',
           '-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'source':str(source),'output':str(output),'genre':genre,
            'roi':list(roi),'protected_caption_top':caption_top,
            'strength':GENRE_STRENGTH[genre],'genres_supported':len(GENRE_STRENGTH),
            'asr_verified':False,'human_review_required':True}

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True)
    p.add_argument('--output',required=True)
    p.add_argument('--genre',default='ai-work',choices=GENRE_STRENGTH)
    p.add_argument('--roi',default=','.join(map(str,DEFAULT_ROI)))
    p.add_argument('--caption-top',type=int,default=DEFAULT_CAPTION_TOP)
    p.add_argument('--preset',default='veryfast')
    p.add_argument('--report')
    args=p.parse_args()
    report=render(args.source,args.output,args.genre,
                  tuple(map(int,args.roi.split(','))),args.caption_top,args.preset)
    if args.report: Path(args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False))
