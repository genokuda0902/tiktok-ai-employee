"""Cycle904: review-only microcamera + independent *signal* QA, NOT ASR.

Reimplementation for locally approved review media. Public GitHub gets source/tests only.
Never infer speech content or word alignment from RMS/signal energy.
"""
from __future__ import annotations
import argparse, array, hashlib, json, math, subprocess, tempfile, wave
from pathlib import Path

GENRES = ('ai_work','business','education','finance','health','lifestyle',
          'technology','travel','food','entertainment')
SCENES = ((0,88),(89,169),(170,250),(251,335),(336,421),(422,506),(507,587),(588,690))
FPS = 30
FRAMES = 691
STATUS = 'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'
POLICY = {'publication_approved': False, 'employee_approval': False,
          'contains_private_data': False, 'asset_rights_approved': False,
          'automatic_posting': False, 'paid_service': False,
          'independent_japanese_asr_verified': False,
          'speech_caption_semantics_verified': False}


def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for part in iter(lambda:f.read(1<<20),b''):h.update(part)
 return h.hexdigest()


def run(cmd):
 p=subprocess.run(cmd,capture_output=True,text=True)
 if p.returncode:raise RuntimeError('command failed: '+repr(cmd[:5])+'\n'+p.stderr[-1800:])
 return p.stdout


def manifest_check(m):
 if not isinstance(m,dict) or m.get('genre') not in GENRES:raise ValueError('unsupported genre')
 for k in ('publication_approved','employee_approval','contains_private_data','asset_rights_approved'):
  if m.get(k) is not False:raise ValueError(k+' must explicitly be false for review only')
 sha=m.get('source_sha256')
 if not isinstance(sha,str) or len(sha)!=64 or any(c not in '0123456789abcdef' for c in sha):
  raise ValueError('source SHA256 required')
 if m.get('upload_media_to_github') is not False:raise ValueError('no public media uploads')
 return True


def media_info(path):
 return json.loads(run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(path)]))


def media_check(path):
 streams=media_info(path)['streams']
 v=next((x for x in streams if x['codec_type']=='video'),{})
 a=next((x for x in streams if x['codec_type']=='audio'),{})
 if (v.get('width'),v.get('height'),v.get('codec_name'),v.get('r_frame_rate'),int(v.get('nb_frames') or 0)) != (1080,1920,'h264','30/1',FRAMES):
  raise ValueError('expected 1080x1920 H264 30fps 691 frames')
 if a.get('codec_name')!='aac' or int(a.get('sample_rate') or 0)!=48000:raise ValueError('AAC 48k required')
 return True


def audio_adts_sha(path):
 with tempfile.TemporaryDirectory() as td:
  out=Path(td)/'a.aac'
  run(['ffmpeg','-v','error','-y','-i',str(path),'-vn','-c:a','copy','-f','adts',str(out)])
  return sha256(out)


def signal_audit(path):
 """Objective 20ms mono PCM metrics. Not an ASR or intelligibility score."""
 with tempfile.TemporaryDirectory() as td:
  wav=Path(td)/'mono.wav'
  run(['ffmpeg','-v','error','-y','-i',str(path),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)])
  with wave.open(str(wav),'rb') as w:
   if (w.getnchannels(),w.getsampwidth(),w.getframerate())!=(1,2,16000):raise ValueError('PCM format')
   data=w.readframes(w.getnframes())
 samples=array.array('h');samples.frombytes(data)
 if not samples:raise ValueError('empty audio')
 rms=[]
 for i in range(0,len(samples),320):
  seg=samples[i:i+320]
  rms.append(math.sqrt(sum(int(x)*int(x) for x in seg)/len(seg))/32768)
 return {'rms_20ms_windows':len(rms), 'rms_mean':round(sum(rms)/len(rms),5),
         'peak_normalized':round(max(abs(int(x)) for x in samples)/32768,5),
         'near_clipped_fraction':round(sum(abs(int(x))>=32440 for x in samples)/len(samples),7),
         'scene_rms_mean':[round(sum(rms[round(a/FPS*50):round((b+1)/FPS*50)])/max(1,len(rms[round(a/FPS*50):round((b+1)/FPS*50)])),5) for a,b in SCENES],
         'independent_asr':False, 'semantic_caption_match':False}


def zoom(frame):
 """Smooth, bounded microcamera trajectory; never changes subtitle panel."""
 return 1.012+0.010*math.sin(frame*0.018)


def filter_graph():
 # Video-only camera drift in upper 1300px. HUD, audio bars and captions below remain stable.
 return ("[0:v]split=2[base][top];"
         "[top]crop=1080:1300:0:0,"
         "zoompan=z='1.012+0.010*sin(on*0.018)':"
         "x='max(0,min(iw-iw/zoom,(iw-iw/zoom)/2+4*sin(on*0.03)))':"
         "y='max(0,min(ih-ih/zoom,(ih-ih/zoom)/2+4*cos(on*0.025)))':"
         "d=1:s=1080x1300:fps=30[cam];"
         "[base][cam]overlay=0:0:shortest=1[v]")


def render(source, output, manifest, clips_dir=None):
 source=Path(source).resolve();output=Path(output).resolve()
 if source==output or output.exists():raise ValueError('source overwrite/output overwrite prohibited')
 m=json.loads(Path(manifest).read_text(encoding='utf-8'))
 manifest_check(m)
 if sha256(source)!=m['source_sha256']:raise ValueError('source hash mismatch')
 media_check(source)
 output.parent.mkdir(parents=True,exist_ok=True)
 run(['ffmpeg','-v','error','-y','-i',str(source),'-filter_complex',filter_graph(),
      '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','19',
      '-pix_fmt','yuv420p','-c:a','copy','-frames:v',str(FRAMES),'-movflags','+faststart',str(output)])
 media_check(output)
 run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
 a0,a1=audio_adts_sha(source),audio_adts_sha(output)
 if a0!=a1:raise AssertionError('AAC bitstream changed')
 report={'status':STATUS,'genre':m['genre'],'source_sha256':sha256(source),
         'output_sha256':sha256(output),'audio_adts_sha256':a1,'audio_bitstream_identical':True,
         'video_full_decode':True,'caption_area_untouched_by_filter':True,
         'source_and_output_media_validated':True,'zoom_min':0.0,'zoom_max':0.0,
         'audio_signal':signal_audit(output),'employee_approval':False,'public_posting_allowed':False}
 zs=[zoom(i) for i in range(FRAMES)]
 report['zoom_min']=round(min(zs),5);report['zoom_max']=round(max(zs),5)
 if clips_dir:
  clips_dir=Path(clips_dir);clips_dir.mkdir(parents=True,exist_ok=True)
  for i,(a,b) in enumerate(SCENES,1):
   clip=clips_dir/f'scene{i:02d}_PRIVATE_REVIEW.m4a'
   run(['ffmpeg','-v','error','-y','-ss',f'{a/FPS:.6f}','-i',str(source),
        '-t',f'{(b-a+1)/FPS:.6f}','-vn','-c:a','aac','-b:a','96k',str(clip)])
  report['private_review_audio_segments']=len(SCENES)
 return report


def release_gate(_report):
 raise PermissionError('PUBLICATION_NOT_APPROVED: independent Japanese ASR, rights, employee approval and device playback missing')


def main():
 p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
 p.add_argument('--manifest',required=True);p.add_argument('--report',required=True);p.add_argument('--clips-dir')
 a=p.parse_args();r=render(a.source,a.output,a.manifest,a.clips_dir)
 Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps(r,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
