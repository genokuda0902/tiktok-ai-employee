"""Offline review-only first-second AFTER-panel visibility repair.

Requires an explicitly reviewed geometry for each source; does not infer visual
truth or publication rights. Reuses a clean frame from the same video and does
not create new claims, audio or captions. 10 genre-capable reusable engine.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess
import json
import hashlib
import cv2
import numpy as np

GENRES = ('ai_work','finance','business','education','lifestyle','health','travel','food','technology','career')

@dataclass(frozen=True)
class HookSpec:
    genre: str
    rect: tuple[int,int,int,int]
    clean_at_s: float
    visible_until_s: float
    fade_duration_s: float
    expected_sha256: str

    def validate(self):
        if self.genre not in GENRES: raise ValueError('unsupported genre')
        x,y,w,h=self.rect
        if not (0<=x<1080 and 0<=y<1440 and 20<=w<=1080-x and 20<=h<=1440-y):
            raise ValueError('repair must stay inside video content area')
        if not (0.0 < self.visible_until_s < self.clean_at_s < 2.9):
            raise ValueError('invalid timing; reference must be later than repair')
        if not (0.05<=self.fade_duration_s<=0.5): raise ValueError('invalid fade')
        if len(self.expected_sha256)!=64 or not all(c in '0123456789abcdef' for c in self.expected_sha256):
            raise ValueError('source hash must be pinned')


def sha256(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()


def alpha_feather(pw:int,ph:int,pixels:int=12)->np.ndarray:
    if min(pw,ph)<20 or pixels<1: raise ValueError('invalid patch dimensions')
    yy,xx=np.mgrid[0:ph,0:pw]
    edge=np.minimum.reduce((xx,yy,pw-1-xx,ph-1-yy)).astype('float32')
    return np.clip(edge/pixels,0,1)*255


def make_patch(source:Path, spec:HookSpec, output:Path):
    spec.validate()
    if sha256(source)!=spec.expected_sha256: raise RuntimeError('source hash mismatch; fail closed')
    cap=cv2.VideoCapture(str(source))
    try:
        if not cap.isOpened(): raise RuntimeError('source cannot open')
        w,h=round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps=cap.get(cv2.CAP_PROP_FPS); n=round(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if (w,h)!=(1080,1920) or abs(fps-30)>0.01 or n!=691:
            raise RuntimeError(f'unexpected video geometry: {w}x{h}, {fps}, {n}')
        cap.set(cv2.CAP_PROP_POS_FRAMES,round(spec.clean_at_s*fps))
        ok,frame=cap.read()
        if not ok: raise RuntimeError('cannot decode clean frame')
        x,y,pw,ph=spec.rect
        crop=frame[y:y+ph,x:x+pw].copy()
        # 12px feather prevents hard seams; inner panel stays fully opaque.
        alpha=alpha_feather(pw,ph)
        bgra=cv2.cvtColor(crop,cv2.COLOR_BGR2BGRA)
        bgra[:,:,3]=alpha.astype('uint8')
        output.parent.mkdir(parents=True,exist_ok=True)
        if not cv2.imwrite(str(output),bgra): raise RuntimeError('cannot save overlay')
        return {'source_sha256':spec.expected_sha256,'patch_rect':spec.rect,'clean_at_s':spec.clean_at_s,
                'visible_until_s':spec.visible_until_s,'fade_duration_s':spec.fade_duration_s,
                'publication_approved':False}
    finally: cap.release()


def render(source:Path,dest:Path,spec:HookSpec,patch_path:Path)->dict:
    qa=make_patch(source,spec,patch_path)
    x,y,_,_=spec.rect
    # 0-2s: show already-visible AFTER card. Blend to source once its original
    # reveal has completed; all non-panel pixels and audio remain source-derived.
    start=spec.visible_until_s-spec.fade_duration_s
    end=spec.visible_until_s
    vf=(f'[1:v]format=rgba,fade=t=out:st={start:.3f}:d={spec.fade_duration_s:.3f}:alpha=1[fix];'
        f'[0:v][fix]overlay={x}:{y}:enable=\'lt(t,{end:.3f})\':shortest=1[v]')
    cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(source),
         '-framerate','30','-loop','1','-i',str(patch_path),'-filter_complex',vf,
         '-map','[v]','-map','0:a:0','-c:v','libx264','-preset','veryfast','-crf','21',
         '-pix_fmt','yuv420p','-c:a','copy','-movflags','+faststart','-t','23.033333',str(dest)]
    dest.parent.mkdir(parents=True,exist_ok=True)
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode: raise RuntimeError(f'ffmpeg failed: {p.stderr[-2000:]}')
    return {**qa,'output_sha256':sha256(dest),'ffmpeg_command':cmd,'audio':'stream-copy'}

if __name__=='__main__':
    a=argparse.ArgumentParser()
    a.add_argument('--source',required=True);a.add_argument('--output',required=True)
    a.add_argument('--patch',required=True);a.add_argument('--qa',required=True)
    a.add_argument('--genre',default='ai_work');a.add_argument('--source-sha256',required=True)
    args=a.parse_args()
    spec=HookSpec(args.genre,(565,596,445,476),2.45,2.18,0.20,args.source_sha256)
    report=render(Path(args.source),Path(args.output),spec,Path(args.patch))
    Path(args.qa).write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='ffmpeg_command'},ensure_ascii=False))
