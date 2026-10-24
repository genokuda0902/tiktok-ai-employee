"""Cycle827: review-only offline Japanese-voice MP4 generator and technical QA.
Same scene renderer as cycle826, but speech-aware subtitle timing.
"""
from __future__ import annotations
import argparse,hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageChops
import speech827

FRAMES=speech827.FRAMES

def render(root):
    root=Path(root);speech827.create(root)
    out=root/'output'/'cycle827_SPEECH_AWARE_JAPANESE_HUMAN_REVIEW.mp4'
    inputs=[];parts=[]
    for i,n in enumerate(FRAMES):
        inputs+=['-i',str(root/'source'/f'scene_{i+1:02}.png')]
        direction=f'(iw-iw/zoom)*on/{n}' if i%2==0 else f'(iw-iw/zoom)*(1-on/{n})'
        parts.append(f"[{i}:v]zoompan=z='min(1.0+on*0.00024,1.028)':x='{direction}':y='(ih-ih/zoom)/2':d={n}:s=1080x1920:fps=30,setsar=1,format=yuv420p[v{i}]")
    parts.append(''.join(f'[v{i}]' for i in range(8))+'concat=n=8:v=1:a=0[vcat]')
    parts.append(f'[vcat]ass={root/"output"/"captions827.ass"}:fontsdir=/usr/share/fonts/opentype/noto[vout]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y',*inputs,
      '-i',str(root/'source'/'voice.m4a'),'-filter_complex',';'.join(parts),
      '-map','[vout]','-map','8:a:0','-c:v','libx264','-preset','veryfast',
      '-crf','23','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','160k',
      '-ar','48000','-af','apad','-t',str(775/30),'-movflags','+faststart',str(out)]
    subprocess.run(cmd,check=True)
    return out

def verify(root):
    root=Path(root);out=root/'output'/'cycle827_SPEECH_AWARE_JAPANESE_HUMAN_REVIEW.mp4'
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(out)]))
    v=next(x for x in info['streams'] if x['codec_type']=='video')
    a=next(x for x in info['streams'] if x['codec_type']=='audio')
    sync=json.loads((root/'output'/'sync827.json').read_text())
    ass=(root/'output'/'captions827.ass').read_text()
    decoded=subprocess.run(['ffmpeg','-v','error','-xerror','-i',str(out),'-map','0:v:0','-f','null','-'],capture_output=True)
    imgs=[Image.open(root/'source'/f'scene_{i:02}.png') for i in range(1,9)]
    checks={
      'mp4_exists_nonempty':out.stat().st_size>1000000,
      'portrait_1080x1920':(v['width'],v['height'])==(1080,1920),
      'h264_30fps':v['codec_name']=='h264' and v['r_frame_rate']=='30/1',
      '775_frames':int(v['nb_frames'])==775,
      'aac_japanese_source_48khz':a['codec_name']=='aac' and a['sample_rate']=='48000' and (root/'source'/'voice.m4a').exists(),
      'audio_full_length':float(a.get('duration',info['format']['duration']))>=25.7,
      'full_video_decode':decoded.returncode==0,
      'eight_1080x1920_original_scenes':len(imgs)==8 and all(im.size==(1080,1920) for im in imgs),
      'eight_distinct_scenes':all(ImageChops.difference(imgs[i],imgs[i+1]).getbbox() for i in range(7)),
      '24_japanese_caption_states':ass.count('Dialogue: 0,')==24 and 'AIで仕事を' in ass,
      'speech_detected_eight_scenes':all(x['voice_activity_detected'] for x in sync['scenes']),
      'changed_caption_boundaries':sum(abs(z)>0.1 for x in sync['scenes'] for z in x['shift_from_old_sec'])>=4,
      'monotonic_scene_safe_captions':all(all(x['caption_boundaries_sec'][j]<x['caption_boundaries_sec'][j+1] for j in range(3)) for x in sync['scenes']),
      'manual_review_required':sync['manual_listening_required'] and sync['not_forced_alignment'],
      'genre_independent_sync':sync['genre_independent'],
      'no_auto_post':True}
    report={'cycle':827,'previous_cycle':826,'checks':checks,'passed':sum(map(bool,checks.values())),
      'total':len(checks),'duration_seconds':float(info['format']['duration']),
      'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
      'source_audio_reused_in_local_build':False,
      'status':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
      'pending':['voice naturalness','word-level alignment','reference-video comparison',
                 'mobile playback','license review','employee approval']}
    (root/'output'/'qa827.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    if not all(checks.values()):raise RuntimeError(json.dumps(checks,indent=2))
    return report

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True)
    p.add_argument('--step',choices=['render','verify'],required=True)
    args=p.parse_args()
    result=(render if args.step=='render' else verify)(args.root)
    print(json.dumps(result,ensure_ascii=False,indent=2,default=str))
