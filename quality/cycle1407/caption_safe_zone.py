"""Reusable caption-safe-area geometry for synthetic review videos.

This is a layout check, NOT proof of speech synchronization or publication approval.
"""
def caption_rect(width: int, height: int):
    if width <= 0 or height <= 0:
        raise ValueError("positive dimensions required")
    # Central safe area; avoid bottom TikTok controls and edges.
    return (round(width * .06), round(height * .72),
            round(width * .94), round(height * .80))

def validate_caption_rect(rect, width: int, height: int):
    x1, y1, x2, y2 = rect
    return (0 <= x1 < x2 <= width and
            height * .65 <= y1 < y2 <= height * .84 and
            x1 >= width * .05 and x2 <= width * .95)

def publication_gate(*, japanese_speech_verified=False,
                     captions_synchronized=False,
                     rights_approved=False, employee_approved=False):
    return all((japanese_speech_verified, captions_synchronized,
                rights_approved, employee_approved))
