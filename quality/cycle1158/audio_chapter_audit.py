"""Non-ASR audio continuity audit. RMS is NOT a Japanese transcript or sync proof."""
import array
import json
import math
import subprocess
from pathlib import Path

# Boundaries inferred from existing 8-chapter edit; manually review before publication.
CHAPTER_EDGES=(0,2.95,5.67,8.37,11.2,14.07,17.3,20.5,23.033333)
RATE=16000


def validate_edges(edges,duration):
    if len(edges)<3 or abs(edges[0])>.01 or abs(edges[-1]-duration)>.05:
        raise ValueError('Chapter coverage mismatch')
    if any(not isinstance(v,(float,int)) or not math.isfinite(v) for v in edges):
        raise ValueError('Invalid edge')
    if any(b-a<.25 for a,b in zip(edges,edges[1:])):
        raise ValueError('Unsorted or too-short chapters')


def audit(path,edges=CHAPTER_EDGES,min_rms=.0003):
    path=Path(path)
    meta=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-of','json',str(path)]))
    duration=float(meta['format']['duration']);validate_edges(edges,duration)
    pcm=subprocess.check_output(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-ac','1','-ar',str(RATE),'-f','s16le','-'])
    samples=array.array('h');samples.frombytes(pcm)
    rows=[]
    for i,(start,end) in enumerate(zip(edges,edges[1:]),1):
        s=samples[int(start*RATE):min(len(samples),int(end*RATE))]
        rms=math.sqrt(sum(v*v for v in s)/max(1,len(s)))/32768
        rows.append({'chapter':i,'start':start,'end':end,'rms':round(rms,6),'signal_present':rms>=min_rms})
    return {'method':'PCM RMS; NOT speech recognition','chapters':rows,'all_chapters_have_audio':all(r['signal_present'] for r in rows),'Japanese_transcript_verified':False,'subtitle_semantics_verified':False}

if __name__=='__main__':
    import sys
    print(json.dumps(audit(sys.argv[1]),ensure_ascii=False,indent=2))
