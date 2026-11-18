from PIL import Image
from clean_slides import render_slide

def test_resolution(tmp_path):
    for i in range(5):
        p = tmp_path / f"{i}.png"
        render_slide(i, p)
        with Image.open(p) as im:
            assert im.size == (1080, 1920)

def test_invalid_index(tmp_path):
    import pytest
    with pytest.raises(ValueError):
        render_slide(5, tmp_path / "bad.png")
