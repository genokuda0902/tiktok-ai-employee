from PIL import Image
from quality.cycle463.kinetic_cues import CUES,apply_cue,safe_bounds
import pytest

FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'

def test_all_eight_generic_cues():
    assert len(CUES)==8
    assert {'hook','before','data','formula','proof','result','compare','cta'}==set(CUES)

def test_caption_zone_untouched():
    im=Image.new('RGB',(720,1280),'#123456')
    old=im.crop((0,1010,720,1113)).tobytes()
    apply_cue(im,'proof',.7,FONT)
    assert im.crop((0,1010,720,1113)).tobytes()==old

def test_motion_progress_changes():
    a=Image.new('RGB',(720,1280),'#123456')
    b=Image.new('RGB',(720,1280),'#123456')
    apply_cue(a,'result',.05,FONT)
    apply_cue(b,'result',.95,FONT)
    assert a.crop((300,260,700,325)).tobytes()!=b.crop((300,260,700,325)).tobytes()

@pytest.mark.parametrize('progress',[-.1,1.01])
def test_invalid_progress(progress):
    with pytest.raises(ValueError):
        apply_cue(Image.new('RGB',(720,1280)),'hook',progress,FONT)

def test_invalid_kind():
    with pytest.raises(ValueError):
        apply_cue(Image.new('RGB',(720,1280)),'unknown',.5,FONT)

def test_bounds():
    assert safe_bounds() and safe_bounds(700)
