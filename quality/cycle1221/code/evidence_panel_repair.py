#!/usr/bin/env python3
"""Review-only correction of a verified, overlapping evidence label in slide video.

Works on 10 genre labels and per-scene, rights-reviewed text specifications.
Does not transcribe speech, fetch external media, publish or merge.
"""
import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
FONT = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

@dataclass(frozen=True)
class Patch:
    genre: str = 'ai'
    scene: int = 3
    label: str = '計算の確認'
    expression: str = '9 + 14 + 21 = 44'
    x: int = 78
    y: int = 1060
    width: int = 766
    height: int = 87


def validate(spec: Patch, width=1080, height=1920):
    if spec.genre not in GENRES: raise ValueError('unsupported genre')
    if not 1 <= spec.scene <= 20: raise ValueError('invalid scene number')
    if not spec.label or not spec.expression: raise ValueError('reviewed text required')
    if any(c in spec.expression for c in '\n\r\t') or len(spec.expression)>42:
        raise ValueError('unsafe expression')
    if spec.x<0 or spec.y<0 or spec.width<300 or spec.height<65:
        raise ValueError('invalid patch rectangle')
    if spec.x+spec.width>width or spec.y+spec.height>height:
        raise ValueError('patch out of bounds')
    # Hard stop: do not cover narration subtitles or publication footer.
    if spec.y+spec.height>1190: raise ValueError('protected subtitle/footer zone')


def make_overlay(spec: Patch, target: Path, size=(1080,1920), font=FONT):
    validate(spec,*size)
    if not Path(font).is_file(): raise FileNotFoundError(font)
    im=Image.new('RGBA',size,(0,0,0,0))
    d=ImageDraw.Draw(im)
    x,y,w,h=spec.x,spec.y,spec.width,spec.height
    d.rounded_rectangle((x,y,x+w,y+h),radius=12,fill=(3,34,44,255),outline=(48,191,180,255),width=2)
    d.rectangle((x+2,y+10,x+8,y+h-10),fill=(64,216,198,255))
    label_font=ImageFont.truetype(font,23)
    expression_font=ImageFont.truetype(font,37)
    d.text((x+26,y+27),spec.label,font=label_font,fill=(196,229,227,255))
    text_x=x+248
    if d.textbbox((text_x,y),spec.expression,font=expression_font)[2] > x+w-18:
        raise ValueError('expression too wide for safe panel')
    d.text((text_x,y+18),spec.expression,font=expression_font,fill=(249,252,255,255))
    target.parent.mkdir(parents=True,exist_ok=True)
    im.save(target)
    return target


def run(cmd):
    p=subprocess.run(cmd,text=True,capture_output=True)
    if p.returncode: raise RuntimeError('ffmpeg/ffprobe error: '+p.stderr[-1800:])
    return p.stdout


def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))


def render(src: Path, dst: Path, spec: Patch, overlay: Path, report: Path, crf=18):
    src,dst,overlay,report=map(Path,(src,dst,overlay,report))
    if not src.is_file(): raise FileNotFoundError(src)
    if src.resolve()==dst.resolve(): raise ValueError('source/output must differ')
    original=probe(src)
    v=next(s for s in original['streams'] if s['codec_type']=='video')
    a=next(s for s in original['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'])!=(1080,1920) or v['codec_name']!='h264' or a['codec_name']!='aac':
        raise ValueError('requires 1080x1920 H.264 and AAC')
    chapters=original['chapters']
    if len(chapters)<spec.scene: raise ValueError('missing requested chapter')
    start=float(chapters[spec.scene-1]['start_time'])
    end=float(chapters[spec.scene-1]['end_time'])
    make_overlay(spec,overlay)
    dst.parent.mkdir(parents=True,exist_ok=True)
    filt=f"[0:v][1:v]overlay=0:0:format=auto:enable='gte(t,{start:.4f})*lt(t,{end:.4f})',format=yuv420p[v]"
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(src),'-loop','1','-i',str(overlay),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0','-map_chapters','0',
         '-c:v','libx264','-preset','veryfast','-crf',str(crf),'-pix_fmt','yuv420p',
         '-frames:v',str(v['nb_frames']),'-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart',str(dst)])
    output=probe(dst)
    ov=next(s for s in output['streams'] if s['codec_type']=='video')
    oa=next(s for s in output['streams'] if s['codec_type']=='audio')
    if ov['nb_frames']!=v['nb_frames'] or len(output['chapters'])!=len(chapters):
        raise RuntimeError(f'frame/chapter count changed: source {v.get("nb_frames")}/{len(chapters)} output {ov.get("nb_frames")}/{len(output["chapters"])} duration {output["format"].get("duration")}')
    if oa['codec_name']!='aac': raise RuntimeError('audio codec changed')
    result={'genre':spec.genre,'patch_scene':spec.scene,'scene_start':start,'scene_end':end,
            'verified_text':{'label':spec.label,'expression':spec.expression},
            'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
            'output_sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),
            'output_bytes':dst.stat().st_size,'width':ov['width'],'height':ov['height'],
            'frames':int(ov['nb_frames']),'chapters':len(output['chapters']),
            'video_codec':ov['codec_name'],'audio_codec':oa['codec_name'],
            'audio_language':oa.get('tags',{}).get('language'),
            'duration_seconds':float(output['format']['duration']),
            'independent_asr':'NOT VERIFIED','speech_caption_semantics':'NOT VERIFIED',
            'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    p.add_argument('--overlay',type=Path,required=True)
    p.add_argument('--report',type=Path,required=True)
    p.add_argument('--genre',choices=GENRES,default='ai')
    p.add_argument('--scene',type=int,default=3)
    p.add_argument('--label',default='計算の確認')
    p.add_argument('--expression',default='9 + 14 + 21 = 44')
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,Patch(genre=a.genre,scene=a.scene,label=a.label,
              expression=a.expression),a.overlay,a.report),ensure_ascii=False,indent=2))
