"""Detect and remove mixed/double-exposed hook transition frames.

Usage: python tools/quality/hook_ghost_guard.py --source input.mp4 --output output.mp4 --report report.json
Requires OpenCV and ffmpeg at runtime. No API keys, no upload, no posting.
"""
import argparse
import json
import subprocess
import tempfile
from pathlib import Path

def spaced_peaks(differences, fps, hook_seconds=2.2, max_cuts=2, exclusion_seconds=.18, min_peak=.12):
    end=min(len(differences),int(hook_seconds*fps))
    ranked=sorted(range(1,end),key=lambda i:differences[i],reverse=True)
    chosen=[]
    for i in ranked:
        if differences[i]<min_peak: break
        if i<5 or i+3>=len(differences): continue
        if all(abs(i-j)>max(1,int(exclusion_seconds*fps)) for j in chosen):
            chosen.append(i)
            if len(chosen)>=max_cuts: break
    return sorted(chosen)

def select_guard_frames(distances, min_both=.08):
    return {i:("before" if a<=b else "after") for i,(a,b) in distances.items() if min(a,b)>min_both}

def render(source, output, report, hook_seconds=2.2, max_cuts=2):
    import cv2
    import numpy as np
    source=Path(source); output=Path(output); report=Path(report)
    if source.resolve()==output.resolve(): raise ValueError("source must differ from output")
    cap=cv2.VideoCapture(str(source))
    if not cap.isOpened(): raise RuntimeError("input cannot be opened")
    fps=float(cap.get(cv2.CAP_PROP_FPS))
    frames=[]; diffs=[]; previous=None
    while True:
        ok,image=cap.read()
        if not ok: break
        gray=cv2.cvtColor(cv2.resize(image,(144,256)),cv2.COLOR_BGR2GRAY)
        diffs.append(0 if previous is None else float(np.mean(cv2.absdiff(gray,previous)))/255)
        frames.append(gray); previous=gray
    cap.release()
    if not frames or fps<=0: raise RuntimeError("invalid video")
    peaks=spaced_peaks(diffs,fps,hook_seconds,max_cuts)
    replacements={}; details=[]
    for peak in peaks:
        before,after=peak-3,peak+2
        distances={}
        for i in range(peak-2,peak+3):
            a=float(np.mean(cv2.absdiff(frames[i],frames[before])))/255
            b=float(np.mean(cv2.absdiff(frames[i],frames[after])))/255
            distances[i]=(a,b)
        for i,side in select_guard_frames(distances).items():
            ref=before if side=="before" else after
            replacements[i]=ref
            details.append({"frame":i,"reference_frame":ref,"time":round(i/fps,4)})
    if not replacements:
        raise RuntimeError("No confident blended frames; output not changed")
    with tempfile.TemporaryDirectory() as folder:
        folder=Path(folder); refs=sorted(set(replacements.values()))
        cap=cv2.VideoCapture(str(source))
        for i in refs:
            cap.set(cv2.CAP_PROP_POS_FRAMES,i); ok,image=cap.read()
            if not ok or not cv2.imwrite(str(folder/f"ref_{i}.png"),image):
                raise RuntimeError(f"Cannot extract clean reference {i}")
        cap.release()
        args=["-i",str(source)]
        for i in refs:
            args+=["-loop","1","-framerate",str(round(fps,6)),"-i",str(folder/f"ref_{i}.png")]
        chain=[]; current="[0:v]"
        for k,(frame,ref) in enumerate(sorted(replacements.items())):
            next_label=f"[v{k}]"
            chain.append(f"{current}[{refs.index(ref)+1}:v]overlay=0:0:enable='eq(n,{frame})':shortest=1{next_label}")
            current=next_label
        subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",*args,
                        "-filter_complex",";".join(chain),"-map",current,"-map","0:a:0",
                        "-c:v","libx264","-crf","17","-preset","fast","-pix_fmt","yuv420p",
                        "-c:a","copy","-frames:v",str(len(frames)),"-movflags","+faststart",
                        str(output)],check=True)
    result={"peaks":[{"frame":i,"seconds":round(i/fps,4),"frame_delta":round(diffs[i],5)} for i in peaks],
            "replacements":details,"count":len(replacements),"fps":fps,
            "publication":"HUMAN_REVIEW / PUBLICATION_NOT_APPROVED","rights":"UNVERIFIED"}
    report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--source",required=True)
    parser.add_argument("--output",required=True)
    parser.add_argument("--report",required=True)
    parser.add_argument("--hook-seconds",type=float,default=2.2)
    parser.add_argument("--max-cuts",type=int,default=2)
    a=parser.parse_args()
    print(json.dumps(render(a.source,a.output,a.report,a.hook_seconds,a.max_cuts)))
