"""Review-only 8-scene -> 16-editorial-beat edit of a SHA-pinned local MP4.

No generated claim, real-service assertion, private media upload or publishing.
The 16 editorial beats are not 16 independent scenes or a v33 reproduction.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

FPS=30
TOTAL=691
BOUNDARIES=(0,89,170,251,336,422,510,588,691)
GENRES=('ai_productivity','beauty','romance_psychology','money_saving',
        'sales_business','career','health_lifestyle','trivia_science',
        'travel_food','product_lifestyle')
POLICY={'review_only':True,'publication_approved':False,'external_upload':False,
        'automatic_posting':False,'source_rights_reviewed':False}


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def beats(boundaries=BOUNDARIES):
    if len(boundaries)!=9 or boundaries[0]!=0 or boundaries[-1]!=TOTAL or any(b<=a for a,b in zip(boundaries,boundaries[1:])):
        raise ValueError('Need eight contiguous scenes and 691 frames')
    return tuple((a,(a+b)//2,b) for a,b in zip(boundaries,boundaries[1:]))


def validate(m):
    if not isinstance(m,dict) or any(m.get(k) is not v for k,v in POLICY.items()):
        raise ValueError('Unapproved media: review-only policy required')
    if m.get('genre') not in GENRES:
        raise ValueError('Unknown genre')
    if not isinstance(m.get('source_sha256'),str) or len(m['source_sha256'])!=64 or any(c not in '0123456789abcdef' for c in m['source_sha256']):
        raise ValueError('Pinned SHA256 required')
    if m.get('real_service_footage') is not False or m.get('reference_equivalent') is not False:
        raise ValueError('Do not imply real-service footage or reference parity')
    return True


def filter_graph():
    # Eight second-half editorial beats: 2 safe central proof reframes and
    # 6 non-cropping focus accents. We deliberately never crop headline-heavy
    # scenes 1-6. All effects end at y1375; subtitles start at y1490.
    bs=beats()
    zoom_ids=(6,7)    # evidence and Before/After: central crop checked visually
    border_ids=(0,1,2,3,4,5)
    zoom='+'.join(f'between(n,{bs[i][1]},{bs[i][2]-1})' for i in zoom_ids)
    border='+'.join(f'between(n,{bs[i][1]},{bs[i][2]-1})' for i in border_ids)
    return ('[0:v]split=2[base][src];'
            '[src]crop=900:1120:90:220,scale=948:1180:flags=lanczos,format=yuv420p[zoom];'
            f"[base][zoom]overlay=66:180:enable='{zoom}':eof_action=pass:shortest=1[part];"
            f"[part]drawbox=x=38:y=155:w=1004:h=1220:color=0x66e5f4@0.72:t=5:enable='{border}'[v]")


def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
        'format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels',
        '-of','json',str(path)],text=True))


def validate_media(path):
    p=probe(path)
    v=next(x for x in p['streams'] if x['codec_type']=='video')
    a=next(x for x in p['streams'] if x['codec_type']=='audio')
    if (v['codec_name'],v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))!=('h264',1080,1920,'30/1',TOTAL):
        raise ValueError('Unexpected video geometry')
    if (a['codec_name'],int(a['sample_rate']),a['channels'])!=('aac',48000,2):
        raise ValueError('Unexpected audio stream')
    return p


def render(source,output,manifest,report):
    source,output,manifest,report=map(Path,(source,output,manifest,report))
    m=json.loads(manifest.read_text(encoding='utf-8'))
    validate(m)
    if sha256(source)!=m['source_sha256']:
        raise ValueError('Source SHA mismatch')
    validate_media(source)
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-filter_complex',filter_graph(),'-map','[v]','-map','0:a:0',
         '-frames:v',str(TOTAL),'-c:v','libx264','-preset','veryfast','-crf','19',
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    subprocess.run(cmd,check=True,timeout=300)
    validate_media(output)
    subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(output),'-f','null','-'],check=True,timeout=120)
    r={'cycle':897,'source_sha256':sha256(source),'output_sha256':sha256(output),
       'editorial_beats':16,'unique_scenes':8,'new_safe_focus_accents':6,'new_evidence_reframes':2,
       'cut_frames':[mid for _,mid,_ in beats()],
       'full_av_decode':'PASS','review_only':True,'publication_approved':False,
       'independent_japanese_asr':'UNVERIFIED','caption_semantic_match':'UNVERIFIED',
       'source_rights':'UNVERIFIED','smartphone_playback':'UNVERIFIED'}
    report.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    return r

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('source','output','manifest','report'):
        ap.add_argument('--'+name,required=True)
    a=ap.parse_args()
    print(json.dumps(render(a.source,a.output,a.manifest,a.report),ensure_ascii=False))
