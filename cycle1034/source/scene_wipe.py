#!/usr/bin/env python3
"""Review-only cinematic scene wipe for approved existing local video.

This is a reimplementation, not recovered v33. No asset upload or posting.
Slide a still of the outgoing scene away, revealing the next scene, without
modifying the lower caption/voice region. 10 genre IDs accepted; real MP4
rendering is allowed only for ai_work with a pinned, private source hash.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path

GENRES=frozenset(('ai_work','beauty','romance_psychology','money_saving',
 'sales_business','career','health_lifestyle','science_trivia',
 'travel_food','product_comparison_lifestyle'))
FPS=30
WIDTH=1080
HEIGHT=1920
CROP_TOP=140
CROP_BOTTOM=1250
SUBTITLE_TOP=1490
CUT_FRAME=256 # 8.533s; existing scene 3 -> 4
WIPE_FRAMES=11

def run(cmd,binary=False):
    p=subprocess.run([str(c) for c in cmd],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode:
        raise RuntimeError('ffmpeg/ffprobe failed: '+' '.join(map(str,cmd[:7]))+'\n'+p.stderr.decode(errors='replace')[-2500:])
    return p.stdout if binary else p.stdout.decode()

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()

def audio_sha(path):
    return hashlib.sha256(run(['ffmpeg','-v','error','-i',path,'-map','0:a:0',
                              '-c','copy','-f','adts','-'],True)).hexdigest()

def probe(path):
    return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',path]))

def validate_cut(cut_frame,total_frames,wipe_frames=WIPE_FRAMES):
    if type(cut_frame) is not int or type(total_frames) is not int or type(wipe_frames) is not int:
        raise ValueError('integer frame counts required')
    if cut_frame<2 or wipe_frames<4 or wipe_frames>15 or cut_frame+wipe_frames>=total_frames:
        raise ValueError('unsafe or out-of-range transition')
    return True

def filtergraph(cut_frame= CUT_FRAME,wipe_frames=WIPE_FRAMES):
    validate_cut(cut_frame,cut_frame+wipe_frames+1,wipe_frames)
    start=cut_frame/FPS
    end=(cut_frame+wipe_frames)/FPS
    duration=wipe_frames/FPS
    # Crop outgoing frame before scene change; protect subtitles y>=1490.
    # Framesync holds this one still while it slides left during the new scene.
    return (f'[0:v]split=2[base][ref];'
            f'[ref]trim=start_frame={cut_frame-1}:end_frame={cut_frame},'
            f'setpts=PTS-STARTPTS,crop={WIDTH}:{CROP_BOTTOM-CROP_TOP}:0:{CROP_TOP}[old];'
            f"[base][old]overlay=x='if(between(t,{start:.6f},{end:.6f}),"
            f"-W*(t-{start:.6f})/{duration:.6f},-W)':y={CROP_TOP}:"
            f'eval=frame:eof_action=repeat:shortest=0[v]')

def render(source,output,report,expected_source_sha,genre='ai_work',review_only=False,
           cut_frame=CUT_FRAME,synthetic_ci=False):
    if not review_only:raise ValueError('explicit human review gate required')
    if genre not in GENRES:raise ValueError('unknown genre')
    if genre!='ai_work':raise ValueError('matching approved source for this genre unavailable')
    source,output,report=(Path(x).resolve() for x in (source,output,report))
    if not source.is_file() or output.exists() or report.exists() or source in (output,report):
        raise ValueError('missing source or existing output/report')
    if len(expected_source_sha)!=64 or sha(source)!=expected_source_sha:
        raise ValueError('pinned source SHA256 mismatch')
    p=probe(source)
    v=[s for s in p['streams'] if s['codec_type']=='video']
    a=[s for s in p['streams'] if s['codec_type']=='audio']
    if len(v)!=1 or len(a)!=1 or len(p['streams'])!=2:raise ValueError('one A/V stream required')
    if (v[0]['codec_name'],v[0]['width'],v[0]['height'],v[0]['r_frame_rate'],
        a[0]['codec_name'],int(a[0]['sample_rate']))!=('h264',WIDTH,HEIGHT,'30/1','aac',48000):
        raise ValueError('unsupported input; no silent video allowed')
    n=int(v[0]['nb_frames']); validate_cut(cut_frame,n)
    if not synthetic_ci and n!=691:raise ValueError('source not pinned 23.033s review edition')
    output.parent.mkdir(parents=True,exist_ok=True);report.parent.mkdir(parents=True,exist_ok=True)
    run(['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-y','-i',source,
         '-filter_complex',filtergraph(cut_frame),'-map','[v]','-map','0:a:0',
         '-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
         '-threads','2','-c:a','copy','-metadata:s:a:0','language=jpn',
         '-movflags','+faststart','-frames:v',str(n),output])
    run(['ffmpeg','-v','error','-xerror','-i',output,'-f','null','-'])
    q=probe(output)
    ov=next(s for s in q['streams'] if s['codec_type']=='video')
    if (ov['width'],ov['height'],ov['r_frame_rate'],int(ov['nb_frames']))!=(WIDTH,HEIGHT,'30/1',n):
        raise RuntimeError('output video mismatch')
    if audio_sha(source)!=audio_sha(output):raise RuntimeError('AAC bitstream changed')
    result={'source_sha256':sha(source),'output_sha256':sha(output),'genre':genre,
            'duration_seconds':float(q['format']['duration']),'frames':n,
            'video':'H.264 1080x1920 30fps','audio':'AAC 48kHz jpn-tagged',
            'audio_bitstream_unchanged':True,'full_av_decode':'PASS',
            'cut_frame':cut_frame,'wipe_frames':WIPE_FRAMES,
            'modified_content_region':[0,CROP_TOP,WIDTH,CROP_BOTTOM],
            'protected_subtitle_y_min':SUBTITLE_TOP,
            'change':'11-frame leftward wipe between scenes 3 and 4, caption-safe',
            'independent_japanese_asr':'NOT_PERFORMED',
            'caption_semantic_sync':'NOT_VERIFIED',
            'source_rights':'NOT_VERIFIED','employee_approval':'NOT_APPROVED',
            'publication':'NOT_APPROVED'}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    for name in ('source','output','report','expected-source-sha'):ap.add_argument('--'+name,required=True)
    ap.add_argument('--genre',default='ai_work');ap.add_argument('--review-only',action='store_true')
    ap.add_argument('--cut-frame',type=int,default=CUT_FRAME)
    ap.add_argument('--synthetic-ci',action='store_true')
    args=ap.parse_args()
    print(json.dumps(render(args.source,args.output,args.report,args.expected_source_sha,
          args.genre,args.review_only,args.cut_frame,args.synthetic_ci),ensure_ascii=False))
