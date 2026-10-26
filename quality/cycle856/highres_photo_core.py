"""cycle856 photo-led quality gate, portable across ten content genres."""
from dataclasses import dataclass
from math import isclose

FRAME_W, FRAME_H = 1080, 1920
PHOTO_BOX = (130, 454, 760, 1084)
CAPTION_CENTER = (445, 1160)
SAFE_TEXT = (130, 270, 760, 1244)
GENRES = ('ai_work', 'sales_business', 'beauty', 'romance', 'saving',
          'career', 'wellness', 'science', 'travel_food', 'product_comparison_lifestyle')


def cover_geometry(source_size, box=PHOTO_BOX):
    """Center-crop to a native-pixel box; never silently enlarge source."""
    sw, sh = source_size
    x1, y1, x2, y2 = box
    bw, bh = x2-x1, y2-y1
    if min(sw, sh, bw, bh) <= 0:
        raise ValueError('invalid source/box size')
    scale = max(bw / sw, bh / sh)
    if scale > 1.0 + 1e-9:
        raise ValueError('photo source too small for native-pixel display')
    dw, dh = round(sw*scale), round(sh*scale)
    return {'scale':scale, 'display_px':(dw,dh), 'crop_px':(bw,bh),
            'source_px':(sw,sh), 'source_area_px':sw*sh}


def check_geometry():
    x1,y1,x2,y2 = PHOTO_BOX
    sx1,sy1,sx2,sy2 = SAFE_TEXT
    cx,cy = CAPTION_CENTER
    return (FRAME_W,FRAME_H)==(1080,1920) and sx1<=x1<x2<=sx2 and y1<y2<cy and sx1<cx<sx2 and cy<sy2


def validate_genres():
    return len(GENRES)==10 and len(set(GENRES))==10
