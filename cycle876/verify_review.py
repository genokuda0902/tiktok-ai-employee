"""Local-only A/V and subtitle-region regression checks; no ASR claims."""
from __future__ import annotations
import argparse, hashlib, json, subprocess
from pathlib import Path
import numpy as np

FPS, FRAMES = 30, 691
START, COUNT = 251, 85


def cmd(args, timeout=150):
    return subprocess.run(args, check=True, capture_output=True, timeout=timeout).stdout


def meta(p):
    d = json.loads(cmd(['ffprobe','-v','error','-show_entries',
                        'format=duration,size:stream=index,codec_type,codec_name,width,height,avg_frame_rate,sample_rate',
                        '-of','json',str(p)]))
    return d


def audio_hash(p):
    b = cmd(['ffmpeg','-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'],timeout=100)
    return hashlib.sha256(b).hexdigest()


def small_frames(p):
    b = cmd(['ffmpeg','-v','error','-i',str(p),'-map','0:v:0','-vf','scale=135:240',
             '-pix_fmt','rgb24','-f','rawvideo','-'],timeout=200)
    a = np.frombuffer(b,dtype=np.uint8)
    return a.reshape((-1,240,135,3))


def verify(old,new):
    old,new=Path(old),Path(new)
    a,b=meta(old),meta(new)
    v=next(x for x in b['streams'] if x['codec_type']=='video')
    sound=next(x for x in b['streams'] if x['codec_type']=='audio')
    assert (v['width'],v['height'],v['codec_name'],v['avg_frame_rate'])==(1080,1920,'h264','30/1')
    assert (sound['codec_name'],sound['sample_rate'])==('aac','48000')
    assert abs(float(b['format']['duration'])-691/30)<.001
    ah,bh=audio_hash(old),audio_hash(new)
    assert ah==bh, 'audio elementary bitstream changed'
    for p in (old,new):
        cmd(['ffmpeg','-v','error','-xerror','-i',str(p),'-f','null','-'],timeout=200)
    x,y=small_frames(old),small_frames(new)
    assert x.shape==y.shape==(691,240,135,3), (x.shape,y.shape)
    # Full-frame tiny downsample checks, not semantic subtitle OCR.
    diff=np.abs(x.astype(np.int16)-y.astype(np.int16))
    changed=diff.mean(axis=(1,2,3))
    # y=1490..1920 is inherited caption/footer; y 186..239 in 135x240 sampling.
    caption=diff[:,186:240].mean(axis=(1,2,3))
    changed_scene=changed[START:START+COUNT]
    untouched=np.concatenate((changed[:START],changed[START+COUNT:]))
    assert np.all(changed_scene>4.0), 'scene frames not visually changed'
    assert float(caption.max())<2.0, 'caption/footer protected area changed'
    assert float(untouched.max())<2.0, 'outside target scene changed'
    return {'status':'TECHNICAL_PASS','source_mp4':str(old),'output_mp4':str(new),
            'source_audio_adts_sha256':ah,'output_audio_adts_sha256':bh,
            'audio_bitstream_identical':True,'duration_s':float(b['format']['duration']),
            'resolution':[v['width'],v['height']],'video_codec':v['codec_name'],
            'audio_codec':sound['codec_name'],'sample_rate':int(sound['sample_rate']),
            'frames':len(x),'changed_target_frames':int(np.sum(changed_scene>4)),
            'target_frames':COUNT,'changed_scene_mean_pixel_delta':float(changed_scene.mean()),
            'caption_footer_max_mean_pixel_delta':float(caption.max()),
            'outside_scene_max_mean_pixel_delta':float(untouched.max()),
            'full_av_decode':True,'japanese_spoken_semantics_verified':False,
            'caption_meaning_timing_verified':False,'smartphone_playback_verified':False,
            'source_rights_verified':False,'publication_approved':False}


if __name__=='__main__':
    p=argparse.ArgumentParser()
    for n in ('old','new','report'):p.add_argument('--'+n,required=True)
    a=p.parse_args();r=verify(a.old,a.new)
    Path(a.report).write_text(json.dumps(r,ensure_ascii=False,indent=2))
    print(json.dumps(r,ensure_ascii=False))