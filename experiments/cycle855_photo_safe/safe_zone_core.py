"""Ten-genre review-only TikTok-safe typography and layout.

Conservative 1080x1920 In-Feed *ad* template-derived exclusion; organic UI
may differ. This is a design check, not a guarantee of on-device visibility.
"""
from dataclasses import dataclass

WIDTH, HEIGHT = 1080, 1920
TOP, BOTTOM, LEFT, RIGHT = 240, 1260, 120, 960
ACTION_X, ACTION_Y = 780, 840
SAFE_CONTENT_X0, SAFE_CONTENT_X1 = 130, 760

PALETTES = {
    'ai_work': ('#101B2C', '#54F0D4'),
    'sales_business': ('#211E2B', '#FFBD71'),
    'beauty': ('#302234', '#F4A6D3'),
    'romance': ('#362232', '#F9A3C0'),
    'saving': ('#172B26', '#A4E6B0'),
    'career': ('#21283A', '#FFB49B'),
    'wellness': ('#243125', '#B9E99D'),
    'science': ('#182B42', '#91D0F8'),
    'travel_food': ('#183438', '#74DFE1'),
    'product_comparison_lifestyle': ('#2F2439', '#D7B0F7'),
}

@dataclass(frozen=True)
class Box:
    left: int
    top: int
    right: int
    bottom: int

    def safe(self):
        if not (LEFT <= self.left < self.right <= RIGHT and TOP <= self.top < self.bottom <= BOTTOM):
            return False
        if self.right > ACTION_X and self.bottom > ACTION_Y:
            return False
        return True

# All semantic information is inside the conservative exclusion boundaries.
TITLE1 = Box(130, 284, 760, 362)
TITLE2 = Box(130, 366, 760, 444)
PHOTO = Box(130, 474, 760, 894)
EXAMPLE = Box(130, 915, 760, 1064)
CAPTION = Box(130, 1083, 760, 1244)
CRITICAL = (TITLE1, TITLE2, PHOTO, EXAMPLE, CAPTION)

def validate():
    assert len(PALETTES) == 10
    assert all(b.safe() for b in CRITICAL)
    assert CAPTION.bottom <= BOTTOM
    assert CAPTION.right <= ACTION_X
    return True
