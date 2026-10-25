from PIL import Image, ImageChops
import pytest
from cycle835 import crop_cover,draw_hook,GENRE_PRESETS,FRAMES,PHOTO

def test_all_genres():
    assert len(GENRE_PRESETS)==10
    assert all(len(v)==4 and v[0].startswith('#') for v in GENRE_PRESETS.values())

def test_total_frames():
    assert sum(FRAMES)==775

def test_crop_aspect():
    im=Image.new('RGB',(940,1672),'red')
    assert crop_cover(im,(478,1000)).size==(478,1000)

def test_hook_has_visible_difference():
    a=Image.new('RGB',(1080,1920),'#09232b')
    b=Image.new('RGB',(1080,1920),'#D1D7D4')
    hero=Image.new('RGB',(940,1672),'#B87351')
    changed=draw_hook(a,hero,b)
    assert changed.size==(1080,1920)
    assert ImageChops.difference(a.crop(PHOTO),changed.crop(PHOTO)).getbbox() is not None

def test_unknown_genre_rejected():
    with pytest.raises(ValueError):
        draw_hook(Image.new('RGB',(1080,1920)),Image.new('RGB',(940,1672)),Image.new('RGB',(1080,1920)),'unknown')
