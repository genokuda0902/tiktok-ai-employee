#!/usr/bin/env python3
"""Review-only, 10-genre-configurable fictional-data proof chart.

Makes a visual, proportionally correct A/B bar comparison in a per-video
reviewed region. Does not infer rights, subtitle meaning, or publication approval.
"""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

POLICY = 'HUMAN_REVIEW/PUBLICATION_NOT_APPROVED'
GENRE_COLORS = {
    'ai':'30D5CE', 'business':'E5B769', 'money':'54C78C',
    'learning':'AC9AFF', 'health':'72D6C3', 'food':'F3B679',
    'travel':'79C8ED', 'beauty':'E4A8D4', 'career':'F4C277',
    'life':'8FD3A9'
}
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
CAPTION_TOP=1280

def command(args):
    return subprocess.run(args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

def digest(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def media(path):
    j=json.loads(command(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))
    v=next(s for s in j['streams'] if s['codec_type']=='video')
    a=next(s for s in j['streams'] if s['codec_type']=='audio')
    return {'width':v['width'],'height':v['height'],'fps':v['avg_frame_rate'],
            'frames':int(v.get('nb_frames') or 0),'duration':float(j['format']['duration']),
            'video_codec':v['codec_name'],'audio_codec':a['codec_name'],
            'audio_rate':int(a['sample_rate']),'bytes':Path(path).stat().st_size}

def audio_hash(path):
    return hashlib.sha256(command(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0','-c:a','copy','-f','adts','pipe:1'])).hexdigest()

def numbers(m):
    data=m['fictional_data']
    if not isinstance(data,dict) or set(data)!= {'A','B'}:raise ValueError('Only approved A/B fictional dataset')
    for values in data.values():
        if not isinstance(values,list) or len(values)!=3 or any(type(x)!=int or x<0 or x>999 for x in values):
            raise ValueError('Three bounded fictional integers per series required')
    a,b=sum(data['A']),sum(data['B'])
    if a+b==0:raise ValueError('No nonzero evidence')
    return a,b,a+b

def validate(m,source):
    if m.get('policy')!=POLICY or m.get('asset_approval')!='review_only_no_publication' or m.get('manual_post_only') is not True:
        raise ValueError('Fail closed: publication policy')
    if m.get('source_sha256')!=digest(source) or m.get('genre') not in GENRE_COLORS or m.get('roi_reviewed') is not True:
        raise ValueError('Source/genre/ROI must be reviewed')
    p=media(source)
    if (p['width'],p['height'],p['fps'],p['video_codec'],p['audio_codec'],p['audio_rate'])!=(1080,1920,'30/1','h264','aac',48000):
        raise ValueError('Unsupported video/audio')
    r=m.get('roi'); times=m.get('time')
    if not isinstance(r,list) or len(r)!=4 or any(type(x)!=int for x in r):raise ValueError('Invalid ROI')
    x,y,w,h=r
    if x<40 or y<200 or w<700 or h<190 or x+w>1040 or y+h>CAPTION_TOP-60:
        raise ValueError('Unsafe or undersized ROI')
    if not isinstance(times,list) or len(times)!=2 or any(type(t) not in (float,int) for t in times):raise ValueError('Invalid time')
    start,end=times
    if start<0 or end-start<1.5 or end>p['duration']-.1:raise ValueError('Time outside scene')
    a,b,total=numbers(m)
    return p,(a,b,total)

def graph(m):
    x,y,w,h=m['roi'];start,end=m['time'];a,b,total=numbers(m)
    accent=GENRE_COLORS[m['genre']]
    on=lambda s=start,e=end:f"enable='between(t,{s:.3f},{e:.3f})'"
    filters=[
        f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x061b2c@1.0:t=fill:{on()}',
        f'drawbox=x={x}:y={y}:w={w}:h={h}:color=0x{accent}@0.82:t=3:{on()}',
    ]
    def txt(s,xx,yy,size,color='white',s0=None):
        text=s.replace(':','\\:').replace("'",'’')
        filters.append(f"drawtext=fontfile={FONT}:text='{text}':fontsize={size}:fontcolor={color}:x={xx}:y={yy}:{on(start if s0 is None else s0)}")
    txt('架空データ｜営業別の合計',x+23,y+13,30)
    txt('営業A',x+24,y+79,28)
    txt('営業B',x+24,y+138,28)
    barx=x+160;barw=w-330
    for yy in (y+85,y+144):
        filters.append(f'drawbox=x={barx}:y={yy}:w={barw}:h=25:color=0x173e53@0.95:t=fill:{on()}')
    # Discrete 10-step animation, tied to real ratios (not arbitrary bar lengths).
    # Overlapping growing rectangles intentionally make a stepped reveal.
    for j in range(1,11):
        t0=start+0.2+(j-1)*0.085
        for yy,val,color in ((y+85,a,accent),(y+144,b,'E5B769')):
            length=max(1,round(barw*val/max(a,b)*j/10))
            filters.append(f'drawbox=x={barx}:y={yy}:w={length}:h=25:color=0x{color}@0.98:t=fill:{on(t0,end)}')
    txt(str(a),x+w-123,y+72,39,'white',start+0.9)
    txt(str(b),x+w-123,y+131,39,'white',start+0.9)
    txt(f'合計 {total}',x+w-210,y+14,31,'0x'+accent,start+1.13)
    return ','.join(filters)

def render(source,output,manifest_path,report):
    source,output,manifest_path,report=map(Path,(source,output,manifest_path,report))
    if source.resolve()==output.resolve():raise ValueError('Never overwrite original')
    m=json.loads(manifest_path.read_text(encoding='utf-8'))
    before,totals=validate(m,source)
    output.parent.mkdir(parents=True,exist_ok=True)
    command(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-vf',graph(m),
             '-map','0:v:0','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','20',
             '-threads','4','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',
             '-t',str(before['duration']),str(output)])
    command(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'])
    after=media(output)
    same=audio_hash(source)==audio_hash(output)
    ok=(same and before['frames']==after['frames'] and abs(before['duration']-after['duration'])<.04)
    result={'policy':POLICY,'source_sha256':digest(source),'output_sha256':digest(output),
            'genre':m['genre'],'fictional_totals':{'A':totals[0],'B':totals[1],'total':totals[2]},
            'roi':m['roi'],'time':m['time'],'before':before,'after':after,
            'full_av_decode':True,'aac_adts_bit_identical':same,'technical_pass':ok,
            'independent_japanese_asr':False,'subtitle_semantics_or_timing_verified':False,
            'source_rights_approved':False,'employee_approved':False,'publication_approved':False}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    if not ok:
        output.unlink(missing_ok=True)
        raise RuntimeError('A/V verification failed; output removed')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('source','output','manifest','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False,indent=2))
