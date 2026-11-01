#!/usr/bin/env python3
"""Review-only scene-caption track for a private Japanese MP4.

Adds a selectable mov_text subtitle track and writes a scene-caption
SRT for manual comparison. Captions are transcribed from *visible on-screen text*,
not independently recognized from audio. This is NOT a speech alignment verdict.
Some MP4 players automatically mark/show the sole subtitle track as default.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SCENE_CAPTIONS = [
    (0.0, 2.9, 'AIで仕事を早くするなら、最初の一歩が大事。'),
    (2.9, 5.8, 'まず、繰り返している作業を書き出そう。'),
    (5.8, 8.7, '次に、完成形の見本を用意する。'),
    (8.7, 11.6, '指示は、目的と条件を具体的に伝える。'),
    (11.6, 14.3, '最初の出力は、必ず自分で確かめる。'),
    (14.3, 17.333333, '違いがあれば、修正点を一つずつ伝える。'),
    (17.333333, 20.3, '使える指示は、テンプレートに残す。'),
    (20.3, 23.033333, '小さな時短を、毎日の習慣にしよう。'),
]
GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for part in iter(lambda:f.read(1024*1024), b''):
            h.update(part)
    return h.hexdigest()


def run(cmd: list[str]) -> str:
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def probe(path: Path) -> dict:
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def ms(t: float) -> str:
    n=round(t*1000)
    return f'{n//3600000:02}:{n//60000%60:02}:{n//1000%60:02},{n%1000:03}'


def validate_cues(cues, duration: float) -> None:
    if not cues: raise ValueError('no captions')
    prev=0.0
    for start,end,txt in cues:
        if not (0 <= start < end <= duration+0.035): raise ValueError('cue outside duration')
        if abs(start-prev)>0.04: raise ValueError('gap or overlap in scene captions')
        if end-start < 0.7: raise ValueError('too-short caption')
        if not txt or len(txt)>38 or '\n' in txt: raise ValueError('caption text too long/empty')
        if len(txt)/(end-start)>18: raise ValueError('caption reading speed too high')
        if re.search(r'[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}',txt): raise ValueError('email in caption')
        if re.search(r'0\d{1,3}-?\d{3,4}-?\d{4}',txt): raise ValueError('possible phone number in caption')
        prev=end
    if abs(prev-duration)>0.05: raise ValueError('captions do not cover full video')


def make_srt(cues) -> str:
    return '\n'.join(f'{i}\n{ms(start)} --> {ms(end)}\n{txt}\n' for i,(start,end,txt) in enumerate(cues,1))


def validate_media(info:dict, expected_size=(1080,1920), expected_fps=30) -> tuple[float,int]:
    streams=info['streams']; v=[s for s in streams if s['codec_type']=='video']; a=[s for s in streams if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or v[0]['codec_name']!='h264' or a[0]['codec_name']!='aac': raise ValueError('unexpected streams')
    if (v[0]['width'],v[0]['height'])!=expected_size: raise ValueError('wrong dimensions')
    fps=v[0]['avg_frame_rate'].split('/'); rate=float(fps[0])/float(fps[1])
    if abs(rate-expected_fps)>0.02: raise ValueError('wrong frame rate')
    if int(a[0]['sample_rate'])!=48000: raise ValueError('wrong audio rate')
    return float(info['format']['duration']),int(v[0].get('nb_frames',round(float(info['format']['duration'])*rate)))


def stream_hash(path:Path, selector:str, fmt:str)->str:
    p=subprocess.run(['ffmpeg','-v','error','-i',str(path),'-map',selector,'-c','copy','-f',fmt,'-'],check=True,capture_output=True)
    return hashlib.sha256(p.stdout).hexdigest()


def build(source:Path, target:Path, srt:Path, report:Path, expected_sha:str, cues=SCENE_CAPTIONS, size=(1080,1920), fps=30):
    source=source.resolve();target=target.resolve();srt=srt.resolve();report=report.resolve()
    if len({source,target,srt,report})!=4: raise ValueError('paths must be distinct')
    if any(p.exists() for p in (target,srt,report)): raise FileExistsError('refuse to overwrite existing outputs')
    if sha256(source)!=expected_sha: raise ValueError('source SHA256 mismatch')
    dur,frames=validate_media(probe(source),size,fps)
    validate_cues(cues,dur)
    srt.parent.mkdir(parents=True,exist_ok=True);target.parent.mkdir(parents=True,exist_ok=True)
    srt.write_text(make_srt(cues),encoding='utf-8')
    try:
        subprocess.run(['ffmpeg','-y','-v','error','-i',str(source),'-i',str(srt),'-map','0:v:0','-map','0:a:0','-map','1:0','-c:v','copy','-c:a','copy','-c:s','mov_text','-metadata:s:s:0','language=jpn','-disposition:s:0','0','-movflags','+faststart',str(target)],check=True)
        result=probe(target)
        if len([s for s in result['streams'] if s['codec_type']=='subtitle'])!=1: raise RuntimeError('missing subtitle stream')
        if stream_hash(source,'0:v:0','h264')!=stream_hash(target,'0:v:0','h264'): raise RuntimeError('video stream changed')
        if stream_hash(source,'0:a:0','adts')!=stream_hash(target,'0:a:0','adts'): raise RuntimeError('audio stream changed')
        subprocess.run(['ffmpeg','-v','error','-i',str(target),'-map','0:v:0','-map','0:a:0','-f','null','-'],check=True,capture_output=True)
        extracted=run(['ffmpeg','-v','error','-i',str(target),'-map','0:s:0','-f','srt','-'])
        for _,_,txt in cues:
            if txt not in extracted: raise RuntimeError('subtitle roundtrip text mismatch')
        report_data={'source_sha256':expected_sha,'output_sha256':sha256(target),'srt_sha256':sha256(srt),'duration':dur,'frames':frames,'video':'H264 stream identical','audio':'AAC stream identical, Japanese content NOT ASR verified','subtitle_track':'mov_text jpn (player may default-enable)' ,'subtitle_default_flag':next(s.get('disposition',{}).get('default',0) for s in result['streams'] if s['codec_type']=='subtitle'),'double_caption_risk':'MP4 may auto-show soft track over existing burned-in captions','cues':len(cues),'decode':'PASS','speech_semantic_alignment':'NOT VERIFIED','publication':'NOT APPROVED'}
        report.write_text(json.dumps(report_data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return report_data
    except Exception:
        target.unlink(missing_ok=True)
        srt.unlink(missing_ok=True)
        raise


def main():
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--srt',type=Path,required=True);p.add_argument('--report',type=Path,required=True);p.add_argument('--source-sha',required=True);p.add_argument('--genre',choices=GENRES,default='ai');a=p.parse_args()
    print(json.dumps(build(a.source,a.out,a.srt,a.report,a.source_sha),ensure_ascii=False,indent=2))
if __name__=='__main__': main()
