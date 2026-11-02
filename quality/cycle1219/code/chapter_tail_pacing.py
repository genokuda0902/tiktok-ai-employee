#!/usr/bin/env python3
"""Review-only silence-tail pacing optimizer; no external assets or publishing."""
import argparse
import json
import math
import re
import subprocess
from pathlib import Path

GENRES = ('ai','business','money','learning','health','food','travel','beauty','career','life')
NOISE_DB = -45
MIN_TAIL_SECONDS = 0.45
POSTROLL_SECONDS = 0.20
MIN_SAVED_SECONDS = 0.10

def call(args, check=True):
    p = subprocess.run(args, text=True, capture_output=True)
    if check and p.returncode:
        raise RuntimeError(f'command failed {p.returncode}: {p.stderr[-2000:]}')
    return p

def probe(path):
    return json.loads(call(['ffprobe','-v','error','-show_format','-show_streams',
                            '-show_chapters','-of','json',str(path)]).stdout)

def detect_silences(path, noise_db=NOISE_DB, min_duration=0.2):
    p = call(['ffmpeg','-hide_banner','-nostats','-i',str(path),'-vn','-af',
              f'silencedetect=noise={noise_db}dB:d={min_duration}', '-f','null','-'])
    starts, spans = [], []
    for line in p.stderr.splitlines():
        a = re.search(r'silence_start:\s*([\d.]+)', line)
        if a:
            starts.append(float(a.group(1)))
        b = re.search(r'silence_end:\s*([\d.]+)', line)
        if b and starts:
            spans.append((starts.pop(0),float(b.group(1))))
    return spans

def calculate_cut(duration, fps, spans, last_chapter_start=0.0,
                  min_tail=MIN_TAIL_SECONDS, postroll=POSTROLL_SECONDS):
    if not spans:
        return duration, 'no_silence_detected'
    start, end = spans[-1]
    if end < duration - 0.1 or duration - start < min_tail:
        return duration, 'no_long_trailing_silence'
    target = math.ceil((start + postroll) * fps - 1e-7) / fps
    target = min(target, duration)
    if target - last_chapter_start < 1.0:
        return duration, 'protect_last_chapter'
    if duration - target < MIN_SAVED_SECONDS:
        return duration, 'savings_too_small'
    return target, 'trimmed_trailing_silence'

def optimize(source, output, report_path=None, genre='ai'):
    if genre not in GENRES:
        raise ValueError('unsupported genre')
    source, output = Path(source), Path(output)
    if not source.is_file():
        raise FileNotFoundError(source)
    if source.resolve() == output.resolve():
        raise ValueError('input and output must differ')
    p = probe(source)
    video = next(s for s in p['streams'] if s['codec_type']=='video')
    audio = next(s for s in p['streams'] if s['codec_type']=='audio')
    if video['codec_name'] != 'h264' or audio['codec_name'] != 'aac':
        raise ValueError('expected H.264 video and AAC audio')
    num, den = map(int,video['avg_frame_rate'].split('/'))
    fps = num / den
    duration = float(video['duration'])
    chapters = p.get('chapters',[])
    spans = detect_silences(source)
    cut, reason = calculate_cut(duration, fps, spans,
                                float(chapters[-1]['start_time']) if chapters else 0)
    output.parent.mkdir(parents=True,exist_ok=True)
    frame_count = round(cut * fps)
    call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
          '-map','0:v:0','-map','0:a:0','-map_chapters','0',
          '-c','copy','-frames:v',str(frame_count),'-t',f'{cut:.6f}',
          '-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
    q = probe(output)
    v = next(s for s in q['streams'] if s['codec_type']=='video')
    if int(v['nb_frames']) != frame_count or abs(float(q['format']['duration']) - cut) > 1/fps:
        raise RuntimeError('incorrect frame count/duration after stream copy')
    if len(q['chapters']) != len(chapters):
        raise RuntimeError('chapter count changed')
    report = {
      'genre':genre, 'source_seconds':duration, 'output_seconds':float(q['format']['duration']),
      'saved_seconds':round(duration-float(q['format']['duration']),3),
      'source_frames':int(video['nb_frames']), 'output_frames':int(v['nb_frames']),
      'fps':fps,'reason':reason,'silence_threshold_db':NOISE_DB,
      'silence_spans_seconds':[[round(a,3),round(b,3)] for a,b in spans],
      'trailing_silence_start_seconds':round(spans[-1][0],3) if spans else None,
      'chapter_count':len(chapters),
      'chapter_activity_audit':[{'chapter':i+1,'start':float(c['start_time']),
        'end':float(c['end_time']),
        'detected_silence_seconds':round(sum(max(0,min(float(c['end_time']),b)-max(float(c['start_time']),a)) for a,b in spans),3)}
        for i,c in enumerate(q['chapters'])],
      'semantic_transcription':'NOT VERIFIED - no independent Japanese ASR model',
      'human_review_required':True,
      'publication':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
    }
    if report_path:
        Path(report_path).parent.mkdir(parents=True,exist_ok=True)
        Path(report_path).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    return report

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('source');a.add_argument('output')
    a.add_argument('--genre',choices=GENRES,default='ai')
    a.add_argument('--report')
    args=a.parse_args()
    print(json.dumps(optimize(args.source,args.output,args.report,args.genre),ensure_ascii=False,indent=2))
