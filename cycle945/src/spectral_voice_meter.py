"""Offline, review-only 8-band spectral audio meter for pre-approved vertical videos.

Replaces generic volume-reactive top badge bars with frequency-specific bands.
Does not transcribe speech, isolate voice, infer copyright, post or publish.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
from pathlib import Path
import numpy as np

FPS = 30
FRAME_COUNT = 691
SR = 16000
BANDS = ((100,250),(250,450),(450,700),(700,1000),
         (1000,1500),(1500,2300),(2300,3600),(3600,6000))
GENRE_PRESETS = {
    'ai_productivity': (.78,.75), 'business': (.74,.72),
    'finance': (.72,.68), 'education': (.76,.72),
    'health': (.68,.65), 'beauty': (.70,.70),
    'food': (.80,.75), 'travel': (.80,.76),
    'lifestyle': (.74,.70), 'technology': (.82,.78),
}
BAR_X = (569,587,605,623,641,659,677,695)
BAR_BOTTOM = 106
ROI = (565,68,710,112)


def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):
            h.update(chunk)
    return h.hexdigest()


def decode_audio(source):
    data=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vn',
                                  '-ac','1','-ar',str(SR),'-f','f32le','pipe:1'])
    return np.frombuffer(data,dtype='<f4')


def extract_features(audio, count=FRAME_COUNT):
    """Per-frame RMS and 8 actual frequency-band energies, not ASR."""
    energies=np.zeros((count,8),dtype=np.float64)
    rms=np.zeros(count,dtype=np.float64)
    hz=np.fft.rfftfreq(1024,1/SR)
    for i in range(count):
        chunk=audio[round(i*SR/FPS):round((i+1)*SR/FPS)]
        if not len(chunk): continue
        rms[i]=np.sqrt(np.mean(chunk.astype(np.float64)**2))
        v=np.zeros(1024)
        v[:len(chunk)]=chunk*np.hanning(len(chunk))
        spectrum=np.abs(np.fft.rfft(v))**2
        for j,(low,high) in enumerate(BANDS):
            energies[i,j]=np.sqrt(np.mean(spectrum[(hz>=low)&(hz<high)]))
    return rms,energies


def meter_heights(rms, energies, genre='ai_productivity'):
    if genre not in GENRE_PRESETS: raise ValueError('unknown genre')
    if energies.ndim!=2 or energies.shape!=(len(rms),8):
        raise ValueError('expected 8 bands for every frame')
    spectral_weight, attack=GENRE_PRESETS[genre]
    # Noise floor and 90th-percentile reference are computed only on this video.
    active=rms>max(0.006,float(np.quantile(rms,.22)))
    if not np.any(active): return np.full(energies.shape,7,dtype=np.int16)
    energy_db=20*np.log10(energies+1e-7)
    lo=np.quantile(energy_db[active],.08,axis=0)
    hi=np.quantile(energy_db[active],.90,axis=0)
    spectral=np.clip((energy_db-lo)/(np.maximum(hi-lo,1.0)),0,1)
    global_db=20*np.log10(rms+1e-8)
    low,high=np.quantile(global_db[active],[.08,.90])
    global_level=np.clip((global_db-low)/max(high-low,1.0),0,1)
    raw=spectral_weight*spectral+(1-spectral_weight)*global_level[:,None]
    # A short release reduces visual flicker without pretending to align words.
    smoothed=np.empty_like(raw)
    smoothed[0]=raw[0]
    for i in range(1,len(raw)):
        alpha=attack if np.any(raw[i]>smoothed[i-1]) else .45
        smoothed[i]=alpha*raw[i]+(1-alpha)*smoothed[i-1]
    smoothed[~active]*=.24
    return np.rint(7+26*np.clip(smoothed,0,1)).astype(np.int16)


def original_bar_heights(frame):
    import cv2
    result=[]
    for x in BAR_X:
        crop=frame[74:108,x:x+11]
        # Teal pixels only; excludes dark background and bright border.
        mask=(crop[:,:,1]>110)&(crop[:,:,0]>70)&(crop[:,:,2]<130)&(crop[:,:,1]>crop[:,:,2]+40)
        result.append(int(np.any(mask,axis=1).sum()))
    return result


def draw_meter(frame, heights, color=(176,199,34)):
    import cv2
    if len(heights)!=8 or any(int(h)<7 or int(h)>33 for h in heights):
        raise ValueError('bar heights outside 7..33')
    x0,y0,x1,y1=ROI
    roi=frame[y0:y1,x0:x1]
    mask=cv2.inRange(roi,np.array([75,110,0],dtype=np.uint8),
                         np.array([255,255,145],dtype=np.uint8))
    mask=cv2.dilate(mask,np.ones((3,3),dtype=np.uint8))
    # Preserve badge outline and VOICE label; only inpaint existing teal pixels.
    clean=cv2.inpaint(roi,mask,4,cv2.INPAINT_TELEA)
    roi[:]=clean
    for x,h in zip(BAR_X,heights):
        top=BAR_BOTTOM-int(h)+1
        cv2.rectangle(frame,(x,top+4),(x+10,BAR_BOTTOM-4),color,-1,cv2.LINE_AA)
        cv2.circle(frame,(x+5,top+4),5,color,-1,cv2.LINE_AA)
        cv2.circle(frame,(x+5,BAR_BOTTOM-4),5,color,-1,cv2.LINE_AA)
    return frame


def correlation(a,b):
    a=np.asarray(a,dtype=float);b=np.asarray(b,dtype=float)
    if np.std(a)<1e-8 or np.std(b)<1e-8:return 0.0
    return float(np.corrcoef(a,b)[0,1])


def run(source,output,report,genre='ai_productivity'):
    import cv2
    source,output,report=map(Path,(source,output,report))
    if not source.is_file():raise FileNotFoundError(source)
    cap=cv2.VideoCapture(str(source))
    count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps=cap.get(cv2.CAP_PROP_FPS)
    w=int(cap.get(cv2.CAP_PROP_FRAME_WIDTH));h=int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    if (count,w,h)!=(FRAME_COUNT,1080,1920) or abs(fps-FPS)>.01:
        raise ValueError('expected 691 frames 1080x1920 30fps')
    audio=decode_audio(source)
    rms,features=extract_features(audio,count)
    heights=meter_heights(rms,features,genre)
    output.parent.mkdir(parents=True,exist_ok=True)
    tmp=output.with_suffix('.video_only.mp4')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo',
         '-pixel_format','bgr24','-video_size','1080x1920','-framerate','30',
         '-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','18',
         '-pix_fmt','yuv420p','-threads','2',str(tmp)]
    proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    cap=cv2.VideoCapture(str(source));before=[]
    try:
        for i in range(count):
            ok,frame=cap.read()
            if not ok:raise RuntimeError('truncated video')
            before.append(original_bar_heights(frame))
            proc.stdin.write(draw_meter(frame,heights[i]).tobytes())
        proc.stdin.close()
        err=proc.stderr.read().decode('utf-8','replace')
        if proc.wait()!=0:raise RuntimeError('ffmpeg: '+err[-1000:])
    finally:
        cap.release()
        if proc.poll() is None:proc.kill()
    subprocess.run(['ffmpeg','-v','error','-y','-i',str(tmp),'-i',str(source),
                    '-map','0:v:0','-map','1:a:0','-c:v','copy','-c:a','copy',
                    '-movflags','+faststart',str(output)],check=True)
    tmp.unlink(missing_ok=True)
    before=np.asarray(before)
    per_band_before=[correlation(before[:,j],features[:,j]) for j in range(8)]
    per_band_target=[correlation(heights[:,j],features[:,j]) for j in range(8)]
    result={'cycle':945,'source':source.name,'source_sha256':sha256(source),
            'output':output.name,'output_sha256':sha256(output),'genre':genre,
            'change':'8-bar audio meter uses 8 real spectral bands instead of generic overall loudness motion',
            'frames':count,'genre_presets':len(GENRE_PRESETS),
            'same_band_correlation_before':per_band_before,
            'same_band_correlation_after_target':per_band_target,
            'mean_same_band_correlation_before':float(np.mean(per_band_before)),
            'mean_same_band_correlation_after_target':float(np.mean(per_band_target)),
            'semantic_japanese_asr':'NOT_TESTED',
            'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED'}
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf8')
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--report',required=True)
    p.add_argument('--genre',choices=sorted(GENRE_PRESETS),default='ai_productivity')
    a=p.parse_args()
    print(json.dumps(run(a.source,a.output,a.report,a.genre),ensure_ascii=False,indent=2))
