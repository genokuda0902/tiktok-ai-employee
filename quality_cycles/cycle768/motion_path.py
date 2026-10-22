"""Reusable, no-cost semantic connection animation for 1080x1920 slide videos.

Only changes the configured artwork region; never modifies narration/subtitle area.
Coordinates are content-specific; animation logic and palette are genre-neutral.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import cv2
import numpy as np

W,H,FPS = 1080,1920,30

@dataclass(frozen=True)
class MotionSpec:
    start_frame: int = 121
    end_frame: int = 177
    path_start: tuple[int,int] = (372, 876)
    path_end: tuple[int,int] = (496, 876)
    screen_rect: tuple[int,int,int,int] = (503, 700, 917, 1050)
    accent_rgb: str = '#52EBD0'
    safe_bottom: int = 1280

    def __post_init__(self):
        assert 0 <= self.start_frame < self.end_frame
        assert len(self.accent_rgb) == 7 and self.accent_rgb[0] == '#'
        assert self.screen_rect[3] < self.safe_bottom
        assert max(self.path_start[1], self.path_end[1]) < self.safe_bottom


def bgr(hex_color: str) -> tuple[int,int,int]:
    c=hex_color.lstrip('#')
    return int(c[4:6],16),int(c[2:4],16),int(c[:2],16)


def apply_motion(frame: np.ndarray, frame_index: int, spec: MotionSpec=MotionSpec()) -> np.ndarray:
    """Add source→target travel then screen activation, preserving all pixels y>=1280."""
    if frame.shape != (H,W,3):
        raise ValueError(f'expected 1080x1920 BGR, got {frame.shape}')
    if not spec.start_frame <= frame_index < spec.end_frame:
        return frame
    # Restrict every compositing operation to a crop of the illustration.
    top,bottom=675,min(1090,spec.safe_bottom)
    crop=frame[top:bottom].copy()
    glow=np.zeros_like(crop)
    sharp=np.zeros_like(crop)
    accent=bgr(spec.accent_rgb)
    local=frame_index-spec.start_frame
    length=spec.end_frame-spec.start_frame
    # Semantic stages: 画面につなげば (travel), 操作できる (screen becomes active).
    # At 30 fps the second caption starts at frame 153.
    active_start=min(153-spec.start_frame,length-1)
    if local < active_start:
        progress=(local % 20)/19.0
        sx,sy=spec.path_start;ex,ey=spec.path_end
        x=int(sx+(ex-sx)*progress);y=int(sy+(ey-sy)*progress)-top
        cv2.circle(glow,(x,y),27,accent,-1,cv2.LINE_AA)
        cv2.circle(sharp,(x,y),8,(255,255,255),-1,cv2.LINE_AA)
        cv2.circle(sharp,(x,y),4,accent,-1,cv2.LINE_AA)
        # Tail follows the connection wire; no arbitrary floating particles.
        for t in range(1,4):
            xt=int(sx+(ex-sx)*max(0,progress-t*.07))
            cv2.circle(sharp,(xt,y),max(2,6-t),accent,-1,cv2.LINE_AA)
    else:
        x1,y1,x2,y2=spec.screen_rect
        # Gently pulse only the monitor outline, then hold a readable end state.
        pulse=.5+.5*np.sin((local-active_start)*np.pi/10)
        thickness=3+round(2*pulse)
        cv2.rectangle(glow,(x1-5,y1-5-top),(x2+5,y2+5-top),accent,10,cv2.LINE_AA)
        cv2.rectangle(sharp,(x1,y1-top),(x2,y2-top),accent,thickness,cv2.LINE_AA)
        # Small, original checkmark inside the monitor's upper-right corner.
        tx,ty=x2-39,y1+37-top
        cv2.circle(sharp,(tx,ty),17,(8,60,53),-1,cv2.LINE_AA)
        cv2.line(sharp,(tx-8,ty),(tx-2,ty+6),accent,4,cv2.LINE_AA)
        cv2.line(sharp,(tx-2,ty+6),(tx+10,ty-8),accent,4,cv2.LINE_AA)
    glow=cv2.GaussianBlur(glow,(0,0),sigmaX=17,sigmaY=17)
    # glow is additive but capped; preserve text and illustration contrast.
    crop=cv2.addWeighted(crop,1,glow,.22,0)
    mask=np.any(sharp>0,axis=2)
    crop[mask]=cv2.addWeighted(crop,.20,sharp,.80,0)[mask]
    result=frame.copy()
    result[top:bottom]=crop
    return result


def genre_spec(accent_hex: str, *, start_frame=121,end_frame=177,
               path_start=(372,876),path_end=(496,876),screen_rect=(503,700,917,1050)) -> MotionSpec:
    """10-genre reuse: only colors and anchor positions are content-dependent."""
    return MotionSpec(start_frame,end_frame,path_start,path_end,screen_rect,accent_hex)
