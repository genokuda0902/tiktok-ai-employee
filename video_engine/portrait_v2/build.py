#!/usr/bin/env python3
"""Rights-gated mixed-media 1080x1920 editor. No media acquisition or auto-posting."""
import argparse, json, subprocess, tempfile, hashlib
from pathlib import Path
from PIL import Image
W,H,FPS=1080,1920,30

def run(args):
    return subprocess.check_output(args, stderr=subprocess.STDOUT, text=True)

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def source(base, entry):
    p=(base/entry).resolve()
    if not p.is_file(): raise FileNotFoundError(p)
    return p

def approved(asset):
    required=('source_type','rights_basis','rights_evidence','commercial_use','derivatives_allowed','privacy_review')
    if any(not asset.get(k) for k in required): raise ValueError('Missing asset provenance/rights field: '+str(asset.get('path')))
    if asset['commercial_use'] is not True or asset['derivatives_allowed'] is not True or asset['privacy_review']!='approved':
        raise ValueError('Asset not cleared for commercial editing: '+str(asset.get('path')))
    if asset['source_type'] not in ('self_shot','licensed','official_permission','ai_disclosed'):
        raise ValueError('Unknown source type')
    if asset['source_type']=='ai_disclosed' and not asset.get('ai_disclosure'):
        raise ValueError('AI imagery must be disclosed')

def main(config):
    cfg=Path(config).resolve(); base=cfg.parent; c=json.loads(cfg.read_text(encoding='utf8'))
    scenes=c['scenes']; assets=c['assets']
    if not 2<=len(scenes)<=12: raise ValueError('Require 2-12 distinct scenes')
    if len({s['asset_id'] for s in scenes})<2: raise ValueError('Require at least two distinct source assets')
    if not c.get('narration'): raise ValueError('Narration required; visual tests use separate workflow')
    audio=source(base,c['narration']); meta=probe(audio)
    if not any(s['codec_type']=='audio' for s in meta['streams']): raise ValueError('Narration lacks audio stream')
    total=sum(float(s['seconds']) for s in scenes)
    if abs(float(meta['format']['duration'])-total)>.35: raise ValueError('Narration/scene duration mismatch')
    captions=c.get('captions')
    if not captions: raise ValueError('Caption timings required')
    caps=json.loads(source(base,captions).read_text(encoding='utf8'))
    for item in caps:
        if not item.get('text') or not 0<=float(item['start'])<float(item['end'])<=total+.05: raise ValueError('Invalid caption timing')
    out=source(base,c['output']) if (base/c['output']).exists() else (base/c['output']).resolve()
    out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='portrait_v2_') as folder:
        temp=Path(folder); clips=[]
        for i,s in enumerate(scenes):
            asset=assets[s['asset_id']]; approved(asset); path=source(base,asset['path'])
            seconds=float(s['seconds']); motion=s.get('motion','static')
            if not 1<=seconds<=15: raise ValueError('Scene duration out of range')
            if motion not in ('static','zoom_in','zoom_out','pan_left','pan_right'): raise ValueError('Invalid motion')
            dest=temp/f'{i:02}.mp4'; frames=round(seconds*FPS)
            if asset['type']=='image':
                with Image.open(path) as im: iw,ih=im.size
                if iw<1080 or ih<1080: raise ValueError('Image too small for high-quality output')
                # Letterbox intentionally prohibited: image must be composed for native portrait.
                if abs(iw/ih-W/H)>.003: raise ValueError('Image must be independently composed in 9:16; no poster crop or padding')
                zoom={'static':'1','zoom_in':'min(zoom+0.0008,1.025)','zoom_out':'max(1.025-on*0.0008,1)'}.get(motion,'1.02')
                x='iw/2-(iw/zoom/2)'; y='ih/2-(ih/zoom/2)'
                if motion=='pan_left': x='(iw-iw/zoom)*(1-on/'+str(max(frames,1))+')'
                if motion=='pan_right': x='(iw-iw/zoom)*on/'+str(max(frames,1))
                vf=f'scale=1080:1920,zoompan=z={zoom}:x={x}:y={y}:d={frames}:s=1080x1920:fps={FPS},format=yuv420p'
                args=['ffmpeg','-v','error','-y','-loop','1','-i',str(path),'-vf',vf,'-frames:v',str(frames)]
            elif asset['type']=='video':
                v=next((z for z in probe(path)['streams'] if z['codec_type']=='video'),None)
                if not v or abs(v['width']/v['height']-W/H)>.003: raise ValueError('Video must be native 9:16')
                if float(probe(path)['format']['duration'])+.03<seconds: raise ValueError('Video source too short')
                args=['ffmpeg','-v','error','-y','-i',str(path),'-t',str(seconds),'-vf','scale=1080:1920:flags=lanczos,setsar=1,fps=30,format=yuv420p']
            else: raise ValueError('Unknown media type')
            run(args+['-an','-c:v','libx264','-preset','medium','-crf','19',str(dest)]);clips.append(dest)
        manifest=temp/'concat.txt';manifest.write_text(''.join("file '"+str(p)+"'\n" for p in clips))
        silent=temp/'silent.mp4';run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(silent)])
        # Caption timing is provided as a separate sidecar; no unverified auto-alignment claim.
        run(['ffmpeg','-v','error','-y','-i',str(silent),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','aac','-b:a','160k','-t',str(total),'-movflags','+faststart',str(out)])
    p=probe(out);v=next(z for z in p['streams'] if z['codec_type']=='video')
    if (v['width'],v['height'])!=(W,H) or not any(z['codec_type']=='audio' for z in p['streams']):raise RuntimeError('Invalid output')
    report={'output':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'dimensions':[W,H],'duration':float(p['format']['duration']),'rights_evidence':'metadata asserted only; human must verify','captions':'timing sidecar validated; not burned in','manual_review_required':['actual rights evidence','visual quality and product accuracy','pronunciation','caption-to-speech alignment','caption burn-in before release']}
    (out.parent/(out.stem+'_qa.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--config',required=True);main(ap.parse_args().config)
