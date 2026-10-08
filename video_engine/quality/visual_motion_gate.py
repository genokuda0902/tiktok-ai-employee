"""Review-only genre-neutral motion-density gate. No publication approval.
Sampling can miss motion; human review remains mandatory.
"""
from dataclasses import dataclass
from typing import Sequence

@dataclass(frozen=True)
class MotionResult:
    sampled_pairs: int
    active_pairs: int
    active_ratio: float
    longest_static_seconds: float
    passed: bool
    reason: str

def analyze_luma_frames(frames: Sequence[bytes], width: int, height: int,
                        sample_interval: float = 0.5, pixel_delta: int = 16,
                        min_changed_fraction: float = 0.012,
                        min_active_ratio: float = 0.20,
                        max_static_seconds: float = 4.0) -> MotionResult:
    """Equally spaced raw 8-bit grayscale frames, one byte per pixel."""
    if width < 2 or height < 2 or len(frames) < 2:
        raise ValueError('at least two frames and 2x2 pixels required')
    if sample_interval <= 0 or not (0 < pixel_delta <= 255):
        raise ValueError('invalid sample interval or pixel threshold')
    if not (0 < min_changed_fraction <= 1) or not (0 < min_active_ratio <= 1):
        raise ValueError('invalid minimum ratios')
    if max_static_seconds <= 0: raise ValueError('invalid maximum static seconds')
    expected=width*height
    if any(len(f)!=expected for f in frames):
        raise ValueError('frame dimensions mismatch')
    left,right=max(0,int(width*.02)),min(width,int(width*.98))
    top,bottom=max(0,int(height*.02)),min(height,int(height*.98))
    pixels=max(1,(right-left)*(bottom-top))
    active=0;streak=0;max_streak=0
    for a,b in zip(frames,frames[1:]):
        changed=0
        for y in range(top,bottom):
            offset=y*width
            for x in range(left,right):
                p=offset+x
                if abs(a[p]-b[p])>=pixel_delta:changed+=1
        is_active=changed/pixels>=min_changed_fraction
        if is_active:active+=1;streak=0
        else:streak+=1;max_streak=max(max_streak,streak)
    pairs=len(frames)-1;ratio=active/pairs
    longest=max_streak*sample_interval
    ok=ratio>=min_active_ratio and longest<=max_static_seconds
    return MotionResult(pairs,active,round(ratio,4),round(longest,3),ok,
        'MOTION_PASS_REVIEW_ONLY' if ok else 'MOTION_INSUFFICIENT_REVIEW_ONLY')

def sample_video_ffmpeg(path: str, interval: float = 0.5, width: int = 96,
                        height: int = 160) -> list[bytes]:
    """Read sampled luma frames using FFmpeg, without uploading any video."""
    import subprocess
    if interval<=0:raise ValueError('interval must be positive')
    proc=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',path,
        '-vf',f'fps=1/{interval},scale={width}:{height}:flags=area,format=gray',
        '-f','rawvideo','-pix_fmt','gray','-'],capture_output=True,check=True)
    size=width*height
    if len(proc.stdout)%size:raise ValueError('incomplete sampled frame')
    return [proc.stdout[i:i+size] for i in range(0,len(proc.stdout),size)]
