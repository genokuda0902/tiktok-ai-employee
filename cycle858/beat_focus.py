"""Review-only, narration-caption-beat-timed detail shots; never posts or uploads media.

Original v33 renderer is NOT recovered. Input remains private and rights-unapproved.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

GENRES = ('ai_work','sales_business','beauty','romance','saving','career',
          'wellness','science','travel_food','product_comparison_lifestyle')
POLICY = {'review_only':True,'publication_approved':False,'automatic_posting':False,
          'external_upload':False,'source_rights_reviewed':False,
          'contains_personal_data':False,'fictional_workflow_example':True}
# Eight major scenes. Second caption beats from a separate Draft PR timing manifest,
# NOT independently transcribed speech. Cuts only on editorial beat starts.
SCENES = ((0,89),(89,170),(170,251),(251,336),
          (336,422),(422,507),(507,588),(588,691))
CUTS = ((118,170),(276,336),(379,422),(458,507),(551,588),(634,691))
ROI = (86,476,908,758)  # excludes headline and burned-in Japanese subtitles
ZOOM = 1.055

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams',
                                               '-show_format','-of','json',str(path)],text=True))

def plan(scenes=SCENES,cuts=CUTS,roi=ROI,zoom=ZOOM):
    if not 1.02<=zoom<=1.12:raise ValueError('unsafe zoom')
    if len(scenes)!=8 or any(a>=b for a,b in scenes):raise ValueError('invalid scenes')
    if any(scenes[i][1]!=scenes[i+1][0] for i in range(7)):
        raise ValueError('scene gap/overlap')
    if len(cuts)<1 or any(not any(s<=a<b<=e for s,e in scenes) for a,b in cuts):
        raise ValueError('cut outside scenes')
    if any(cuts[i][1]>cuts[i+1][0] for i in range(len(cuts)-1)):
        raise ValueError('overlapping cuts')
    x,y,w,h=roi
    if x<0 or y<0 or w<500 or h<400 or x+w>1080 or y+h>1240:
        raise ValueError('unsafe caption/header region')
    zw=int(w/zoom)//2*2;zh=int(h/zoom)//2*2
    cx=x+(w-zw)//2;cy=y+(h-zh)//2
    expr='+'.join(f'between(n\\,{a}\\,{b-1})' for a,b in cuts)
    return {'roi':roi,'crop':(cx,cy,zw,zh),'cut_windows':cuts,
            'cut_frames':sum(b-a for a,b in cuts),'enable':expr}

def validate(source,output,manifest,genre,scenes,cuts):
    source,output=Path(source),Path(output)
    if genre not in GENRES:raise ValueError('unknown genre')
    if not source.is_file():raise FileNotFoundError('private source missing')
    if output.exists() or source.resolve()==output.resolve():raise ValueError('refuse overwrite')
    if manifest!={**POLICY,'source_sha256':sha256(source)}:
        raise ValueError('source hash or review-only policy mismatch')
    p=probe(source);v=next((s for s in p['streams'] if s['codec_type']=='video'),None)
    a=next((s for s in p['streams'] if s['codec_type']=='audio'),None)
    if not v or not a or (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],a['codec_name'])!=('h264',1080,1920,'30/1','aac'):
        raise ValueError('H264 1080x1920 30fps AAC required')
    if int(v.get('nb_frames',0))!=scenes[-1][1]:raise ValueError('frame count mismatch')
    plan(scenes,cuts)
    return int(v['nb_frames'])

def render(source,output,manifest,genre='ai_work',scenes=SCENES,cuts=CUTS):
    frames=validate(source,output,manifest,genre,scenes,cuts)
    p=plan(scenes,cuts);x,y,w,h=p['roi'];cx,cy,zw,zh=p['crop']
    # Scale only picture inset; original Japanese headline and captions remain.
    filt=(f'[0:v]split=2[base][detail];[detail]crop={zw}:{zh}:{cx}:{cy},'
          f'scale={w}:{h}:flags=lanczos,format=yuv420p[focus];'
          f'[base][focus]overlay=x={x}:y={y}:enable={p["enable"]}:'
          'eof_action=pass:shortest=1:format=auto[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(source),
         '-filter_complex',filt,'-map','[v]','-map','0:a:0','-c:v','libx264',
         '-preset','ultrafast','-crf','19','-pix_fmt','yuv420p','-r','30',
         '-frames:v',str(frames),'-c:a','copy','-movflags','+faststart',str(output)]
    try:subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        Path(output).unlink(missing_ok=True)
        raise RuntimeError('render failed: '+e.stderr.decode(errors='replace')[-1600:])
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],
                   check=True,stdout=subprocess.DEVNULL)
    p2=probe(output);v=next(s for s in p2['streams'] if s['codec_type']=='video')
    if int(v['nb_frames'])!=frames:raise RuntimeError('truncated output')
    return {'cycle':858,'genre':genre,'source_sha256':sha256(source),
            'output_sha256':sha256(output),'frames':frames,'fps':30,
            'extra_focus_shots':len(cuts),'changed_frames':p['cut_frames'],
            'windows':[list(z) for z in cuts],'roi':list(p['roi']),
            'independent_japanese_transcription_verified':False,
            'semantic_subtitle_sync_verified':False,'rights_approved':False,
            'phone_playback_verified':False,'publication_approved':False,
            'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for k in ('source','output','manifest','report'):ap.add_argument('--'+k,required=True)
    ap.add_argument('--genre',default='ai_work')
    ap.add_argument('--synthetic',action='store_true',help='two-second synthetic CI smoke only')
    a=ap.parse_args()
    m=json.loads(Path(a.manifest).read_text(encoding='utf-8'))
    if a.synthetic:
        scenes=((0,5),(5,10),(10,15),(15,45),(45,49),(49,53),(53,56),(56,60))
        cuts=((20,40),)
    else:scenes,cuts=SCENES,CUTS
    r=render(a.source,a.output,m,a.genre,scenes,cuts)
    Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(r,ensure_ascii=False))
