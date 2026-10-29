"""Fail-closed action-aware focus cue renderer for REVIEW-ONLY vertical videos.

Highlights manually verified actions in an existing, locally held MP4.
Does not infer truth, use external assets, transcribe speech, or approve publication.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import argparse
import hashlib
import json
import subprocess

GENRES = ('ai_work','finance','business','education','lifestyle','health','travel','food','technology','career')
WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 691
CONTENT_BOTTOM = 1440  # lower Japanese burned-in captions are protected

@dataclass(frozen=True)
class Beat:
    start: float
    end: float
    rect: tuple[int,int,int,int]
    label: str  # metadata only; never drawn on frames

    def validate(self):
        x,y,w,h = self.rect
        if not (0 <= x < WIDTH and 0 <= y < CONTENT_BOTTOM and 30 <= w <= WIDTH-x and 30 <= h <= CONTENT_BOTTOM-y):
            raise ValueError('focus rect overlaps protected captions or exceeds frame')
        if not (0 <= self.start < self.end <= FRAMES/FPS and 0.2 <= self.end-self.start <= 4.0):
            raise ValueError('invalid focus beat duration')
        if not self.label or len(self.label)>50: raise ValueError('invalid metadata label')

@dataclass(frozen=True)
class FocusSpec:
    genre: str
    source_sha256: str
    beats: tuple[Beat,...]

    def validate(self):
        if self.genre not in GENRES: raise ValueError('unsupported genre')
        if len(self.source_sha256)!=64 or any(c not in '0123456789abcdef' for c in self.source_sha256):
            raise ValueError('expected sha256 required')
        if not (1 <= len(self.beats) <= 8): raise ValueError('1-8 focus beats required')
        last_end = -1.
        for b in self.beats:
            b.validate()
            if b.start < last_end: raise ValueError('beats must be chronological and nonoverlapping')
            last_end = b.end

def sha256(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def video_info(path:Path)->dict:
    r=subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type,codec_name,width,height,avg_frame_rate,sample_rate,channels,nb_frames','-show_entries','format=duration','-of','json',str(path)],capture_output=True,text=True,check=True)
    return json.loads(r.stdout)

def validate_source(path:Path,spec:FocusSpec):
    spec.validate()
    if sha256(path)!=spec.source_sha256:raise ValueError('source SHA mismatch; refuse to render')
    streams=video_info(path)['streams']; v=next((s for s in streams if s['codec_type']=='video'),None)
    a=next((s for s in streams if s['codec_type']=='audio'),None)
    if not v or (v.get('width'),v.get('height'),v.get('avg_frame_rate'),int(v.get('nb_frames','0')))!=(WIDTH,HEIGHT,'30/1',FRAMES):
        raise ValueError('unexpected source video geometry/frame count')
    if not a or a.get('codec_name')!='aac' or a.get('sample_rate')!='48000':
        raise ValueError('expected AAC 48kHz narration track')

def video_filter(spec:FocusSpec)->str:
    spec.validate()
    filters=[]
    for b in spec.beats:
        x,y,w,h=b.rect
        en=f'between(t,{b.start:.3f},{b.end:.3f})'
        filters.append(f"drawbox=x={x-8 if x>=8 else x}:y={y-8 if y>=8 else y}:w={w+16 if x>=8 and x+w+8<=WIDTH else w}:h={h+16 if y>=8 and y+h+8<=CONTENT_BOTTOM else h}:color=0x21d7c5@0.26:t=10:enable='{en}'")
        filters.append(f"drawbox=x={x}:y={y}:w={w}:h={h}:color=0x7dffe8@0.88:t=5:enable='{en}'")
    return ','.join(filters)

def render(source:Path,output:Path,spec:FocusSpec)->dict:
    validate_source(source,spec)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',video_filter(spec),'-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode:raise RuntimeError('ffmpeg render failed: '+r.stderr[-2000:])
    return {'input_sha256':spec.source_sha256,'output_sha256':sha256(output),'genre':spec.genre,
            'beats':[{'start':b.start,'end':b.end,'rect':b.rect,'label':b.label} for b in spec.beats],
            'audio':'stream copy; not independently transcribed','publication_approved':False}

# Geometry and timings are verified for the cycle948 fictional Calc example ONLY.
# Other genres must provide a separate, human-reviewed FocusSpec.
def reviewed_ai_work_spec(source_sha:str)->FocusSpec:
    return FocusSpec('ai_work',source_sha,(
        Beat(11.95,12.98,(384,738,306,98),'highlight source cell as manual input changes'),
        Beat(13.00,14.36,(861,1072,150,138),'verify recalculated total in source'),
    ))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--source-sha256',required=True)
    p.add_argument('--output',required=True);p.add_argument('--qa',required=True)
    a=p.parse_args(); report=render(Path(a.source),Path(a.output),reviewed_ai_work_spec(a.source_sha256))
    Path(a.qa).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
