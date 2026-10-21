"""Cycle731 chart timing/genre contract. Synthetic data; review only."""
W,H,FPS=1080,1920,30
START,END,TOTAL=294,384,819
MONTHS=("1月","2月","3月","4月")
SALES=(12,15,20,18)
GENRES=("ai_work","beauty","love_psychology","saving","sales_business","career","health","science","travel_food","product_comparison")
CAPTION_SAFE=(62,1230,1018,1530)
def visible_progress(frame):
    if not 0<=frame<END-START:raise ValueError("bad frame")
    return tuple(max(0.,min(1.,(frame-10-i*15)/15)) for i in range(4))
def validate(genre):
    if genre not in GENRES or len(GENRES)!=10:raise ValueError("bad genre")
    if sum(SALES)!=65:raise ValueError("bad data")
    x1,y1,x2,y2=CAPTION_SAFE
    if not(0<=x1<x2<=W and 1100<y1<y2<=1550):raise ValueError("unsafe captions")
