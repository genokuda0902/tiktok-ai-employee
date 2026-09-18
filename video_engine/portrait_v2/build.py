#!/usr/bin/env python3
"""Offline rights-gated portrait renderer. Technical tests are NOT publication approval."""
import argparse, json, subprocess, tempfile, hashlib
from pathlib import Path
from PIL import Image
W,H,FPS=1080,1920,30

def run(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if p.returncode: raise RuntimeError(' '.join(map(str,args))+'\n'+p.stderr[-3000:])
    return p.stdout

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))

def main(config):
    cfg=Path(config).resolve();base=cfg.parent;c=json.loads(cfg.read_text(encoding='utf8'))
    scenes=c['scenes'];assets=c['assets'];test=c.get('mode')=='technical_test'
    if not 2<=len(scenes)<=12 or len({s['asset_id'] for s in scenes})<2: raise ValueError('Require 2-12 scenes and at least two independent assets')
    audio=(base/c['narration']).resolve();am=probe(audio)
    if not any(s['codec_type']=='audio' for s in am['streams']):raise ValueError('Narration missing audio')
    total=sum(float(s['seconds']) for s in scenes)
    if abs(float(am['format']['duration'])-total)>.35:raise ValueError('Audio duration mismatch')
    caps=json.loads((base/c['captions']).read_text(encoding='utf8'))
    if not caps or any(not x.get('text') or not 0<=float(x['start'])<float(x['end'])<=total+.05 for x in caps):raise ValueError('Invalid captions')
    out=(base/c['output']).resolve();out.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='portrait_v2_') as folder:
        td=Path(folder);segments=[]
        for i,s in enumerate(scenes):
            a=assets[s['asset_id']];path=(base/a['path']).resolve()
            if not path.is_file():raise FileNotFoundError(path)
            if not test and not (a.get('commercial_use') is True and a.get('derivatives_allowed') is True and a.get('privacy_review')=='approved' and a.get('rights_evidence') and a.get('rights_basis') and a.get('source_type')):raise ValueError('Asset rights not approved')
            sec=float(s['seconds']);frames=round(sec*FPS);motion=s.get('motion','static')
            if not 1<=sec<=15 or motion not in ('static','zoom_in','zoom_out','pan_left','pan_right'):raise ValueError('Invalid scene')
            dest=td/f'{i:02}.mp4'
            if a['type']=='image':
                with Image.open(path) as im:iw,ih=im.size
                if abs(iw/ih-W/H)>.004:raise ValueError('Independent native 9:16 image required')
                z={'static':'1','zoom_in':'min(zoom+0.0007,1.04)','zoom_out':'max(1.04-on*0.0007,1)'}.get(motion,'1.04')
                x='iw/2-iw/zoom/2';y='ih/2-ih/zoom/2'
                if motion=='pan_left':x=f'(iw-iw/zoom)*(1-on/{frames})'
                if motion=='pan_right':x=f'(iw-iw/zoom)*on/{frames}'
                vf=f"scale={W}:{H},zoompan=z='{z}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p"
                cmd=['ffmpeg','-v','error','-y','-loop','1','-framerate',str(FPS),'-i',str(path),'-vf',vf,'-frames:v',str(frames)]
            elif a['type']=='video':
                v=next(s for s in probe(path)['streams'] if s['codec_type']=='video')
                if abs(v['width']/v['height']-W/H)>.004 or float(probe(path)['format']['duration'])+.05<sec:raise ValueError('Invalid video aspect or duration')
                cmd=['ffmpeg','-v','error','-y','-i',str(path),'-t',str(sec),'-vf',f'scale={W}:{H},setsar=1,fps={FPS},format=yuv420p']
            else:raise ValueError('Unknown media type')
            run(cmd+['-an','-c:v','libx264','-preset','ultrafast','-crf','23',str(dest)]);segments.append(dest)
        manifest=td/'concat.txt';manifest.write_text(''.join("file '"+str(p)+"'\n" for p in segments))
        joined=td/'joined.mp4';run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(joined)])
        ass=td/'captions.ass'
        header='[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Noto Sans CJK JP,65,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,4,1,2,95,95,330,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
        def stamp(x):return f'{int(x//3600)}:{int(x%3600//60):02}:{x%60:05.2f}'
        def wrap(t):return '\\N'.join(t[i:i+14] for i in range(0,len(t),14))
        ass.write_text(header+''.join(f'Dialogue: 0,{stamp(x["start"])},{stamp(x["end"])},Default,,0,0,0,,{wrap(x["text"])}\n' for x in caps),encoding='utf8')
        run(['ffmpeg','-v','error','-y','-i',str(joined),'-i',str(audio),'-vf',f'ass={ass}','-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','ultrafast','-crf','23','-c:a','aac','-b:a','160k','-t',str(total),'-movflags','+faststart',str(out)])
    p=probe(out);v=next(s for s in p['streams'] if s['codec_type']=='video')
    if (v['width'],v['height'])!=(W,H) or not any(s['codec_type']=='audio' for s in p['streams']):raise RuntimeError('Invalid output')
    report={'mode':c.get('mode','review'),'output':str(out),'resolution':[W,H],'duration':float(p['format']['duration']),'audio':True,'captions_burned':True,'rights':'test only' if test else 'metadata assertions; human verification required','manual_review':'required','sha256':hashlib.sha256(out.read_bytes()).hexdigest()}
    (out.parent/(out.stem+'_render.json')).write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);main(p.parse_args().config)
