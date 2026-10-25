import pytest
from cycle841.caption_engine import (
    FPS,WIDTH,HEIGHT,GENRE_PALETTES,BOUNDARIES,SCENE_LENGTHS,
    REQUIRED_POLICY,require_review_only,map_cut_aware_time,active_phrase,
    ass_time,single_beat_captions
)

def test_frame_exact():
    assert (WIDTH,HEIGHT,FPS)==(1080,1920,30)
    assert sum(SCENE_LENGTHS)==691
    assert BOUNDARIES==(89,170,249,336,422,511,588)

def test_ten_genres():
    assert len(GENRE_PALETTES)==10
    for genre in GENRE_PALETTES:
        require_review_only(REQUIRED_POLICY,genre)

def test_fail_closed():
    for key in REQUIRED_POLICY:
        invalid={**REQUIRED_POLICY,key:not REQUIRED_POLICY[key]}
        with pytest.raises(ValueError):
            require_review_only(invalid,"ai_work")
    with pytest.raises(ValueError):
        require_review_only(REQUIRED_POLICY,"unsupported")

def test_cut_aware_timeline():
    assert abs(map_cut_aware_time(3.71)-3.31)<.001
    assert abs(map_cut_aware_time(25.83)-23.03)<.001
    assert ass_time(23.03)=="0:00:23.03"

def test_single_active_phrase():
    text=(r"{\c&H00BEC637&}AIで仕事を\N"
          r"{\c&H00F0F0F0&}早くするなら、\N"
          r"{\c&H00F0F0F0&}最初の一歩が大事。")
    assert active_phrase(text)=="AIで仕事を"
    with pytest.raises(ValueError):
        active_phrase("no highlight")

def test_24_state_validation():
    one=(r"Dialogue: 0,0:00:00.27,0:00:00.93,Caption,,0,0,0,,"
         r"{\c&H00BEC637&}AIで仕事を\N"
         r"{\c&H00F0F0F0&}早くするなら、\N"
         r"{\c&H00F0F0F0&}最初の一歩が大事。")
    with pytest.raises(ValueError):
        single_beat_captions(one)
