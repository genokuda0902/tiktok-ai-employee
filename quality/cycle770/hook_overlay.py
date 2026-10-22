"""Offline two-stage hook overlay for 1080x1920 TikTok videos."""
import cv2

START_Y = 185
END_Y = 1320
FRAME_LIMIT = 60

def overlay_hook(frame, slides, index):
    if index >= FRAME_LIMIT:
        return frame
    if frame.shape[:2] != (1920, 1080):
        raise ValueError("Expected 1080x1920 frame")
    if len(slides) != 2 or any(s.shape != (1135, 1080, 3) for s in slides):
        raise ValueError("Expected two 1080x1135 BGR slides")
    if index < 29:
        art = slides[0]
    elif index <= 34:
        alpha = (index - 29) / 5
        art = cv2.addWeighted(slides[0], 1 - alpha, slides[1], alpha, 0)
    else:
        art = slides[1]
    out = frame.copy()
    out[START_Y:END_Y] = art
    return out
