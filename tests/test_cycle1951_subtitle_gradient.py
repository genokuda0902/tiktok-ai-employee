import tempfile
from pathlib import Path
from PIL import Image
from tools.cycle1951_subtitle_gradient import create_overlay

def test_gradient_preserves_upper_region():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d)/"overlay.png"
        create_overlay(p,width=12,height=100,start_y=60,max_alpha=27)
        im=Image.open(p)
        assert im.size == (12,100)
        assert im.getpixel((3,0))[3] == 0
        assert im.getpixel((3,59))[3] == 0
        values=[im.getpixel((3,y))[3] for y in range(60,100)]
        assert values == sorted(values)
        assert values[-1] <= 27
