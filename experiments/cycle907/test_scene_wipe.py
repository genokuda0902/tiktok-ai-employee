import sys
from pathlib import Path
import numpy as np
import pytest
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parent))
import scene_wipe as s

def test_ten_genres_and_no_posting_actions():
    assert len(s.GENRE_COLORS) == 10
    code = Path(s.__file__).read_text()
    for forbidden in ('requests.post(', 'TikTokApi', 'upload_video', 'merge_pull_request'):
        assert forbidden not in code

def test_seven_boundaries_and_subtitle_safe_region():
    assert s.CUT_FRAMES == (87,174,250,348,435,522,609)
    assert s.CONTENT_HEIGHT <= 1200
    assert s.WIDTH == 1080 and s.HEIGHT == 1920 and s.FPS == 30

def test_mask_is_monotone_and_ends_clear():
    masks = [s.mask_for_frame(i) for i in range(s.WIPE_FRAMES)]
    assert np.all(masks[0] == 255)
    assert np.all(masks[-1] == 0)
    assert all(np.all(b <= a) for a,b in zip(masks,masks[1:]))
    assert any(np.any((m > 0) & (m < 255)) for m in masks[1:-1])

def test_smooth_progress_and_bounds():
    assert s.ease(0) == 0 and s.ease(1) == 1
    assert all(s.ease(i/20) <= s.ease((i+1)/20) for i in range(20))
    for invalid in (-.1,1.1):
        with pytest.raises(ValueError): s.ease(invalid)

def test_rgba_overlay_and_safe_height():
    sample = Image.new('RGB',(1080,1920),'#224466')
    for genre in s.GENRE_COLORS:
        im = s.make_overlay(sample,3,genre)
        assert im.size == (1080,s.CONTENT_HEIGHT)
        assert im.mode == 'RGBA'
        assert 0 < im.getchannel('A').getextrema()[1] <= 255
    with pytest.raises(ValueError): s.make_overlay(sample,3,'unknown')

def test_fail_closed_invalid_input():
    sample = Image.new('RGB',(720,1280))
    with pytest.raises(ValueError): s.make_overlay(sample,0,'ai_work')
    with pytest.raises(ValueError): s.mask_for_frame(8)
    with pytest.raises(ValueError): s.ffmpeg_command(Path('a'), [], Path('b'))

def test_ffmpeg_filter_preserves_audio_and_avoids_caption_overlay():
    folders = [Path(f'/tmp/cut_{c}') for c in s.CUT_FRAMES]
    cmd = s.ffmpeg_command(Path('source.mp4'),folders,Path('output.mp4'))
    assert '-c:a' in cmd and cmd[cmd.index('-c:a')+1] == 'copy'
    assert cmd.count('-i') == 8
    assert 'overlay=x=0:y=0' in cmd[cmd.index('-filter_complex')+1]
    assert '-pix_fmt' in cmd and 'yuv420p' in cmd
