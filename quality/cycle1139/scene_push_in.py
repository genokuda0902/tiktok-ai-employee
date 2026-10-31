"""Chapter-aware 0–2.4% cinematic push-in for 10 TikTok genres.
No user media or speech uploaded. No posting. Review-only."""
import argparse
import json
import subprocess
from pathlib import Path

GENRES = ('ai_workflow','business','finance','health','beauty',
          'travel','education','lifestyle','technology','entertainment')
MAX_ZOOM = 1.024

def probe(source):
    d=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
      '-show_chapters','-show_format','-of','json',str(source)],text=True))
    v=next(s for s in d['streams'] if s['codec_type']=='video')
    if (int(v['width']),int(v['height']),v['avg_frame_rate'])!=(1080,1920,'30/1'):
        raise ValueError('Source must be 1080x1920 30fps')
    n=int(v['nb_frames']) if 'nb_frames' in v else round(float(d['format']['duration'])*30)
    starts=sorted(set([0]+[round(float(c['start_time'])*30)
         for c in d['chapters'] if float(c['start_time'])>0.01]))
    if len(starts)<2 or starts[0]!=0 or starts[-1]>=n:
        raise ValueError('Two or more valid chapters required')
    return n,starts+[n]

def zoom_value(frame,starts,max_zoom=MAX_ZOOM):
    if max_zoom<1 or max_zoom>1.04: raise ValueError('Unsafe zoom')
    if frame<0 or frame>=starts[-1]: raise ValueError('Frame outside video')
    for a,b in zip(starts,starts[1:]):
        if a<=frame<b:
            return 1+(max_zoom-1)*(frame-a)/max(1,b-a-1)
    raise AssertionError('Unreachable')

def zoom_expression(starts,max_zoom=MAX_ZOOM):
    if max_zoom<1 or max_zoom>1.04: raise ValueError('Unsafe zoom')
    if starts[0]!=0 or any(b<=a for a,b in zip(starts,starts[1:])):
        raise ValueError('Invalid chapters')
    expr='1'
    for a,b in reversed(list(zip(starts,starts[1:]))):
        z=f'1+{max_zoom-1:.6f}*(on-{a})/{max(1,b-a-1)}'
        expr=f'if(between(on,{a},{b-1}),{z},{expr})'
    return expr

def render(source,output,genre='ai_workflow',max_zoom=MAX_ZOOM):
    if genre not in GENRES: raise ValueError('Unknown genre')
    source,output=Path(source),Path(output)
    if not source.is_file(): raise FileNotFoundError(source)
    n,starts=probe(source)
    z=zoom_expression(starts,max_zoom)
    vf=(f"zoompan=z='{z}':x='iw/2-iw/zoom/2':"
        "y='ih/2-ih/zoom/2':d=1:s=1080x1920:fps=30,format=yuv420p")
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
      '-map','0:v:0','-map','0:a:0','-vf',vf,'-c:v','libx264',
      '-preset','veryfast','-crf','19','-threads','4','-pix_fmt','yuv420p',
      '-r','30','-c:a','copy','-map_metadata','0','-map_chapters','0',
      '-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True)
    return {'frames':n,'chapter_frames':starts,'genre':genre,
      'max_zoom':max_zoom,'audio':'copied, speech semantics not verified'}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('source');p.add_argument('output')
    p.add_argument('--genre',choices=GENRES,default='ai_workflow')
    p.add_argument('--max-zoom',type=float,default=MAX_ZOOM)
    a=p.parse_args()
    print(json.dumps(render(a.source,a.output,a.genre,a.max_zoom),
                     ensure_ascii=False,indent=2))
