"""Frame-local cinematic CPU highlight for cycle766; reusable in ten genre presets."""
import cv2
import numpy as np
FPS=30
BOARD_ROI=(185,610,775,1040)

def add_glow(frame, frame_index):
    i=frame_index
    if i<4 or i>=56:
        return frame
    fade=min(1.0,(i-4)/10.0,(56-i)/11.0)
    phase=(i-4)/52.0
    x0,y0,x1,y1=BOARD_ROI
    roi=frame[y0:y1,x0:x1].copy()
    glow=np.zeros_like(roi)
    x=int(390+24*phase)-x0
    y=int(850+78*phase)-y0
    cv2.ellipse(glow,(x,y),(11,35),-16,0,360,(75,173,65),-1)
    cv2.circle(glow,(x+8,y-16),3,(142,238,105),-1)
    soft=cv2.GaussianBlur(glow,(0,0),18)
    out=cv2.addWeighted(roi,1,soft,0.64*fade,0)
    frame[y0:y1,x0:x1]=cv2.addWeighted(out,1,glow,0.74*fade,0)
    return frame
