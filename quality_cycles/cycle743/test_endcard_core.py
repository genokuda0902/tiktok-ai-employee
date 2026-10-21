import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from endcard_core import load_genres,stage_at,inside_safe_area,BLACK_FRAME_INDICES
def test_ten_genres():
    genres=load_genres(ROOT/"config"/"endcards.json")
    assert len(genres)==10
def test_boot_prerequisite():
    science=load_genres(ROOT/"config"/"endcards.json")["雑学・科学"]
    assert "microSD" in science[0][0]
    assert "OS" in science[0][0]
    assert "print(2 + 3)" in science[2][1]
def test_stage_transitions():
    assert [stage_at(i) for i in (379,394,395,410,411,428)]==[1,1,2,2,3,3]
def test_safe_area():
    assert inside_safe_area()
    assert not inside_safe_area((0,0,1080,1920))
def test_black_flash_indices():
    assert BLACK_FRAME_INDICES==(57,118,177,240,280,327,375)
