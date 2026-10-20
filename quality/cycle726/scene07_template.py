"""Reusable 10-genre storyboard timing for cycle726.
The full Pillow+FFmpeg renderer, tests and example MP4 are in the cycle726 ZIP
delivered for human review. This module is stdlib-only for CI.
"""
from __future__ import annotations

FPS=30
SCENE_START_FRAME=461
SCENE_END_FRAME=531
FRAMES=SCENE_END_FRAME-SCENE_START_FRAME
VIDEO_WIDTH,VIDEO_HEIGHT=1080,1920
GENRES={
    "AI・仕事効率化":"#5DD9FF",
    "美容・身だしなみ":"#FFB2D3",
    "恋愛・心理":"#DCA9FF",
    "お金・節約":"#81E4B2",
    "営業・ビジネス":"#FFCC74",
    "転職・キャリア":"#ADC6FF",
    "健康・生活改善":"#7DDFCA",
    "雑学・科学":"#56E6D4",
    "旅行・グルメ":"#FFAD8C",
    "商品比較・暮らし":"#D7E6A3",
}
CODE="print(2 + 3)"
CAPTION_BOX=(70,1384,865,1548)
TIKTOK_RIGHT_EXCLUSION=180
TIKTOK_BOTTOM_EXCLUSION=315

def smooth(x):
    x=max(0.0,min(1.0,float(x)))
    return x*x*(3.0-2.0*x)

def state(frame):
    """Scene-relative frame -> typed code, result reveal and Japanese speech captions.
    Caption timings are scene-aligned approximations, NOT ASR word alignment.
    """
    if not isinstance(frame,int) or not 0<=frame<FRAMES:
        raise ValueError("frame out of range")
    t=frame/FPS
    typed=0 if t<.20 else round(smooth((t-.20)/.70)*len(CODE))
    global_time=SCENE_START_FRAME/FPS+t
    caption=("最初は、" if 15.5333<=global_time<16.1333 else
             "たった一行。" if 16.1333<=global_time<17.0 else "")
    return {"typed_code":CODE[:typed],"result_visible":t>=1.12,
            "subtitle":caption,"stage":min(3,1+int(t>=.80)+int(t>=1.12))}

def validate():
    """Fail closed when the 10-genre palette or TikTok safe zones drift."""
    assert len(GENRES)==10
    assert all(v.startswith("#") and len(v)==7 for v in GENRES.values())
    x0,y0,x1,y1=CAPTION_BOX
    assert 0<=x0<x1<=VIDEO_WIDTH-TIKTOK_RIGHT_EXCLUSION
    assert 0<=y0<y1<=VIDEO_HEIGHT-TIKTOK_BOTTOM_EXCLUSION
    assert FRAMES==70
    assert state(0)["typed_code"]==""
    assert state(FRAMES-1)["typed_code"]==CODE
    assert state(FRAMES-1)["result_visible"]
    return True

if __name__=="__main__":
    print("cycle726",validate(),"10 genres",len(GENRES))
