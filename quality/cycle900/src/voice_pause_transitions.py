"""Review-only, audio-pause-gated editorial light sweeps. Never posts or uploads media."""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

WIDTH, HEIGHT, FPS = 1080, 1920, 30
CUT_FRAMES = (89, 170, 251, 336, 423, 510, 588)
CAPTION_TOP = 1490
EFFECT_TOP, EFFECT_BOTTOM = 50, 1430
WINDOW_FRAMES = 2
MAX_CUT_RMS = 0.025
GENRES = ('ai_productivity','business','study','cooking','travel','beauty','health','finance','pets','hobbies')
POLICY = {'publication_approved':False,'automatic_posting':False,'external_upload':False,
          'paid_service':False,'human_review_required':True}


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()


def gate_cut(rms: float, threshold: float=MAX_CUT_RMS) -> bool:
    if not (0 <= rms <= 1): raise ValueError('invalid RMS')
    return rms <= threshold


def active_cut(frame: int, eligible: tuple[int,...]) -> tuple[int,int] | None:
    for cut in eligible:
        if abs(frame-cut)<=WINDOW_FRAMES: return cut,frame-cut
    return None


def light_strength(offset: int) -> float:
    if abs(offset)>WINDOW_FRAMES: return 0.
    return (1.0-abs(offset)/(WINDOW_FRAMES+1))*0.14


def measure_cut_rms(audio, rate: int, cuts=CUT_FRAMES):
    import numpy as np
    result={}
    for cut in cuts:
        t=cut/FPS
        start=max(0,round((t-.065)*rate)); stop=min(len(audio),round((t+.065)*rate))
        window=audio[start:stop]
        result[cut]=float(np.sqrt(np.mean(window*window))) if len(window) else 1.
    return result


def decode_audio(source: Path, rate: int=16000):
    import numpy as np
    raw=subprocess.check_output(['ffmpeg','-nostdin','-v','error','-i',str(source),'-vn',
                                 '-ac','1','-ar',str(rate),'-f','s16le','-'])
    return np.frombuffer(raw,dtype='<i2').astype(np.float32)/32768


def apply_light(frame, offset: int):
    """Edit ONLY y=50:1430, leaving the burned subtitle area untouched."""
    import numpy as np
    amount=light_strength(offset)
    if not amount: return frame
    h,w=frame.shape[:2]
    if (w,h)!=(WIDTH,HEIGHT): raise ValueError('unexpected video dimensions')
    center=((offset+WINDOW_FRAMES)/(2*WINDOW_FRAMES))*(w+240)-120
    xs=np.arange(w,dtype=np.float32)
    weights=(amount*np.exp(-.5*((xs-center)/105.)**2)).astype(np.float32)
    roi=frame[EFFECT_TOP:EFFECT_BOTTOM]
    # BGR tint: cyan-white, kept subtle to preserve the evidence UI.
    for channel,target in enumerate((230.,248.,252.)):
        original=roi[:,:,channel].astype(np.float32)
        roi[:,:,channel]=np.clip(original+(target-original)*weights[None,:],0,255).astype(np.uint8)
    return frame


def render(source: Path, output: Path, expected_sha: str):
    import cv2
    if sha256(source)!=expected_sha: raise ValueError('source SHA mismatch; fail closed')
    if source.resolve()==output.resolve(): raise ValueError('cannot overwrite source')
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError('cannot decode source')
    count=round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if count!=691: raise ValueError(f'expected 691 frames, got {count}')
    audio=decode_audio(source)
    rms=measure_cut_rms(audio,16000)
    eligible=tuple(c for c in CUT_FRAMES if gate_cut(rms[c]))
    output.parent.mkdir(parents=True,exist_ok=True)
    cmd=['ffmpeg','-y','-nostdin','-v','error','-f','rawvideo','-pix_fmt','bgr24',
         '-s',f'{WIDTH}x{HEIGHT}','-r',str(FPS),'-i','pipe:0','-i',str(source),
         '-map','0:v:0','-map','1:a:0','-c:v','libx264','-preset','veryfast',
         '-crf','18','-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart',str(output)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    edited=0
    try:
        for i in range(count):
            ok,frame=cap.read()
            if not ok: raise RuntimeError(f'failed at frame {i}')
            item=active_cut(i,eligible)
            if item:
                apply_light(frame,item[1]); edited+=1
            proc.stdin.write(frame.tobytes())
        proc.stdin.close()
        error=proc.stderr.read().decode(errors='replace')
        if proc.wait()!=0: raise RuntimeError(error[-2000:])
    finally:
        cap.release()
        if proc.poll() is None: proc.kill()
    return {'source_sha256':expected_sha,'output_sha256':sha256(output),
            'cut_rms':{str(k):round(v,6) for k,v in rms.items()},
            'eligible_cuts':list(eligible),'edited_frames':edited,
            'caption_untouched_before_encoding':True,'publication_approved':False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--sha256',required=True)
    p.add_argument('--report',type=Path,required=True)
    a=p.parse_args()
    result=render(a.source,a.output,a.sha256)
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')

if __name__=='__main__': main()
