from pathlib import Path
import importlib.util
from PIL import Image
import numpy as np

P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('build_cycle585',P/'build_cycle585.py')
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def test_cues_cover_every_frame_without_gaps():
    assert m.validate_cues()
    assert sum(end-start for start,end,_ in m.CUES)==468

def test_all_ten_genres_have_legible_caption_images():
    for genre in m.genres():
        im=m.subtitle_card(7,genre)
        assert im.size==(1080,160)
        assert im.getbbox() is not None
        assert np.asarray(im)[:,945:,:3].mean()<40

def test_mask_is_opaque_where_old_caption_was_clipped():
    im=np.asarray(m.subtitle_card(0))
    assert np.all(im[40:,:,3]==255)

def test_output_is_never_approved_implicitly():
    assert 'HUMAN_REVIEW' in m.OUTPUT.name
    assert 'PUBLICATION' not in m.OUTPUT.name
