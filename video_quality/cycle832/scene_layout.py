"""Cycle832 shared scene geometry for 10 genres (standard-library only).

This module is the portable part of the local cycle832 video renderer.
Actual image-generation assets, audio and the full renderer are kept in
the human-review ZIP; CI does NOT certify photo/video parity.
No publishing, posting, merging or paid API usage.
"""
WIDTH, HEIGHT = 1080, 1920
FRAME_COUNTS = (101, 93, 91, 99, 98, 101, 89, 103)
GENRE_ACCENTS = {
    "sales_business": "#F8B55E", "ai_work": "#3FE2D0",
    "beauty": "#EFA3BA", "romance": "#E8A6CE",
    "saving": "#E7C46D", "career": "#8DB4F5",
    "wellness": "#9CD6AB", "science": "#E3AC83",
    "travel_food": "#B5A0F4", "productivity": "#7FD4D9",
}
PHOTO_BOX = (62, 379, 1018, 1399)
SUBTITLE_BOX = (56, 1440, 1024, 1780)
SOURCE_COLLAGE_SIZE = (1024, 1536)

def source_crop(index):
    """Photo-only 240x405 crop; excludes timecode and burned-in text."""
    if not 0 <= index < 8:
        raise ValueError("scene index must be 0..7")
    x = (index % 4) * 256
    y = 70 if index < 4 else 835
    return (x + 8, y, x + 248, y + 405)

def validate_layout():
    assert len(GENRE_ACCENTS) == 10
    assert len(FRAME_COUNTS) == 8 and sum(FRAME_COUNTS) == 775
    assert WIDTH == 1080 and HEIGHT == 1920
    assert PHOTO_BOX[2] - PHOTO_BOX[0] == 956
    assert SUBTITLE_BOX[1] > PHOTO_BOX[1]
    for i in range(8):
        l,t,r,b = source_crop(i)
        assert (r-l, b-t) == (240,405)
        assert 0 <= l < r <= SOURCE_COLLAGE_SIZE[0]
        assert 0 <= t < b <= SOURCE_COLLAGE_SIZE[1]
    return True

if __name__ == "__main__":
    validate_layout()
    print("cycle832 geometry PASS")
