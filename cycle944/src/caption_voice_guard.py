"""Review-only Japanese subtitle legibility guard for voice-active fade gaps.

Uses audio energy and image contrast, NOT ASR; never claims semantic verification.
Requires the source's captions to be already burned into the MP4.
No network, posting, approvals, billing or asset uploads.
"""
from __future__ import annotations
import argparse, hashlib, json, math, subprocess
from pathlib import Path

GENRE_PRESETS = {
    'ai_productivity': .018, 'business': .018, 'finance': .017,
    'education': .019, 'health': .018, 'beauty': .020,
    'food': .019, 'travel': .020, 'lifestyle': .019,
    'technology': .018,
}
FPS=30
SCENE_CUTS=(0,87,174,261,348,435,522,609,691)
PATCH=(185,1458,923,1688)
TEXT=(250,1490,820,1625)

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def scene_for_frame(i,cuts=SCENE_CUTS):
    return next((j for j in range(len(cuts)-1) if cuts[j]<=i<cuts[j+1]),None)

def groups(indices):
    out=[]
    for i in indices:
        if out and i==out[-1][-1]+1:out[-1].append(i)
        else:out.append([i])
    return out

def select_repairs(visibility, rms_db, threshold=.018, max_gap=4, search=8,
                   cuts=SCENE_CUTS, min_reference=.045, voice_db=-34):
    """Return {frame: reference_frame}; short voiced dim runs with nearby bright text."""
    assert len(visibility)==len(rms_db)
    bad=[i for i,(v,db) in enumerate(zip(visibility,rms_db))
         if v<threshold and db>voice_db]
    selected={}
    for run in groups(bad):
        if len(run)>max_gap:continue
        if scene_for_frame(run[0],cuts)!=scene_for_frame(run[-1],cuts):continue
        candidates=[]
        for idx in (run[0]-1,run[-1]+1):
            direction=-1 if idx<run[0] else 1
            for distance in range(1,search+1):
                j=run[0]-distance if direction==-1 else run[-1]+distance
                if j<0 or j>=len(visibility):break
                if scene_for_frame(j,cuts)!=scene_for_frame(run[0],cuts):break
                if visibility[j]>=min_reference:
                    candidates.append((min(abs(j-k) for k in run),j))
                    break
        if not candidates:continue
        for i in run:
            selected[i]=min((j for _,j in candidates),key=lambda j:(abs(j-i),j>i))
    return selected

def audio_frame_db(source,sample_rate=16000,fps=FPS):
    import numpy as np
    raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(source),'-vn',
        '-ac','1','-ar',str(sample_rate),'-f','f32le','pipe:1'])
    audio=np.frombuffer(raw,dtype='<f4')
    count=int(math.ceil(len(audio)*fps/sample_rate))
    out=[]
    for i in range(count):
        s=audio[int(i*sample_rate/fps):int((i+1)*sample_rate/fps)]
        rms=float(np.sqrt(np.mean(s*s))) if len(s) else 0.
        out.append(20*math.log10(rms+1e-10))
    return out

def text_visibility(frame):
    import numpy as np
    x0,y0,x1,y1=TEXT
    band=frame[y0:y1,x0:x1]
    return float(np.mean((band[:,:,0]>120)&(band[:,:,1]>120)&(band[:,:,2]>120)))

def patch_frame(frame,reference,opacity=.92):
    import cv2
    x0,y0,x1,y1=PATCH
    roi=frame[y0:y1,x0:x1]
    other=reference[y0:y1,x0:x1]
    cv2.addWeighted(other,opacity,roi,1-opacity,0,dst=roi)
    return frame

def run(source,output,report,genre='ai_productivity'):
    import cv2
    if genre not in GENRE_PRESETS:raise ValueError('unknown genre')
    source,output,report=map(Path,(source,output,report))
    if not source.is_file():raise FileNotFoundError(source)
    cap=cv2.VideoCapture(str(source))
    fps=cap.get(cv2.CAP_PROP_FPS)
    frames=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if abs(fps-FPS)>.01 or frames!=691:raise ValueError('expected 691 frames at 30 fps')
    audio_db=audio_frame_db(source)
    if len(audio_db)<frames:raise RuntimeError('audio shorter than expected')
    vis=[]
    for _ in range(frames):
        ok,frame=cap.read()
        if not ok:raise RuntimeError('source decode truncated')
        vis.append(text_visibility(frame))
    cap.release()
    repairs=select_repairs(vis,audio_db[:frames],threshold=GENRE_PRESETS[genre])
    refs={}
    cap=cv2.VideoCapture(str(source))
    for idx in sorted(set(repairs.values())):
        cap.set(cv2.CAP_PROP_POS_FRAMES,idx)
        ok,frame=cap.read()
        if not ok:raise RuntimeError('reference decode failed')
        refs[idx]=frame
    cap.release()
    output.parent.mkdir(parents=True,exist_ok=True)
    temp=output.with_name('cycle944_video_only.mp4')
    enc=subprocess.Popen(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-f','rawvideo','-pixel_format','bgr24','-video_size','1080x1920',
        '-framerate','30','-i','pipe:0','-an','-c:v','libx264',
        '-preset','veryfast','-crf','18','-pix_fmt','yuv420p',
        '-movflags','+faststart',str(temp)],stdin=subprocess.PIPE,stderr=subprocess.PIPE)
    cap=cv2.VideoCapture(str(source))
    try:
        for i in range(frames):
            ok,frame=cap.read()
            if not ok:raise RuntimeError('render source truncated')
            if i in repairs:patch_frame(frame,refs[repairs[i]])
            enc.stdin.write(frame.tobytes())
        enc.stdin.close()
        error=enc.stderr.read().decode('utf8','replace')
        if enc.wait()!=0:raise RuntimeError(error[-1200:])
    finally:
        cap.release()
        if enc.poll() is None:enc.kill()
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y',
        '-i',str(temp),'-i',str(source),'-map','0:v:0','-map','1:a:0',
        '-c:v','copy','-c:a','copy','-movflags','+faststart',str(output)],check=True)
    temp.unlink(missing_ok=True)
    result={
        'cycle':944,'genre':genre,'source':source.name,'source_sha256':sha256(source),
        'output':output.name,'output_sha256':sha256(output),
        'improvement':'Speech-active faded subtitle gaps restored from adjacent legible frames; no ASR or semantic claim',
        'repaired_frames':sorted(repairs),'reference_frames':{str(k):v for k,v in repairs.items()},
        'frame_count':frames,'genre_presets':len(GENRE_PRESETS),
        'voice_threshold_dbfs':-34,'max_gap_frames':4,
        'approval':'HUMAN_REVIEW / PUBLICATION_NOT_APPROVED',
    }
    report.parent.mkdir(parents=True,exist_ok=True)
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',required=True)
    parser.add_argument('--output',required=True)
    parser.add_argument('--report',required=True)
    parser.add_argument('--genre',choices=sorted(GENRE_PRESETS),default='ai_productivity')
    a=parser.parse_args()
    print(json.dumps(run(a.source,a.output,a.report,a.genre),ensure_ascii=False,indent=2))
