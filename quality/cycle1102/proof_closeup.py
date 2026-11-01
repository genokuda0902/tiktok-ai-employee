"""Review-only Calc evidence close-up, original reimplementation (not v33)."""
import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

GENRES=('ai_work','money','career','business','health','study','lifestyle','technology','travel','mindset')
CROP=(90,335,900,500)
DEST=(50,325,980,544)
SAFE_Y=1280
START=20.3
END=21.6

def sha(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def call(cmd):
    p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode: raise RuntimeError(p.stderr[-2000:])
    return p.stdout

def validate(manifest):
    if set(manifest)!={'genre','synthetic_scenario','review_only','rights_status','contains_private_data'}:
        raise ValueError('manifest fields mismatch')
    if manifest['genre'] not in GENRES: raise ValueError('unsupported genre')
    if manifest['synthetic_scenario'] is not True or manifest['review_only'] is not True:
        raise ValueError('review-only gate failed')
    if manifest['rights_status']!='unverified' or manifest['contains_private_data'] is not False:
        raise ValueError('privacy/rights gate failed')
    x,y,w,h=CROP;dx,dy,dw,dh=DEST
    if not(0<=x<x+w<=1080 and 0<=y<y+h<SAFE_Y and 0<=dx<dx+dw<=1080 and 0<=dy<dy+dh<SAFE_Y):
        raise ValueError('caption safe geometry failed')
    return True

def probe(path):
    return json.loads(call(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def audio_sha(path):
    with tempfile.TemporaryDirectory() as t:
        p=Path(t)/'audio.aac'
        call(['ffmpeg','-v','error','-y','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts',str(p)])
        return sha(p)

def render(source,out,expected_sha,manifest,start=START,end=END):
    validate(manifest)
    if sha(source)!=expected_sha: raise ValueError('input SHA256 mismatch')
    data=probe(source)
    v=next((s for s in data['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in data['streams'] if s['codec_type']=='audio'),None)
    if not v or not a: raise ValueError('both video and audio required')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'])!=('h264',1080,1920,'30/1'):
        raise ValueError('source format mismatch')
    if (a['codec_name'],a['sample_rate'])!=('aac','48000'):
        raise ValueError('audio format mismatch')
    duration=float(data['format']['duration'])
    if not(0<=start<end<=duration-0.05): raise ValueError('invalid closeup window')
    x,y,w,h=CROP;dx,dy,dw,dh=DEST
    fc=(f'[0:v]split[base][src];[src]crop={w}:{h}:{x}:{y},'
        f'scale={dw}:{dh}:flags=lanczos[detail];'
        f"[base][detail]overlay={dx}:{dy}:enable='gte(t,{start})*lt(t,{end})':eof_action=pass[v]")
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    call(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
          '-filter_complex',fc,'-map','[v]','-map','0:a:0','-c:v','libx264',
          '-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-c:a','copy',
          '-movflags','+faststart',str(out)])
    result=probe(out)
    ov=next(s for s in result['streams'] if s['codec_type']=='video')
    return {'source_sha256':expected_sha,'output_sha256':sha(out),
            'audio_bitstream_identical':audio_sha(source)==audio_sha(out),
            'frames':int(ov.get('nb_frames',0)), 'duration':float(result['format']['duration']),
            'closeup_seconds':[start,end],'safe_caption_y_min':SAFE_Y,
            'release':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
            'japanese_semantic_asr':'NOT_VERIFIED','phone_playback':'NOT_VERIFIED'}

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--source-sha',required=True)
    p.add_argument('--out',required=True);p.add_argument('--manifest',required=True)
    p.add_argument('--report');p.add_argument('--start',type=float,default=START)
    p.add_argument('--end',type=float,default=END)
    a=p.parse_args()
    r=render(a.source,a.out,a.source_sha,json.loads(Path(a.manifest).read_text(encoding='utf-8')),a.start,a.end)
    if a.report: Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
