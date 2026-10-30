#!/usr/bin/env python3
"""cycle1009: remove MP4 soft captions that default ON over existing burned-in Japanese captions.
Keep H264/AAC packets and MP4 chapters; export SRT/VTT for optional accessibility.
Review only; no transcription, rights clearance, publication or uploads.
"""
import argparse, hashlib, json, re, subprocess, tempfile
from pathlib import Path
GENRES=('ai_work','business','finance','education','health','travel','cooking','lifestyle','technology','entertainment')
STATUS='HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'

def run(args):
    p=subprocess.run(args,capture_output=True,text=True,timeout=240)
    if p.returncode: raise RuntimeError(f'{args[0]} exited {p.returncode}: {p.stderr[-1000:]}')
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_chapters','-show_format','-of','json',str(path)]))

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()

def srt_to_vtt(srt):
    blocks=re.split(r'\n\s*\n',srt.replace('\r\n','\n').strip())
    if not srt.strip(): raise ValueError('empty SRT')
    out=['WEBVTT','']; last=-1
    for i,block in enumerate(blocks,1):
        lines=block.splitlines()
        if len(lines)<3 or lines[0].strip()!=str(i): raise ValueError('invalid cue number/text')
        m=re.fullmatch(r'(\d\d:\d\d:\d\d),(\d{3}) --> (\d\d:\d\d:\d\d),(\d{3})',lines[1].strip())
        if not m: raise ValueError('invalid timecode')
        def ms(t,s):
            h,mi,se=map(int,t.split(':'))
            if mi>=60 or se>=60: raise ValueError('invalid clock')
            return ((h*60+mi)*60+se)*1000+int(s)
        start,end=ms(m[1],m[2]),ms(m[3],m[4])
        if not last<=start<end: raise ValueError('overlapping/reversed cue')
        last=end
        text='\n'.join(lines[2:]).strip()
        if not text or '-->' in text: raise ValueError('invalid cue text')
        out.extend([f'{m[1]}.{m[2]} --> {m[3]}.{m[4]}',text,''])
    return '\n'.join(out).rstrip()+'\n'

def packet_sha(path,kind):
    with tempfile.TemporaryDirectory() as tmp:
        out=Path(tmp)/('packets.h264' if kind=='v' else 'packets.aac')
        run(['ffmpeg','-v','error','-y','-i',str(path),'-map',f'0:{kind}:0','-c','copy','-f','h264' if kind=='v' else 'adts',str(out)])
        return sha(out)

def process(source,output,srt_source,*,genre='ai_work',synthetic=False):
    source,output,srt_source=map(Path,(source,output,srt_source))
    if genre not in GENRES: raise ValueError('unknown genre')
    if source.resolve()==output.resolve(): raise ValueError('cannot overwrite input')
    if not source.is_file() or not srt_source.is_file(): raise FileNotFoundError('source and approved SRT required')
    srt=srt_source.read_text(encoding='utf-8-sig')
    vtt=srt_to_vtt(srt)
    info=probe(source)
    streams=info['streams']
    video=next((s for s in streams if s['codec_type']=='video'),None)
    audio=next((s for s in streams if s['codec_type']=='audio'),None)
    subtitles=[s for s in streams if s['codec_type']=='subtitle']
    if not video or not audio or not subtitles: raise ValueError('requires video, audio, existing soft subtitle')
    if (video['codec_name'],video['width'],video['height'],video['avg_frame_rate'])!=('h264',1080,1920,'30/1'): raise ValueError('video spec mismatch')
    if (audio['codec_name'],audio['sample_rate'])!=('aac','48000'): raise ValueError('audio spec mismatch')
    duration=float(info['format']['duration'])
    if not synthetic and not (23<=duration<=23.1 and len(info.get('chapters',[]))==8): raise ValueError('unexpected review source')
    output.parent.mkdir(parents=True,exist_ok=True)
    if output.with_suffix('.srt').resolve()==srt_source.resolve(): raise ValueError('cannot overwrite source SRT')
    run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-map','0:v:0','-map','0:a:0','-map_metadata','0','-map_chapters','0',
         '-c:v','copy','-c:a','copy','-metadata:s:a:0','language=jpn','-movflags','+faststart',str(output)])
    output.with_suffix('.srt').write_text(srt,encoding='utf-8')
    output.with_suffix('.vtt').write_text(vtt,encoding='utf-8')
    result=probe(output)
    if any(s['codec_type']=='subtitle' for s in result['streams']): raise AssertionError('subtitle remains')
    if len(result.get('chapters',[]))!=len(info.get('chapters',[])): raise AssertionError('chapters lost')
    if packet_sha(source,'v')!=packet_sha(output,'v'): raise AssertionError('video changed')
    if packet_sha(source,'a')!=packet_sha(output,'a'): raise AssertionError('audio changed')
    run(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
    return dict(status=STATUS,genre=genre,duration=float(result['format']['duration']),
                size=[video['width'],video['height']],fps=video['avg_frame_rate'],
                chapters=len(result.get('chapters',[])),embedded_subtitles=0,
                optional_srt=str(output.with_suffix('.srt')),optional_vtt=str(output.with_suffix('.vtt')),
                video_packets_identical=True,audio_packets_identical=True,full_decode='PASS',
                independent_asr='NOT_DONE',publication='NOT_APPROVED')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--srt',type=Path,required=True);p.add_argument('--genre',choices=GENRES,default='ai_work')
    p.add_argument('--synthetic',action='store_true')
    a=p.parse_args()
    print(json.dumps(process(a.source,a.output,a.srt,genre=a.genre,synthetic=a.synthetic),ensure_ascii=False,indent=2))
