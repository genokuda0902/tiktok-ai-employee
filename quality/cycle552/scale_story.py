"""Reusable visual-scale metadata for cycle552. No external images or publishing."""
from dataclasses import dataclass

GENRES = ("AI・仕事効率化","美容・身だしなみ","恋愛・心理","お金・節約","営業・ビジネス","転職・キャリア","健康・生活改善","雑学・科学","旅行・グルメ","商品比較・暮らし")
BOARD_MM = (85.0, 56.0)  # Raspberry Pi official approximate PCB dimensions
CARD_MM = (85.60, 53.98)  # ISO/IEC 7810 ID-1
SCENE_FRAME_START = 53
SCENE_FRAME_END = 105
CAPTION_TOP = 1270
PANEL_RECT = (60, 500, 1020, 1220)
PUBLICATION_APPROVED = False

def validate_scale_layout():
    x0,y0,x1,y1 = PANEL_RECT
    return len(GENRES)==10 and 0<=x0<x1<=1080 and 0<=y0<y1<CAPTION_TOP and SCENE_FRAME_END>SCENE_FRAME_START and not PUBLICATION_APPROVED

def dimension_comparison():
    return {"board_mm": BOARD_MM, "card_mm": CARD_MM, "board_to_card_width_ratio": BOARD_MM[0]/CARD_MM[0], "label": "CGイメージ・実機写真ではありません"}
