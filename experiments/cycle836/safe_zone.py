"""TikTok 9:16 caption placement policy for cycle836.

The subtitle block should end before the lower 20% UI exclusion region.
This is a geometric estimate; smartphone playback still needs review.
"""
WIDTH, HEIGHT = 1080, 1920
LOWER_UI_START = int(HEIGHT * 0.8)  # 1536
SUBTITLE_CENTER_Y = 1395
MAX_SUBTITLE_BLOCK_HEIGHT = 270
CAPTION_PANEL = (32, 1210, 1048, 1562)

def subtitle_inside_safe_zone(center=SUBTITLE_CENTER_Y,
                              block_height=MAX_SUBTITLE_BLOCK_HEIGHT):
    """Conservatively estimate whether all visible glyphs stay above lower UI."""
    return (center - block_height / 2 >= 0 and
            center + block_height / 2 <= LOWER_UI_START)

def move_ass_caption_center(ass_text, old_center=1640,
                            new_center=SUBTITLE_CENTER_Y):
    """Keep the 24 existing timing states while moving subtitle positions."""
    return ass_text.replace(f"pos(540,{old_center})",
                            f"pos(540,{new_center})")
