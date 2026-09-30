import pytest

from quality.caption_safezone_contract import CaptionBox, validate_caption_safezone


def test_cycle231_geometry_passes_with_26px_clearance():
    assert validate_caption_safezone(1920, CaptionBox(top=1370, height=140)) == 26


def test_cycle230_geometry_fails_with_4px_intrusion():
    with pytest.raises(ValueError, match="caption safe-zone violation"):
        validate_caption_safezone(1920, CaptionBox(top=1390, height=150))


@pytest.mark.parametrize(
    "frame_height,box",
    [
        (0, CaptionBox(top=0, height=100)),
        (1920, CaptionBox(top=-1, height=100)),
        (1920, CaptionBox(top=100, height=0)),
    ],
)
def test_invalid_geometry_fails_closed(frame_height, box):
    with pytest.raises(ValueError, match="invalid geometry"):
        validate_caption_safezone(frame_height, box)
