"""Verify repaired figure, untouched scene, audio PCM, full video decode."""
import argparse,hashlib,io,json,subprocess
from pathlib import Path
from PIL import Image
import numpy as np
from repair_caption_collision import probe

def run(cmd):
    p=subprocess.run(cmd,capture_output=True)
    if p.returncode:raise RuntimeError(p.stderr.decode(errors='replace')[-2000:])
    return p.stdout

def audio_pcm_sha(path):
    data=run(['ffmpeg','-v','error','-i',str(path),'-map','0:a:0',
      '-f','s16le','-acodec','pcm_s16le','-ar','48000','-ac','2','-'])
    return hashlib.sha256(data).hexdigest()

def frame(path,seconds):
    data=run(['ffmpeg','-v','error','-ss',str(seconds),'-i',str(path),
      '-frames:v','1','-f','image2pipe','-vcodec','png','-'])
    return Image.open(io.BytesIO(data)).convert('RGB')

def mae(a,b,box):
    return float(np.mean(np.abs(np.asarray(a.crop(box),dtype=np.int16)
                                 -np.asarray(b.crop(box),dtype=np.int16))))

def verify(obstructed,clean,output,report):
    p=probe(output)
    run(['ffmpeg','-v','error','-i',str(output),'-f','null','-'])
    aud0,aud1=audio_pcm_sha(obstructed),audio_pcm_sha(output)
    before,after,master=frame(obstructed,19.8),frame(output,19.8),frame(clean,19.8)
    box=(330,1400,850,1530)
    old_dist,new_dist=mae(before,master,box),mae(after,master,box)
    untouched=mae(frame(obstructed,10.5),frame(output,10.5),(200,400,850,1250))
    result={'pcm_audio_exact':aud0==aud1,'old_caption_vs_clean_mae':old_dist,
      'repaired_caption_vs_clean_mae':new_dist,
      'protected_text_restored':new_dist<old_dist*.2,
      'untouched_scene_mae':untouched,'untouched_scene_nearly_same':untouched<3.,
      'video_full_decode':True,'audio_pcm_sha256':aud1,
      'video_frames':int(next(s for s in p['streams'] if s['codec_type']=='video')['nb_frames'])}
    if not all(result[k] for k in ('pcm_audio_exact','protected_text_restored','untouched_scene_nearly_same')):
        raise AssertionError(json.dumps(result))
    Path(report).parent.mkdir(parents=True,exist_ok=True)
    Path(report).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    for key in ('input','clean','output','report'):p.add_argument('--'+key,required=True)
    a=p.parse_args()
    verify(a.input,a.clean,a.output,a.report)
