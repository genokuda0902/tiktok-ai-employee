"""Cycle688 reusable hook plan (no posting, no external dependencies)."""
PALETTES = {
 "ai_work": ("#40E2F2","#91ABFF"),
 "beauty": ("#F78DD0","#B0A1F7"),
 "love_psychology": ("#F5A7D1","#A8CBF9"),
 "saving": ("#82E7A5","#F3D083"),
 "sales_business": ("#57E7C0","#F4C981"),
 "career": ("#89C3F5","#80E1D0"),
 "health": ("#70E7B8","#9BCDF3"),
 "science": ("#49EFD2","#83B6FC"),
 "travel_food": ("#F3C475","#82DCCE"),
 "product_comparison": ("#B6ABF8","#85DBE5"),
}
WIDTH=1080
HEIGHT=1920
FPS=30
HOOK_SECONDS=2.1
GRAPHIC_BOTTOM=1360

def validate_hook(genre, question, answer, box):
    if genre not in PALETTES: raise ValueError("genre")
    if not question or not answer: raise ValueError("text")
    x,y,w,h=box
    if min(x,y)<0 or min(w,h)<=0 or x+w>WIDTH or y+h>GRAPHIC_BOTTOM:
        raise ValueError("safe area")
    return True
