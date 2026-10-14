#!/usr/bin/env python3
"""cycle576: image-first content motion and original scene-change earcons.

Review-only. The inherited source is not rights-cleared and is never committed.
No Japanese narration is claimed. No posting or auto-publishing.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
import soundfile as sf

GENRES=('ai_productivity','beauty','relationships','finance','sales','career',
        'wellness','science','travel_food','product_comparison')
SOURCE_SHA='6d182e9ed79f426a4d9a556e8557a160c84bc06031bd3110114405f3bac04511'
DURATION=20.0
CHAPTERS=((0.0,'結果'),(2.0,'元データ'),(4.0,'数式'),(6.0,'操作'),
          (9.0,'範囲選択'),(12.0,'照合'),(16.0,'比較'),(18.5,'保存'))
RIGHTS='INHERITED_ASSETS_UNVERIFIED'

def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()

def run(cmd):
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:
        raise RuntimeError('command failed '+str(p.returncode)+': '+' '.join(map(str,cmd))+'\n'+p.stderr[-4000:])
    return p

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_entries',
        'stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate:format=duration,size',
        '-of','json',str(path)]).stdout)

def validate_chapters(chapters=CHAPTERS, genres=GENRES):
    assert len(genres)==10 and len(set(genres))==10
    assert len(chapters)>=2 and chapters[0][0]==0
    assert all(chapters[i+1][0]>chapters[i][0] for i in range(len(chapters)-1))
    assert chapters[-1][0]<DURATION
    assert all(label and len(label)<=16 for _,label in chapters)
    return True

def make_earcons(folder,chapters=CHAPTERS,rate=44100):
    """Entirely synthesized gentle ticks at chapter boundaries."""
    validate_chapters(chapters)
    n=round(DURATION*rate)
    wave=np.zeros(n,dtype=np.float32)
    for i,(at,_) in enumerate(chapters):
        length=round(.16*rate)
        t=np.arange(length,dtype=np.float64)/rate
        attack=np.minimum(1.,t/.012)
        release=np.exp(-25*np.maximum(t-.025,0))
        env=attack*release
        freq=600+45*(i%4)
        pulse=(np.sin(2*np.pi*freq*t)+.25*np.sin(2*np.pi*freq*2*t))*env
        idx=round(at*rate)
        wave[idx:idx+length]+=(.085*pulse).astype(np.float32)
    peak=float(np.max(np.abs(wave)))
    assert 0<peak<.2
    p=Path(folder)/'original_transition_earcons.wav'
    sf.write(p,wave,rate,subtype='PCM_16')
    return p,peak

def filter_graph():
    # Only main content is animated. Headers, burned captions and REVIEW footer stay fixed.
    z="1.018+0.018*(1-cos(2*PI*on/180))/2"
    x="(iw-iw/zoom)/2+3*sin(on/47)"
    y="(ih-ih/zoom)/2+3*cos(on/59)"
    return (
      '[0:v]split=2[base][raw];'
      '[raw]crop=1020:1410:30:230,'
      f"zoompan=z='{z}':x='{x}':y='{y}':d=1:s=1020x1410:fps=30,"
      'setsar=1[move];'
      '[base][move]overlay=30:230:shortest=1:format=auto,'
      'format=yuv420p[v];'
      '[0:a:0]volume=0.87[bgm];'
      '[1:a:0]volume=1.0[earcon];'
      '[bgm][earcon]amix=inputs=2:duration=first:dropout_transition=0,'
      'alimiter=limit=0.89[a]')

def render(source,output,genre='ai_productivity'):
    validate_chapters()
    if genre not in GENRES:raise ValueError('unrecognized genre')
    source,output=Path(source),Path(output)
    if sha(source)!=SOURCE_SHA:raise ValueError('unapproved/unexpected source bytes')
    meta=probe(source)
    v=next(s for s in meta['streams'] if s['codec_type']=='video')
    a=next(s for s in meta['streams'] if s['codec_type']=='audio')
    if (v['width'],v['height'],v['r_frame_rate'])!=(1080,1920,'30/1') or abs(float(meta['format']['duration'])-20)>.06:
        raise ValueError('invalid source video')
    if a['codec_name']!='aac':raise ValueError('expected AAC source audio')
    output.parent.mkdir(parents=True,exist_ok=True)
    earcons,peak=make_earcons(output.parent)
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),'-i',str(earcons),
        '-filter_complex',filter_graph(),'-map','[v]','-map','[a]','-map','0:s:0',
        '-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-r','30',
        '-c:a','aac','-b:a','160k','-ar','44100','-c:s','mov_text','-t','20',
        '-movflags','+faststart',str(output)]
    run(cmd)
    result=probe(output)
    streams={s['codec_type']:s for s in result['streams']}
    assert {'video','audio','subtitle'}.issubset(streams)
    assert streams['video']['width']==1080 and streams['video']['height']==1920
    assert abs(float(result['format']['duration'])-DURATION)<.06
    manifest={'cycle':576,'genre':genre,'source_sha256':SOURCE_SHA,
        'output_sha256':sha(output),'duration_seconds':DURATION,
        'chapters':CHAPTERS,'source_rights':RIGHTS,'earcon_original_peak':peak,
        'motion':'continuous 1.8%-3.6% center zoom with subpixel pan in content only',
        'audio':'inherited BGM plus original transition earcons',
        'narration':'ABSENT','semantic_voice_caption_sync':'UNVERIFIED',
        'captions':'inherited Japanese baked subtitles + mov_text',
        'human_approval':False,'publication':'NOT_APPROVED','auto_post':False,
        'cost_jpy':0,'probe':result}
    (output.parent/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    return manifest

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',required=True)
    ap.add_argument('--output',required=True)
    ap.add_argument('--genre',default='ai_productivity')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.genre),ensure_ascii=False,indent=2))
