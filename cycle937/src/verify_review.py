#!/usr/bin/env python3
"""Technical-only QA. Never equate audio energy with Japanese ASR/semantic sync."""
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np
from template_detail_microcuts import (WIDTH,HEIGHT,FPS,TOTAL_FRAMES,
    OVERLAY_START,OVERLAY_END,SAFE_Y,POLICY)


def cmd(args):
 p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-1600:])
 return p.stdout


def probe(path):
 return json.loads(cmd(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def validate_meta(meta):
 streams=meta.get('streams',[])
 v=next((x for x in streams if x.get('codec_type')=='video'),None)
 a=next((x for x in streams if x.get('codec_type')=='audio'),None)
 if not v or not a:raise AssertionError('audio and video both required')
 if (v.get('codec_name'),v.get('width'),v.get('height'),v.get('r_frame_rate'))!=('h264',WIDTH,HEIGHT,'30/1'):
  raise AssertionError('invalid video codec/resolution/fps')
 if (a.get('codec_name'),int(a.get('sample_rate',0)))!=('aac',48000):raise AssertionError('invalid audio codec/sample rate')
 if abs(float(meta['format']['duration'])-TOTAL_FRAMES/FPS)>0.08:raise AssertionError('duration mismatch')
 return v,a


def small_frames(path):
 b=cmd(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:v:0',
       '-vf','scale=135:240','-pix_fmt','gray','-f','rawvideo','-'])
 a=np.frombuffer(b,dtype=np.uint8)
 if a.size!=TOTAL_FRAMES*135*240:raise AssertionError(f'frame count mismatch: {a.size//(135*240)}')
 return a.reshape(TOTAL_FRAMES,240,135)


def adts(path):
 return cmd(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:a:0',
             '-c:a','copy','-f','adts','-'])


def audio_rms(path):
 b=cmd(['ffmpeg','-hide_banner','-loglevel','error','-i',str(path),'-map','0:a:0',
       '-ac','1','-ar','16000','-f','s16le','-'])
 x=np.frombuffer(b,dtype='<i2').astype('float32')/32768
 if x.size<16000*20:raise AssertionError('audio unexpectedly short')
 ranges=[(0,2.9),(2.9,5.8),(5.8,8.7),(8.7,11.6),(11.6,14.5),(14.5,17.4),(17.4,19.5667),(19.5667,23.0333)]
 vals=[float(np.sqrt(np.mean(np.square(x[int(s*16000):int(e*16000)])))) for s,e in ranges]
 if min(vals)<0.00005:raise AssertionError('one scene has near-silent soundtrack')
 return vals


def verify(source,output):
 s=probe(source);o=probe(output);validate_meta(s);validate_meta(o)
 # Fail closed if decoder sees any invalid packet/frame.
 cmd(['ffmpeg','-v','error','-xerror','-i',str(output),'-map','0:v:0','-map','0:a:0','-f','null','-'])
 sa=adts(source);oa=adts(output)
 if sa!=oa:raise AssertionError('AAC elementary bitstream changed')
 a=small_frames(source).astype('int16');b=small_frames(output).astype('int16')
 diff=np.abs(a-b).mean(axis=(1,2))
 band=np.abs(a[:,186:229,:]-b[:,186:229,:]).mean(axis=(1,2))
 outside=np.r_[diff[:OVERLAY_START],diff[OVERLAY_END:]]
 changed=diff[OVERLAY_START:OVERLAY_END]
 if np.any(changed<2.0):raise AssertionError('edited frame too similar')
 if float(outside.max())>1.5:raise AssertionError('unintended edit outside target range')
 if float(band.max())>1.5:raise AssertionError('subtitle region modified')
 rms=audio_rms(output)
 return {'policy':POLICY,'status':'TECHNICAL_PASS_HUMAN_REVIEW_REQUIRED',
   'source_sha256':hashlib.sha256(Path(source).read_bytes()).hexdigest(),
   'output_sha256':hashlib.sha256(Path(output).read_bytes()).hexdigest(),
   'video':'H264 1080x1920 30fps 691 frames','duration_s':float(o['format']['duration']),
   'audio':'AAC 48000Hz inherited, ADTS identical',
   'full_decode':'PASS','edited_frames':len(changed),
   'changed_frame_mae_min':round(float(changed.min()),3),
   'outside_frame_mae_max':round(float(outside.max()),3),
   'caption_region_mae_max':round(float(band.max()),3),
   'audio_rms_by_scene':[round(x,5) for x in rms],
   'speech_activity_test':'audio energy only; NOT ASR',
   'independent_japanese_transcription':'NOT_VERIFIED',
   'subtitle_semantics_and_word_timing':'NOT_VERIFIED',
   'smartphone_playback':'NOT_VERIFIED','rights':'NOT_VERIFIED',
   'employee_approval':'NOT_APPROVED','publication_allowed':False}

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True);p.add_argument('--report',required=True)
 a=p.parse_args();r=verify(a.source,a.output);Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=False))
